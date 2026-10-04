"""Ventana principal; coordina servicios sin incluir lógica de dominio."""

from __future__ import annotations

import os
import queue
import threading
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk
from PIL import Image

from app.core import BookGenerationCancelled, BookGenerationService, validate_app_config, ProjectManager, TemplateManager
from app.csv import import_csv
from app.i18n import LocaleManager, SUPPORTED_LANGUAGES
from app.models import AppConfig, PAGE_PRESETS, PuzzleBook, Project, ProjectMetadata
from app.pdf import PdfBookRenderer
from app.pdf.fonts import FONT_OPTION_NAMES
from app.pdf.preview import render_preview
from app.themes import THEMES
from app.themes.advanced_themes import ADVANCED_THEMES
from app.utils import load_config, save_config
from app.ui.puzzle_overview import PuzzleOverviewDialog
from app.ui.book_preview import BookPreviewWindow
from app.ui.mass_export_dialog import MassExportDialog
from app.ui.visual_editor import VisualEditorDialog
from app.ui.cover_creator import CoverCreatorDialog


class WordSearchBookMakerApp(ctk.CTk):
    """GUI responsiva con una cola de eventos entre hilos y Tk."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Word Search Book Maker")
        self.geometry("1360x860")
        self.minsize(1080, 700)
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.config_model = AppConfig()
        self.imported_book: PuzzleBook | None = None
        self.generated_book: PuzzleBook | None = None
        self.current_project: Project | None = None
        self.project_manager = ProjectManager()
        self.template_manager = TemplateManager()
        self._events: queue.Queue[tuple[str, object]] = queue.Queue()
        self._cancel_event = threading.Event()
        self._worker: threading.Thread | None = None
        self._preview_index = 0
        self._preview_solution = False
        self._preview_width = 760
        self._preview_image: ctk.CTkImage | None = None
        self._variables: dict[str, ctk.Variable] = {}
        self.locale = LocaleManager(self.config_model.language)

        self._build_interface()
        self._set_controls_from_config()
        self._apply_language()
        self.after(100, self._drain_events)

    def _var(self, key: str, value: str | bool = "") -> ctk.Variable:
        variable: ctk.Variable = ctk.BooleanVar(value=value) if isinstance(value, bool) else ctk.StringVar(value=value)
        self._variables[key] = variable
        return variable

    def _section(self, parent: ctk.CTkScrollableFrame, title: str) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", padx=6, pady=(5, 2))
        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(7, 4))
        return frame

    def _entry(self, parent: ctk.CTkFrame, label: str, key: str, width: int = 85) -> ctk.CTkEntry:
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(row, text=label, width=128, anchor="w").pack(side="left")
        entry = ctk.CTkEntry(row, textvariable=self._var(key), width=width)
        entry.pack(side="right")
        return entry

    def _build_interface(self) -> None:
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        sidebar = ctk.CTkScrollableFrame(self, width=360, label_text="CONFIGURACIÓN")
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        content = ctk.CTkFrame(self)
        content.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=1)

        csv_section = self._section(sidebar, "1. Archivo CSV")
        ctk.CTkButton(csv_section, text="CARGAR CSV", command=self._choose_csv).pack(fill="x", padx=10, pady=3)
        self.csv_summary = ctk.CTkLabel(csv_section, text="Aún no se ha cargado ningún CSV.", justify="left", anchor="w", wraplength=310)
        self.csv_summary.pack(fill="x", padx=10, pady=(3, 8))

        page = self._section(sidebar, "2. Página y márgenes")
        preset_row = ctk.CTkFrame(page, fg_color="transparent")
        preset_row.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(preset_row, text="Preset", width=128, anchor="w").pack(side="left")
        ctk.CTkComboBox(preset_row, values=list(PAGE_PRESETS), variable=self._var("page.preset"), command=self._on_preset).pack(side="right")
        self._entry(page, "Ancho", "page.width")
        self._entry(page, "Alto", "page.height")
        unit_row = ctk.CTkFrame(page, fg_color="transparent")
        unit_row.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(unit_row, text="Unidad", width=128, anchor="w").pack(side="left")
        ctk.CTkSegmentedButton(unit_row, values=["mm", "in"], variable=self._var("page.unit")).pack(side="right")
        for name, label in (("top", "Superior"), ("bottom", "Inferior"), ("left", "Izquierdo"), ("right", "Derecho")):
            self._entry(page, f"Margen {label}", f"page.margins.{name}")

        puzzle = self._section(sidebar, "3. Sopa")
        self._entry(puzzle, "Filas", "grid.rows")
        self._entry(puzzle, "Columnas", "grid.columns")
        difficulty_row = ctk.CTkFrame(puzzle, fg_color="transparent")
        difficulty_row.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(difficulty_row, text="Dificultad", width=128, anchor="w").pack(side="left")
        ctk.CTkComboBox(difficulty_row, values=["fácil", "medio", "difícil", "experto", "personalizado"], variable=self._var("grid.difficulty"), command=self._on_difficulty_change, width=165).pack(side="right")
        checks = ctk.CTkFrame(puzzle, fg_color="transparent")
        checks.pack(fill="x", padx=8, pady=3)
        direction_names = [
            ("derecha", "→"), ("izquierda", "←"), ("abajo", "↓"), ("arriba", "↑"),
            ("diagonal_descendente", "↘"), ("diagonal_ascendente", "↙"),
            ("diagonal_descendente_inversa", "↗"), ("diagonal_ascendente_inversa", "↖"),
        ]
        for index, (key, label) in enumerate(direction_names):
            ctk.CTkCheckBox(checks, text=label, width=55, variable=self._var(f"direction.{key}", False)).grid(row=index // 4, column=index % 4, padx=2, pady=2)
        ctk.CTkCheckBox(puzzle, text="Permitir palabras invertidas", variable=self._var("grid.allow_reversed", False)).pack(anchor="w", padx=10, pady=2)
        ctk.CTkCheckBox(puzzle, text="Permitir diagonales", variable=self._var("grid.allow_diagonals", True)).pack(anchor="w", padx=10, pady=2)
        ctk.CTkCheckBox(puzzle, text="Permitir cruces", variable=self._var("grid.allow_intersections", True)).pack(anchor="w", padx=10, pady=2)
        ctk.CTkCheckBox(puzzle, text="Preferir espaciado", variable=self._var("grid.prefer_spacing", True)).pack(anchor="w", padx=10, pady=(2, 7))

        layout = self._section(sidebar, "4. Palabras y diseño")
        self._entry(layout, "Título", "layout.title", 165)
        self._entry(layout, "Subtítulo", "layout.subtitle", 165)
        grid_position_row = ctk.CTkFrame(layout, fg_color="transparent")
        grid_position_row.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(grid_position_row, text="Posición sopa", width=128, anchor="w").pack(side="left")
        ctk.CTkComboBox(grid_position_row, values=["centro", "arriba", "abajo", "izquierda", "derecha", "personalizado"], variable=self._var("layout.grid_position"), width=165).pack(side="right")
        self._entry(layout, "Posición X (%)", "layout.custom_grid_x_percent")
        self._entry(layout, "Posición Y (%)", "layout.custom_grid_y_percent")
        font_row = ctk.CTkFrame(layout, fg_color="transparent")
        font_row.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(font_row, text="Fuente", width=128, anchor="w").pack(side="left")
        ctk.CTkComboBox(font_row, values=list(FONT_OPTION_NAMES), variable=self._var("layout.font_name"), width=165).pack(side="right")
        self._entry(layout, "Tamaño título", "layout.title_size")
        self._entry(layout, "Tamaño subtítulo", "layout.subtitle_size")
        self._entry(layout, "Letra cuadrícula", "layout.grid_font_size")
        self._entry(layout, "Letra palabras", "layout.words_font_size")
        self._entry(layout, "Casilla (pt)", "layout.cell_size")
        self._entry(layout, "Grosor línea", "layout.line_width")
        self._entry(layout, "Columnas palabras", "layout.word_columns")
        order_row = ctk.CTkFrame(layout, fg_color="transparent")
        order_row.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(order_row, text="Orden", width=128, anchor="w").pack(side="left")
        ctk.CTkComboBox(order_row, values=["original", "alfabetico"], variable=self._var("layout.word_order"), width=165).pack(side="right")
        position_row = ctk.CTkFrame(layout, fg_color="transparent")
        position_row.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(position_row, text="Lista", width=128, anchor="w").pack(side="left")
        ctk.CTkComboBox(position_row, values=["abajo", "arriba", "izquierda", "derecha"], variable=self._var("layout.words_position"), width=165).pack(side="right")
        ctk.CTkCheckBox(layout, text="Ajustar automáticamente", variable=self._var("layout.auto_fit", True)).pack(anchor="w", padx=10, pady=(2, 7))

        export = self._section(sidebar, "5. Soluciones y exportación")
        ctk.CTkCheckBox(export, text="Incluir soluciones", variable=self._var("export.include_solutions", True)).pack(anchor="w", padx=10, pady=2)
        export_mode_row = ctk.CTkFrame(export, fg_color="transparent")
        export_mode_row.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(export_mode_row, text="Modo export", width=128, anchor="w").pack(side="left")
        ctk.CTkComboBox(export_mode_row, values=["completo", "puzzles_solamente", "soluciones_solamente"], variable=self._var("export.export_mode"), width=165).pack(side="right")
        solutions_per_row = ctk.CTkFrame(export, fg_color="transparent")
        solutions_per_row.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(solutions_per_row, text="Soluciones/página", width=128, anchor="w").pack(side="left")
        ctk.CTkComboBox(solutions_per_row, values=["1", "2", "4"], variable=self._var("export.solutions_per_page"), width=165).pack(side="right")
        for label, key, values in [
            ("Estilo", "export.solution_style", ["círculo", "línea", "resaltado"]),
            ("Orden", "export.order_mode", ["consecutivo", "soluciones_al_final"]),
        ]:
            row = ctk.CTkFrame(export, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=2)
            ctk.CTkLabel(row, text=label, width=128, anchor="w").pack(side="left")
            ctk.CTkComboBox(row, values=values, variable=self._var(key), width=165).pack(side="right")
        self._entry(export, "Sopas (todas/1-3)", "export.selected_puzzles", 165)
        self._entry(export, "Archivo PDF", "export.output_path", 165)
        buttons = ctk.CTkFrame(export, fg_color="transparent")
        buttons.pack(fill="x", padx=10, pady=(3, 7))
        ctk.CTkButton(buttons, text="Carpeta", width=90, command=self._choose_output).pack(side="left")
        ctk.CTkButton(buttons, text="ABRIR CARPETA", width=120, command=self._open_output_folder).pack(side="right")

        config_section = self._section(sidebar, "6. Configuración JSON")
        json_buttons = ctk.CTkFrame(config_section, fg_color="transparent")
        json_buttons.pack(fill="x", padx=10, pady=(1, 8))
        ctk.CTkButton(json_buttons, text="Guardar", width=95, command=self._save_configuration).pack(side="left")
        ctk.CTkButton(json_buttons, text="Cargar", width=95, command=self._load_configuration).pack(side="left", padx=5)
        ctk.CTkButton(json_buttons, text="Restablecer", width=95, command=self._reset_configuration).pack(side="right")

        settings_section = self._section(sidebar, "7. Ajustes")
        lang_row = ctk.CTkFrame(settings_section, fg_color="transparent")
        lang_row.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(lang_row, text="Idioma", width=128, anchor="w").pack(side="left")
        ctk.CTkComboBox(lang_row, values=SUPPORTED_LANGUAGES, variable=self._var("settings.language"), command=self._on_language_change, width=165).pack(side="right")
        theme_row = ctk.CTkFrame(settings_section, fg_color="transparent")
        theme_row.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(theme_row, text="Tema", width=128, anchor="w").pack(side="left")
        ctk.CTkComboBox(theme_row, values=list(THEMES.keys()), variable=self._var("settings.theme"), command=self._on_theme_change, width=165).pack(side="right")
        
        # Advanced theme button
        ctk.CTkButton(settings_section, text="Editor Visual", command=self._open_visual_editor).pack(fill="x", padx=10, pady=2)
        ctk.CTkButton(settings_section, text="Creador Portada", command=self._open_cover_creator).pack(fill="x", padx=10, pady=2)

        project_section = self._section(sidebar, "8. Proyectos")
        project_buttons = ctk.CTkFrame(project_section, fg_color="transparent")
        project_buttons.pack(fill="x", padx=10, pady=(1, 4))
        ctk.CTkButton(project_buttons, text="Nuevo", width=75, command=self._create_project).pack(side="left")
        ctk.CTkButton(project_buttons, text="Abrir", width=75, command=self._open_project).pack(side="left", padx=3)
        ctk.CTkButton(project_buttons, text="Guardar", width=75, command=self._save_project).pack(side="left", padx=3)
        project_buttons2 = ctk.CTkFrame(project_section, fg_color="transparent")
        project_buttons2.pack(fill="x", padx=10, pady=(0, 4))
        ctk.CTkButton(project_buttons2, text="Duplicar", width=75, command=self._duplicate_project).pack(side="left")
        ctk.CTkButton(project_buttons2, text="Renombrar", width=75, command=self._rename_project).pack(side="left", padx=3)
        ctk.CTkButton(project_buttons2, text="Eliminar", width=75, command=self._delete_project).pack(side="left", padx=3)
        self.project_name_entry = self._entry(project_section, "Nombre proyecto", "project.name", 165)
        self.project_status = ctk.CTkLabel(project_section, text="Sin proyecto cargado", anchor="w", wraplength=310)
        self.project_status.pack(fill="x", padx=10, pady=(2, 8))

        template_section = self._section(sidebar, "9. Plantillas")
        template_buttons = ctk.CTkFrame(template_section, fg_color="transparent")
        template_buttons.pack(fill="x", padx=10, pady=(1, 4))
        ctk.CTkButton(template_buttons, text="Guardar", width=75, command=self._save_template).pack(side="left")
        ctk.CTkButton(template_buttons, text="Cargar", width=75, command=self._load_template).pack(side="left", padx=3)
        ctk.CTkButton(template_buttons, text="Eliminar", width=75, command=self._delete_template).pack(side="left", padx=3)
        self.template_name_entry = self._entry(template_section, "Nombre plantilla", "template.name", 165)
        self.template_status = ctk.CTkLabel(template_section, text="Plantillas disponibles", anchor="w", wraplength=310)
        self.template_status.pack(fill="x", padx=10, pady=(2, 8))

        ctk.CTkLabel(content, text="PREVISUALIZACIÓN", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, pady=(12, 4))
        self.preview_area = ctk.CTkScrollableFrame(content, label_text="Cargue un CSV y pulse PREVISUALIZAR")
        self.preview_area.grid(row=1, column=0, sticky="nsew", padx=12, pady=5)
        self.preview_label = ctk.CTkLabel(self.preview_area, text="", anchor="center")
        self.preview_label.pack(expand=True, padx=8, pady=8)
        controls = ctk.CTkFrame(content)
        controls.grid(row=2, column=0, sticky="ew", padx=12, pady=(5, 12))
        self.previous_button = ctk.CTkButton(controls, text="← Anterior", width=105, command=lambda: self._move_preview(-1))
        self.previous_button.pack(side="left", padx=5, pady=8)
        self.next_button = ctk.CTkButton(controls, text="Siguiente →", width=105, command=lambda: self._move_preview(1))
        self.next_button.pack(side="left", padx=5, pady=8)
        self.solution_switch = ctk.CTkSwitch(controls, text="Ver solución", variable=self._var("preview.solution", False), command=self._refresh_preview)
        self.solution_switch.pack(side="left", padx=10)
        ctk.CTkButton(controls, text="−", width=35, command=lambda: self._change_zoom(-90)).pack(side="left", padx=2)
        ctk.CTkButton(controls, text="+", width=35, command=lambda: self._change_zoom(90)).pack(side="left", padx=2)
        self.preview_counter = ctk.CTkLabel(controls, text="Sin páginas")
        self.preview_counter.pack(side="left", padx=12)
        self.mass_export_button = ctk.CTkButton(controls, text="MASS EXPORT", width=110, command=self._open_mass_export)
        self.mass_export_button.pack(side="right", padx=5)
        self.book_preview_button = ctk.CTkButton(controls, text="PREVIEW BOOK", width=120, command=self._open_book_preview)
        self.book_preview_button.pack(side="right", padx=5)
        self.overview_button = ctk.CTkButton(controls, text="VER SOPAS", width=100, command=self._open_puzzle_overview)
        self.overview_button.pack(side="right", padx=5)
        self.preview_button = ctk.CTkButton(controls, text="PREVISUALIZAR", command=lambda: self._start_work("preview"))
        self.preview_button.pack(side="right", padx=5)
        self.export_button = ctk.CTkButton(controls, text="GENERAR PDF", fg_color="#257B3F", hover_color="#17612D", command=lambda: self._start_work("export"))
        self.export_button.pack(side="right", padx=5)
        self.regenerate_button = ctk.CTkButton(controls, text="REGENERAR SOPA", width=140, command=lambda: self._start_work("regenerate_single"))
        self.regenerate_button.pack(side="right", padx=5)
        self.mass_button = ctk.CTkButton(controls, text="GENERACIÓN MASIVA", width=140, command=lambda: self._start_work("mass_generate"))
        self.mass_button.pack(side="right", padx=5)
        self.cancel_button = ctk.CTkButton(controls, text="Cancelar", width=85, state="disabled", command=self._cancel_work)
        self.cancel_button.pack(side="right", padx=5)
        bottom = ctk.CTkFrame(content, fg_color="transparent")
        bottom.grid(row=3, column=0, sticky="ew", padx=18, pady=(0, 10))
        self.progress = ctk.CTkProgressBar(bottom)
        self.progress.pack(side="left", fill="x", expand=True, padx=(0, 12))
        self.progress.set(0)
        self.status = ctk.CTkLabel(bottom, text="Listo.", anchor="w")
        self.status.pack(side="right")

    def _on_preset(self, value: str) -> None:
        if value in PAGE_PRESETS:
            width, height, unit = PAGE_PRESETS[value]
            self._variables["page.width"].set(str(width))
            self._variables["page.height"].set(str(height))
            self._variables["page.unit"].set(unit)

    def _on_difficulty_change(self, value: str) -> None:
        from app.models import DIFFICULTY_PRESETS
        if value in DIFFICULTY_PRESETS:
            preset = DIFFICULTY_PRESETS[value]
            for key, preset_value in preset.items():
                if key == "rows":
                    self._variables["grid.rows"].set(str(preset_value))
                elif key == "columns":
                    self._variables["grid.columns"].set(str(preset_value))
                elif key == "allow_intersections":
                    self._variables["grid.allow_intersections"].set(preset_value)
                elif key == "max_attempts":
                    self._variables["grid.max_attempts"].set(str(preset_value))
                elif key == "prefer_spacing":
                    self._variables["grid.prefer_spacing"].set(preset_value)

    def _on_language_change(self, value: str) -> None:
        self.config_model.language = value
        self.locale.set_language(value)
        self._apply_language()

    def _on_theme_change(self, value: str) -> None:
        self.config_model.theme = value
        self._apply_theme()

    def _set_controls_from_config(self) -> None:
        config = self.config_model
        values: dict[str, str | bool] = {
            "page.preset": config.page.preset, "page.width": str(config.page.width), "page.height": str(config.page.height), "page.unit": config.page.unit,
            "page.margins.top": str(config.page.margins.top), "page.margins.bottom": str(config.page.margins.bottom), "page.margins.left": str(config.page.margins.left), "page.margins.right": str(config.page.margins.right),
            "grid.rows": str(config.grid.rows), "grid.columns": str(config.grid.columns), "grid.allow_reversed": config.grid.allow_reversed,
            "grid.allow_diagonals": config.grid.allow_diagonals, "grid.allow_intersections": config.grid.allow_intersections,
            "grid.prefer_spacing": config.grid.prefer_spacing, "grid.difficulty": config.grid.difficulty,
            "layout.title": config.layout.title, "layout.subtitle": config.layout.subtitle, "layout.word_columns": str(config.layout.word_columns),
            "layout.grid_position": config.layout.grid_position, "layout.custom_grid_x_percent": str(config.layout.custom_grid_x_percent), "layout.custom_grid_y_percent": str(config.layout.custom_grid_y_percent),
            "layout.title_size": str(config.layout.title_size), "layout.subtitle_size": str(config.layout.subtitle_size), "layout.grid_font_size": str(config.layout.grid_font_size),
            "layout.words_font_size": str(config.layout.words_font_size), "layout.cell_size": str(config.layout.cell_size), "layout.line_width": str(config.layout.line_width),
            "layout.font_name": config.layout.font_name if config.layout.font_name in FONT_OPTION_NAMES else "Arial",
            "layout.word_order": config.layout.word_order, "layout.words_position": config.layout.words_position, "layout.auto_fit": config.layout.auto_fit,
            "export.include_solutions": config.export.include_solutions, "export.solution_style": config.export.solution_style, "export.order_mode": config.export.order_mode,
            "export.selected_puzzles": config.export.selected_puzzles, "export.output_path": config.export.output_path,
            "export.solutions_per_page": str(config.export.solutions_per_page),
            "export.export_mode": config.export.export_mode,
            "settings.language": config.language, "settings.theme": config.theme,
            "project.name": self.current_project.metadata.name if self.current_project else "",
        }
        for direction, value in config.grid.directions.items():
            values[f"direction.{direction}"] = value
        for key, value in values.items():
            if key in self._variables:
                self._variables[key].set(value)

    def _as_float(self, key: str, label: str) -> float:
        try:
            return float(str(self._variables[key].get()).replace(",", "."))
        except ValueError as exc:
            raise ValueError(f"{label} debe ser un número.") from exc

    def _as_int(self, key: str, label: str) -> int:
        try:
            return int(str(self._variables[key].get()))
        except ValueError as exc:
            raise ValueError(f"{label} debe ser un número entero.") from exc

    def _read_controls_into_config(self) -> AppConfig:
        # Clonar mediante JSON evita que un trabajo en segundo plano observe
        # cambios que el usuario haga mientras está ejecutándose.
        config = AppConfig.from_dict(self.config_model.to_dict())
        config.page.preset = str(self._variables["page.preset"].get())
        config.page.width, config.page.height = self._as_float("page.width", "Ancho"), self._as_float("page.height", "Alto")
        config.page.unit = str(self._variables["page.unit"].get())
        for name in ("top", "bottom", "left", "right"):
            setattr(config.page.margins, name, self._as_float(f"page.margins.{name}", f"Margen {name}"))
        config.grid.rows, config.grid.columns = self._as_int("grid.rows", "Filas"), self._as_int("grid.columns", "Columnas")
        config.grid.directions = {name: bool(self._variables[f"direction.{name}"].get()) for name in config.grid.directions}
        config.grid.allow_reversed = bool(self._variables["grid.allow_reversed"].get())
        config.grid.allow_diagonals = bool(self._variables["grid.allow_diagonals"].get())
        config.grid.allow_intersections = bool(self._variables["grid.allow_intersections"].get())
        config.grid.prefer_spacing = bool(self._variables["grid.prefer_spacing"].get())
        config.grid.difficulty = str(self._variables["grid.difficulty"].get())
        config.layout.title = str(self._variables["layout.title"].get())
        config.language = str(self._variables["settings.language"].get())
        config.theme = str(self._variables["settings.theme"].get())
        config.layout.subtitle = str(self._variables["layout.subtitle"].get())
        config.layout.grid_position = str(self._variables["layout.grid_position"].get())
        config.layout.custom_grid_x_percent = self._as_float("layout.custom_grid_x_percent", "Posición X")
        config.layout.custom_grid_y_percent = self._as_float("layout.custom_grid_y_percent", "Posición Y")
        config.layout.title_size = self._as_float("layout.title_size", "Tamaño de título")
        config.layout.subtitle_size = self._as_float("layout.subtitle_size", "Tamaño de subtítulo")
        config.layout.grid_font_size = self._as_float("layout.grid_font_size", "Letra de cuadrícula")
        config.layout.words_font_size = self._as_float("layout.words_font_size", "Letra de palabras")
        config.layout.cell_size = self._as_float("layout.cell_size", "Casilla")
        config.layout.line_width = self._as_float("layout.line_width", "Grosor de línea")
        config.layout.word_columns = self._as_int("layout.word_columns", "Columnas de palabras")
        config.layout.font_name = str(self._variables["layout.font_name"].get())
        config.layout.word_order = str(self._variables["layout.word_order"].get())
        config.layout.words_position = str(self._variables["layout.words_position"].get())
        config.layout.auto_fit = bool(self._variables["layout.auto_fit"].get())
        config.export.include_solutions = bool(self._variables["export.include_solutions"].get())
        config.export.solution_style = str(self._variables["export.solution_style"].get())
        config.export.order_mode = str(self._variables["export.order_mode"].get())
        config.export.selected_puzzles = str(self._variables["export.selected_puzzles"].get()) or "todas"
        config.export.output_path = str(self._variables["export.output_path"].get()).strip()
        config.export.solutions_per_page = int(str(self._variables["export.solutions_per_page"].get()))
        if not config.export.output_path:
            raise ValueError("Seleccione un archivo PDF de salida.")
        self.config_model = config
        return config

    def _choose_csv(self) -> None:
        selected = filedialog.askopenfilename(title="Seleccionar CSV", filetypes=[("CSV", "*.csv"), ("Todos los archivos", "*.*")])
        if not selected:
            return
        result = import_csv(selected)
        if not result.success:
            self.imported_book = None
            self.generated_book = None
            self.csv_summary.configure(text="CSV no cargado.\n" + "\n".join(error.display() for error in result.errors[:8]))
            messagebox.showerror("CSV inválido", "\n".join(error.display() for error in result.errors[:12]))
            return
        self.imported_book = result.book
        self.generated_book = None
        assert result.book is not None
        low, high = result.book.word_count_range
        self.csv_summary.configure(text=f"CSV cargado correctamente\nSopas: {len(result.book.puzzles)}\nPalabras totales: {result.book.word_count}\nPalabras por sopa: {low}–{high}")
        self.status.configure(text="CSV listo para generar.")

    def _choose_output(self) -> None:
        current = Path(str(self._variables["export.output_path"].get()) or "output/libro_sopas.pdf")
        selected = filedialog.asksaveasfilename(title="Guardar libro PDF", initialfile=current.name, defaultextension=".pdf", filetypes=[("PDF", "*.pdf")], initialdir=str(current.parent))
        if selected:
            self._variables["export.output_path"].set(selected)

    def _open_output_folder(self) -> None:
        output = Path(str(self._variables["export.output_path"].get()) or "output/libro_sopas.pdf").resolve().parent
        output.mkdir(parents=True, exist_ok=True)
        try:
            os.startfile(str(output))  # type: ignore[attr-defined]  # Windows
        except OSError as exc:
            messagebox.showerror("No se pudo abrir la carpeta", str(exc))

    def _save_configuration(self) -> None:
        try:
            config = self._read_controls_into_config()
        except ValueError as exc:
            messagebox.showerror("Configuración inválida", str(exc))
            return
        destination = filedialog.asksaveasfilename(title="Guardar configuración", defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not destination:
            return
        try:
            save_config(config, destination)
            self.status.configure(text=f"Configuración guardada: {Path(destination).name}")
        except OSError as exc:
            messagebox.showerror("No se pudo guardar", str(exc))

    def _load_configuration(self) -> None:
        source = filedialog.askopenfilename(title="Cargar configuración", filetypes=[("JSON", "*.json")])
        if not source:
            return
        try:
            self.config_model = load_config(source)
            self._set_controls_from_config()
            self.status.configure(text=f"Configuración cargada: {Path(source).name}")
        except (OSError, ValueError) as exc:
            messagebox.showerror("No se pudo cargar la configuración", str(exc))

    def _reset_configuration(self) -> None:
        self.config_model = AppConfig()
        self._set_controls_from_config()
        self.status.configure(text="Valores predeterminados restaurados.")

    def _apply_language(self) -> None:
        """Apply the current language to all UI elements."""
        t = self.locale.ui
        # Update window title
        self.title(t("app_title"))
        # Update section labels
        # Note: CustomTkinter doesn't have a simple way to update all labels
        # dynamically. For a full implementation, we would need to store references
        # to all translatable widgets and update them individually.
        # This is a simplified approach that updates key elements.
        self.status.configure(text=t("ready"))

    def _apply_theme(self) -> None:
        """Apply the current theme to the application."""
        from app.themes import apply_theme
        apply_theme(self.config_model.theme, self)

    def _start_work(self, task: str) -> None:
        if self._worker and self._worker.is_alive():
            return
        if not self.imported_book:
            messagebox.showwarning("Falta el CSV", "Cargue primero un archivo CSV válido.")
            return
        if task == "regenerate_single" and not self.generated_book:
            messagebox.showwarning("Falta generación", "Genere previamente las sopas.")
            return
        if task == "mass_generate" and not self.imported_book:
            messagebox.showwarning("Falta el CSV", "Cargue primero un archivo CSV válido.")
            return
        try:
            config = self._read_controls_into_config()
            selected = config.selected_numbers([puzzle.number for puzzle in self.imported_book.puzzles])
            errors = validate_app_config(config)
            if errors:
                raise ValueError("\n".join(error.display() for error in errors))
        except ValueError as exc:
            messagebox.showerror("Configuración inválida", str(exc))
            return
        self._cancel_event.clear()
        self.progress.set(0)
        self._set_working(True)
        self.status.configure(text="Preparando generación…")
        
        if task == "regenerate_single":
            puzzle_number = self.generated_book.puzzles[self._preview_index].number if self.generated_book else 1
            worker = threading.Thread(target=self._run_work, args=(task, config, puzzle_number), daemon=True)
        else:
            worker = threading.Thread(target=self._run_work, args=(task, config, selected), daemon=True)
        self._worker = worker
        worker.start()

    def _run_work(self, task: str, config: AppConfig, selected: list[int] | int) -> None:
        def progress(done: int, total: int, status: str) -> None:
            self._events.put(("progress", (done / max(total, 1), status)))
        try:
            if task == "regenerate_single":
                puzzle_number = selected  # type: ignore[assignment]
                generated = BookGenerationService().regenerate_single_puzzle(
                    self.generated_book, puzzle_number, config.grid, progress, self._cancel_event.is_set
                )
            elif task == "mass_generate":
                generated, failures = BookGenerationService().generate_mass(
                    self.imported_book, config.grid, progress, self._cancel_event.is_set
                )
                if failures:
                    failure_msg = f"{len(failures)} puzzles failed to generate: {', '.join(str(f[0]) for f in failures)}"
                    self._events.put(("mass_done", (generated, failures, failure_msg)))
                else:
                    self._events.put(("mass_done", (generated, [], "All puzzles generated successfully")))
            else:
                generated = BookGenerationService().generate(
                    self.imported_book, config.grid, selected, progress, self._cancel_event.is_set  # type: ignore[arg-type]
                )
            if self._cancel_event.is_set():
                raise BookGenerationCancelled()
            if task == "export":
                rendered_path = PdfBookRenderer().export(generated, config, progress=progress, cancelled=self._cancel_event.is_set)
                self._events.put(("export_done", (generated, rendered_path)))
            elif task == "regenerate_single":
                self._events.put(("regenerate_done", generated))
            elif task == "mass_generate":
                # Mass generation results handled above
                pass
            else:
                self._events.put(("preview_done", generated))
        except BookGenerationCancelled:
            self._events.put(("cancelled", None))
        except InterruptedError:
            self._events.put(("cancelled", None))
        except Exception as exc:  # El hilo comunica el error; Tk se toca solo en el principal.
            self._events.put(("error", str(exc)))

    def _drain_events(self) -> None:
        try:
            while True:
                kind, payload = self._events.get_nowait()
                if kind == "progress":
                    fraction, status = payload  # type: ignore[misc]
                    self.progress.set(fraction)
                    self.status.configure(text=status)
                elif kind == "preview_done":
                    self.generated_book = payload  # type: ignore[assignment]
                    self._preview_index = 0
                    self._preview_solution = False
                    self._variables["preview.solution"].set(False)
                    self._refresh_preview()
                    self.status.configure(text="Previsualización preparada.")
                    self.progress.set(1)
                    self._set_working(False)
                elif kind == "regenerate_done":
                    self.generated_book = payload  # type: ignore[assignment]
                    self._refresh_preview()
                    self.status.configure(text=f"Sopa {self._preview_index + 1} regenerada. Otras sopas sin cambios.")
                    self.progress.set(1)
                    self._set_working(False)
                elif kind == "mass_done":
                    generated, failures, message = payload  # type: ignore[assignment]
                    self.generated_book = generated
                    self._refresh_preview()
                    self.status.configure(text=message)
                    self.progress.set(1)
                    self._set_working(False)
                    if failures:
                        failure_text = "\n".join(f"Puzzle {f[0]}: {f[1][0] if f[1] else 'Unknown error'}" for f in failures[:5])
                        messagebox.showwarning("Generación Masiva", f"{len(failures)} puzzles fallaron:\n{failure_text}")
                elif kind == "export_done":
                    book, output = payload  # type: ignore[misc]
                    self.generated_book = book
                    self._preview_index = 0
                    self._refresh_preview()
                    self.status.configure(text=f"PDF generado: {output}")
                    self.progress.set(1)
                    self._set_working(False)
                    messagebox.showinfo("PDF generado", f"El libro se guardó en:\n{output}")
                elif kind == "cancelled":
                    self.status.configure(text="Operación cancelada; no se creó un PDF incompleto.")
                    self.progress.set(0)
                    self._set_working(False)
                elif kind == "error":
                    self.status.configure(text="La operación no pudo completarse.")
                    self._set_working(False)
                    messagebox.showerror("Error de generación", str(payload))
        except queue.Empty:
            pass
        self.after(100, self._drain_events)

    def _set_working(self, working: bool) -> None:
        state = "disabled" if working else "normal"
        self.preview_button.configure(state=state)
        self.export_button.configure(state=state)
        self.regenerate_button.configure(state=state)
        self.cancel_button.configure(state="normal" if working else "disabled")

    def _cancel_work(self) -> None:
        self._cancel_event.set()
        self.status.configure(text="Cancelando de forma segura…")
        self.cancel_button.configure(state="disabled")

    def _move_preview(self, delta: int) -> None:
        if not self.generated_book:
            return
        self._preview_index = max(0, min(len(self.generated_book.puzzles) - 1, self._preview_index + delta))
        self._refresh_preview()

    def _change_zoom(self, delta: int) -> None:
        self._preview_width = max(360, min(1400, self._preview_width + delta))
        self._refresh_preview()

    def _refresh_preview(self) -> None:
        if not self.generated_book or not self.generated_book.puzzles:
            self.preview_label.configure(text="No hay páginas generadas.", image=None)
            self.preview_counter.configure(text="Sin páginas")
            return
        self._preview_solution = bool(self._variables["preview.solution"].get())
        puzzle = self.generated_book.puzzles[self._preview_index]
        try:
            image: Image.Image = render_preview(puzzle, self.config_model, self._preview_solution, max_width=self._preview_width)
            self._preview_image = ctk.CTkImage(light_image=image, dark_image=image, size=image.size)
            self.preview_label.configure(image=self._preview_image, text="")
            kind = "Solución" if self._preview_solution else "Sopa"
            self.preview_counter.configure(text=f"{kind} {self._preview_index + 1} de {len(self.generated_book.puzzles)}")
        except Exception as exc:
            self.preview_label.configure(image=None, text=f"No se pudo crear la previsualización:\n{exc}")

    def _create_project(self) -> None:
        """Create a new project."""
        project_name = self._variables.get("project.name")
        if project_name:
            name = project_name.get()
        else:
            name = "nuevo_proyecto"
        
        if not name:
            messagebox.showerror("Error", "Por favor ingrese un nombre para el proyecto.")
            return
        
        try:
            config = self._read_controls_into_config()
            project = self.project_manager.create_project(name, config, self.generated_book)
            self.current_project = project
            self._update_project_status()
            messagebox.showinfo("Proyecto Creado", f"Proyecto '{name}' creado exitosamente.")
        except Exception as exc:
            messagebox.showerror("Error", f"No se pudo crear el proyecto: {exc}")

    def _open_project(self) -> None:
        """Open an existing project."""
        projects = self.project_manager.list_projects()
        if not projects:
            messagebox.showinfo("Abrir Proyecto", "No hay proyectos guardados.")
            return
        
        # Create a simple dialog to select project
        dialog = ctk.CTkToplevel(self)
        dialog.title("Seleccionar Proyecto")
        dialog.geometry("400x300")
        
        listbox = ctk.CTkScrollableFrame(dialog, width=350, height=200)
        listbox.pack(padx=20, pady=20)
        
        selected_project = [None]
        
        for project_name in projects:
            btn = ctk.CTkButton(listbox, text=project_name, command=lambda n=project_name: selected_project.__setitem__(0, n))
            btn.pack(fill="x", pady=2)
        
        def on_select():
            if selected_project[0]:
                try:
                    project = self.project_manager.load_project(selected_project[0])
                    self.current_project = project
                    self.config_model = project.config
                    self.generated_book = project.book
                    self._variables["project.name"].set(project.metadata.name)
                    self._set_controls_from_config()
                    self._update_project_status()
                    self._refresh_preview()
                    dialog.destroy()
                    messagebox.showinfo("Proyecto Abierto", f"Proyecto '{selected_project[0]}' cargado exitosamente.")
                except Exception as exc:
                    messagebox.showerror("Error", f"No se pudo abrir el proyecto: {exc}")
            else:
                messagebox.showwarning("Selección", "Por favor seleccione un proyecto.")
        
        ctk.CTkButton(dialog, text="Abrir", command=on_select).pack(pady=10)

    def _save_project(self) -> None:
        """Save the current project."""
        if not self.current_project:
            messagebox.showwarning("Guardar Proyecto", "No hay proyecto cargado para guardar.")
            return
        
        try:
            self.current_project.config = self._read_controls_into_config()
            self.current_project.book = self.generated_book
            self.current_project.metadata.name = self._variables.get("project.name", ctk.StringVar(value="")).get()
            self.project_manager.save_project(self.current_project)
            self._update_project_status()
            messagebox.showinfo("Proyecto Guardado", f"Proyecto '{self.current_project.metadata.name}' guardado exitosamente.")
        except Exception as exc:
            messagebox.showerror("Error", f"No se pudo guardar el proyecto: {exc}")

    def _duplicate_project(self) -> None:
        """Duplicate the current project."""
        if not self.current_project:
            messagebox.showwarning("Duplicar Proyecto", "No hay proyecto cargado para duplicar.")
            return
        
        new_name = self.current_project.metadata.name + "_copia"
        try:
            self.project_manager.duplicate_project(self.current_project.metadata.name, new_name)
            messagebox.showinfo("Proyecto Duplicado", f"Proyecto duplicado como '{new_name}'.")
        except Exception as exc:
            messagebox.showerror("Error", f"No se pudo duplicar el proyecto: {exc}")

    def _rename_project(self) -> None:
        """Rename the current project."""
        if not self.current_project:
            messagebox.showwarning("Renombrar Proyecto", "No hay proyecto cargado para renombrar.")
            return
        
        new_name = self._variables.get("project.name", ctk.StringVar(value="")).get()
        if not new_name or new_name == self.current_project.metadata.name:
            messagebox.showwarning("Renombrar Proyecto", "Por favor ingrese un nuevo nombre diferente.")
            return
        
        try:
            self.project_manager.rename_project(self.current_project.metadata.name, new_name)
            self.current_project.metadata.name = new_name
            self._update_project_status()
            messagebox.showinfo("Proyecto Renombrado", f"Proyecto renombrado a '{new_name}'.")
        except Exception as exc:
            messagebox.showerror("Error", f"No se pudo renombrar el proyecto: {exc}")

    def _delete_project(self) -> None:
        """Delete the current project."""
        if not self.current_project:
            messagebox.showwarning("Eliminar Proyecto", "No hay proyecto cargado para eliminar.")
            return
        
        if messagebox.askyesno("Eliminar Proyecto", f"¿Está seguro de eliminar el proyecto '{self.current_project.metadata.name}'? Esta acción no se puede deshacer."):
            try:
                self.project_manager.delete_project(self.current_project.metadata.name)
                self.current_project = None
                self._variables["project.name"].set("")
                self._update_project_status()
                messagebox.showinfo("Proyecto Eliminado", "Proyecto eliminado exitosamente.")
            except Exception as exc:
                messagebox.showerror("Error", f"No se pudo eliminar el proyecto: {exc}")

    def _update_project_status(self) -> None:
        """Update the project status label."""
        if self.current_project:
            metadata = self.current_project.metadata
            status_text = f"Proyecto: {metadata.name}\nEstado: {metadata.status}\nModificado: {metadata.modified_date[:10] if metadata.modified_date else 'N/A'}"
            self.project_status.configure(text=status_text)
        else:
            self.project_status.configure(text="Sin proyecto cargado")

    def _open_puzzle_overview(self) -> None:
        """Open the puzzle organization overview dialog."""
        if not self.generated_book or not self.generated_book.puzzles:
            messagebox.showwarning("Puzzle Overview", "No puzzles generated yet. Please generate puzzles first.")
            return
        
        dialog = PuzzleOverviewDialog(
            self,
            self.generated_book,
            on_select=self._on_puzzle_select,
            on_delete=self._on_puzzle_delete,
            on_duplicate=self._on_puzzle_duplicate,
            on_regenerate=self._on_puzzle_regenerate,
        )

    def _open_book_preview(self) -> None:
        """Open the enhanced book preview window."""
        if not self.generated_book or not self.generated_book.puzzles:
            messagebox.showwarning("Book Preview", "No puzzles generated yet. Please generate puzzles first.")
            return
        
        config = self._read_controls_into_config()
        BookPreviewWindow(self, self.generated_book, config)

    def _open_mass_export(self) -> None:
        """Open the mass export dialog."""
        if not self.generated_book or not self.generated_book.puzzles:
            messagebox.showwarning("Mass Export", "No puzzles generated yet. Please generate puzzles first.")
            return
        
        config = self._read_controls_into_config()
        MassExportDialog(self, self.generated_book, config)

    def _save_template(self) -> None:
        """Save current configuration as a template."""
        template_name = self._variables.get("template.name")
        if template_name:
            name = template_name.get()
        else:
            name = "nueva_plantilla"
        
        if not name:
            messagebox.showerror("Error", "Por favor ingrese un nombre para la plantilla.")
            return
        
        try:
            config = self._read_controls_into_config()
            self.template_manager.create_template_from_config(name, config, category="general")
            self._update_template_status()
            messagebox.showinfo("Plantilla Guardada", f"Plantilla '{name}' guardada exitosamente.")
        except Exception as exc:
            messagebox.showerror("Error", f"No se pudo guardar la plantilla: {exc}")

    def _load_template(self) -> None:
        """Load a template and apply it to current configuration."""
        templates = self.template_manager.list_templates()
        if not templates:
            messagebox.showinfo("Cargar Plantilla", "No hay plantillas guardadas.")
            return
        
        # Create a simple dialog to select template
        dialog = ctk.CTkToplevel(self)
        dialog.title("Seleccionar Plantilla")
        dialog.geometry("400x300")
        
        listbox = ctk.CTkScrollableFrame(dialog, width=350, height=200)
        listbox.pack(padx=20, pady=20)
        
        selected_template = [None]
        
        for template_name in templates:
            btn = ctk.CTkButton(listbox, text=template_name, command=lambda n=template_name: selected_template.__setitem__(0, n))
            btn.pack(fill="x", pady=2)
        
        def on_select():
            if selected_template[0]:
                try:
                    config = self._read_controls_into_config()
                    merged_config = self.template_manager.apply_template(selected_template[0], config)
                    self.config_model = merged_config
                    self._set_controls_from_config()
                    self._variables["template.name"].set(selected_template[0])
                    dialog.destroy()
                    messagebox.showinfo("Plantilla Cargada", f"Plantilla '{selected_template[0]}' aplicada exitosamente.")
                except Exception as exc:
                    messagebox.showerror("Error", f"No se pudo cargar la plantilla: {exc}")
            else:
                messagebox.showwarning("Selección", "Por favor seleccione una plantilla.")
        
        ctk.CTkButton(dialog, text="Cargar", command=on_select).pack(pady=10)

    def _delete_template(self) -> None:
        """Delete a template."""
        template_name = self._variables.get("template.name")
        if template_name:
            name = template_name.get()
        else:
            name = ""
        
        if not name:
            messagebox.showwarning("Eliminar Plantilla", "Por favor ingrese el nombre de la plantilla a eliminar.")
            return
        
        if messagebox.askyesno("Eliminar Plantilla", f"¿Está seguro de eliminar la plantilla '{name}'? Esta acción no se puede deshacer."):
            try:
                self.template_manager.delete_template(name)
                self._variables["template.name"].set("")
                self._update_template_status()
                messagebox.showinfo("Plantilla Eliminada", "Plantilla eliminada exitosamente.")
            except Exception as exc:
                messagebox.showerror("Error", f"No se pudo eliminar la plantilla: {exc}")

    def _update_template_status(self) -> None:
        """Update the template status label."""
        templates = self.template_manager.list_templates()
        if templates:
            self.template_status.configure(text=f"Plantillas disponibles: {len(templates)}\n{', '.join(templates[:5])}")
        else:
            self.template_status.configure(text="No hay plantillas guardadas")

    def _open_visual_editor(self) -> None:
        """Open the visual editor dialog."""
        config = self._read_controls_into_config()
        VisualEditorDialog(self, config)

    def _open_cover_creator(self) -> None:
        """Open the cover creator dialog."""
        config = self._read_controls_into_config()
        CoverCreatorDialog(self, config)

    def _on_puzzle_select(self, indices: list[int]) -> None:
        """Handle puzzle selection from overview."""
        # Navigate to the first selected puzzle
        if indices:
            self._preview_index = indices[0]
            self._refresh_preview()

    def _on_puzzle_delete(self, indices: list[int]) -> None:
        """Handle puzzle deletion from overview."""
        if not self.generated_book:
            return
        
        # Delete puzzles in reverse order to preserve indices
        for index in sorted(indices, reverse=True):
            if 0 <= index < len(self.generated_book.puzzles):
                del self.generated_book.puzzles[index]
        
        # Re-number remaining puzzles
        for i, puzzle in enumerate(self.generated_book.puzzles):
            puzzle.number = i + 1
        
        self._refresh_preview()
        messagebox.showinfo("Puzzles Deleted", f"Deleted {len(indices)} puzzle(s).")

    def _on_puzzle_duplicate(self, indices: list[int]) -> None:
        """Handle puzzle duplication from overview."""
        if not self.generated_book:
            return
        
        from app.models import Word
        from copy import deepcopy
        
        # Duplicate puzzles
        for index in sorted(indices):
            if 0 <= index < len(self.generated_book.puzzles):
                original = self.generated_book.puzzles[index]
                # Create deep copy of the puzzle
                new_puzzle = deepcopy(original)
                self.generated_book.puzzles.insert(index + 1, new_puzzle)
        
        # Re-number all puzzles
        for i, puzzle in enumerate(self.generated_book.puzzles):
            puzzle.number = i + 1
        
        self._refresh_preview()
        messagebox.showinfo("Puzzles Duplicated", f"Duplicated {len(indices)} puzzle(s).")

    def _on_puzzle_regenerate(self, indices: list[int]) -> None:
        """Handle puzzle regeneration from overview."""
        if not self.generated_book:
            return
        
        from app.core import BookGenerationService
        from app.models import GenerationResult
        
        service = BookGenerationService()
        config = self._read_controls_into_config()
        
        regenerated_count = 0
        for index in indices:
            if 0 <= index < len(self.generated_book.puzzles):
                puzzle = self.generated_book.puzzles[index]
                result: GenerationResult = service.regenerate_single_puzzle(puzzle, config.grid)
                if result.success and result.puzzle:
                    self.generated_book.puzzles[index] = result.puzzle
                    regenerated_count += 1
        
        self._refresh_preview()
        messagebox.showinfo("Puzzles Regenerated", f"Regenerated {regenerated_count} of {len(indices)} puzzle(s).")
