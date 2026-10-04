"""Mass export dialog for generating multiple PDFs."""

from __future__ import annotations

import os
from tkinter import filedialog, messagebox

import customtkinter as ctk

from app.core import MassExporter, MassExportResult
from app.models import AppConfig, PuzzleBook


class MassExportDialog(ctk.CTkToplevel):
    """Dialog for mass export configuration and execution."""

    def __init__(self, parent: ctk.CTk, book: PuzzleBook, config: AppConfig) -> None:
        super().__init__(parent)
        self.title("Mass Export")
        self.geometry("700x500")
        self.book = book
        self.config = config
        self.exporter = MassExporter()
        self._is_exporting = False
        
        self._build_interface()

    def _build_interface(self) -> None:
        """Build the mass export interface."""
        # Export mode selection
        mode_frame = ctk.CTkFrame(self)
        mode_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(mode_frame, text="Export Mode:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10)
        
        self.export_mode = ctk.StringVar(value="variations")
        ctk.CTkRadioButton(mode_frame, text="Configuration Variations", variable=self.export_mode, value="variations", command=self._update_ui).pack(side="left", padx=10)
        ctk.CTkRadioButton(mode_frame, text="Multiple Solutions per Page", variable=self.export_mode, value="solutions", command=self._update_ui).pack(side="left", padx=10)
        
        # Variations frame
        self.variations_frame = ctk.CTkScrollableFrame(self, height=200)
        self.variations_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Add variation controls
        self._add_variation_controls()
        
        # Output directory
        output_frame = ctk.CTkFrame(self)
        output_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(output_frame, text="Output Directory:").pack(side="left", padx=10)
        self.output_path = ctk.StringVar(value="output/mass_export")
        ctk.CTkEntry(output_frame, textvariable=self.output_path).pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkButton(output_frame, text="Browse", width=80, command=self._browse_output).pack(side="right", padx=5)
        
        # Progress
        self.progress_frame = ctk.CTkFrame(self)
        self.progress_frame.pack(fill="x", padx=10, pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        self.progress_bar.set(0)
        
        self.progress_label = ctk.CTkLabel(self.progress_frame, text="Ready to export")
        self.progress_label.pack(pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        self.export_button = ctk.CTkButton(button_frame, text="Start Export", fg_color="#257B3F", hover_color="#17612D", command=self._start_export)
        self.export_button.pack(side="right", padx=5)
        
        self.cancel_button = ctk.CTkButton(button_frame, text="Cancel", state="disabled", command=self._cancel_export)
        self.cancel_button.pack(side="right", padx=5)
        
        ctk.CTkButton(button_frame, text="Close", command=self.destroy).pack(side="left", padx=5)

    def _add_variation_controls(self) -> None:
        """Add controls for configuration variations."""
        # Solutions per page variations
        solutions_frame = ctk.CTkFrame(self.variations_frame)
        solutions_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(solutions_frame, text="Solutions per Page Variations:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=5)
        
        self.var_1_solution = ctk.BooleanVar(value=True)
        self.var_2_solutions = ctk.BooleanVar(value=True)
        self.var_4_solutions = ctk.BooleanVar(value=True)
        
        ctk.CTkCheckBox(solutions_frame, text="1 solution per page", variable=self.var_1_solution).pack(anchor="w", padx=10)
        ctk.CTkCheckBox(solutions_frame, text="2 solutions per page", variable=self.var_2_solutions).pack(anchor="w", padx=10)
        ctk.CTkCheckBox(solutions_frame, text="4 solutions per page", variable=self.var_4_solutions).pack(anchor="w", padx=10)
        
        # Page format variations
        page_frame = ctk.CTkFrame(self.variations_frame)
        page_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(page_frame, text="Page Format Variations:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=5)
        
        self.var_a4 = ctk.BooleanVar(value=False)
        self.var_letter = ctk.BooleanVar(value=False)
        self.var_6x9 = ctk.BooleanVar(value=False)
        
        ctk.CTkCheckBox(page_frame, text="A4", variable=self.var_a4).pack(anchor="w", padx=10)
        ctk.CTkCheckBox(page_frame, text="Letter", variable=self.var_letter).pack(anchor="w", padx=10)
        ctk.CTkCheckBox(page_frame, text="6×9 in", variable=self.var_6x9).pack(anchor="w", padx=10)

    def _update_ui(self) -> None:
        """Update UI based on export mode."""
        # For simplicity, we'll use variations mode for now
        pass

    def _browse_output(self) -> None:
        """Browse for output directory."""
        directory = filedialog.askdirectory()
        if directory:
            self.output_path.set(directory)

    def _start_export(self) -> None:
        """Start the mass export process."""
        if self._is_exporting:
            return
        
        # Create variations
        variations = []
        
        # Solutions per page variations
        if self.var_1_solution.get():
            config = AppConfig.from_dict(self.config.to_dict())
            config.export.solutions_per_page = 1
            variations.append(("1_solution_per_page", config))
        
        if self.var_2_solutions.get():
            config = AppConfig.from_dict(self.config.to_dict())
            config.export.solutions_per_page = 2
            variations.append(("2_solutions_per_page", config))
        
        if self.var_4_solutions.get():
            config = AppConfig.from_dict(self.config.to_dict())
            config.export.solutions_per_page = 4
            variations.append(("4_solutions_per_page", config))
        
        # Page format variations
        if self.var_a4.get():
            config = AppConfig.from_dict(self.config.to_dict())
            config.page.apply_preset("A4")
            variations.append(("A4_format", config))
        
        if self.var_letter.get():
            config = AppConfig.from_dict(self.config.to_dict())
            config.page.apply_preset("Letter")
            variations.append(("Letter_format", config))
        
        if self.var_6x9.get():
            config = AppConfig.from_dict(self.config.to_dict())
            config.page.apply_preset("6 × 9 in")
            variations.append(("6x9_format", config))
        
        if not variations:
            messagebox.showwarning("No Variations", "Please select at least one variation to export.")
            return
        
        # Create tasks
        output_dir = self.output_path.get()
        self.exporter.create_tasks_from_variations(self.book, self.config, variations, output_dir)
        
        # Start export
        self._is_exporting = True
        self.export_button.configure(state="disabled")
        self.cancel_button.configure(state="normal")
        
        def export_thread():
            result = self.exporter.execute(
                progress_callback=self._on_progress,
                cancel_check=self.exporter.is_cancelled,
            )
            self.after(0, lambda: self._on_export_complete(result))
        
        import threading
        thread = threading.Thread(target=export_thread)
        thread.daemon = True
        thread.start()

    def _on_progress(self, current: int, total: int, message: str) -> None:
        """Handle progress updates."""
        self.after(0, lambda: self.progress_bar.set(current / total))
        self.after(0, lambda: self.progress_label.configure(text=message))

    def _on_export_complete(self, result: MassExportResult) -> None:
        """Handle export completion."""
        self._is_exporting = False
        self.export_button.configure(state="normal")
        self.cancel_button.configure(state="disabled")
        
        if result.failed > 0:
            failure_text = "\n".join([f"{name}: {error}" for name, error in result.failures[:5]])
            messagebox.showwarning(
                "Export Completed with Errors",
                f"Completed: {result.completed}/{result.total}\nFailed: {result.failed}\n\nFailures:\n{failure_text}"
            )
        else:
            messagebox.showinfo("Export Complete", f"Successfully exported {result.completed} PDF(s).")

    def _cancel_export(self) -> None:
        """Cancel the export."""
        self.exporter.cancel()
        self.progress_label.configure(text="Cancelling...")
