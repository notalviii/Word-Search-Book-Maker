"""Translation dictionaries for English and Spanish.

All user-facing text should be translated here. The same translations
are used for both the UI and PDF generation to avoid duplication.
"""

from __future__ import annotations

from typing import TypedDict


class UITranslations(TypedDict):
    # Main window
    app_title: str
    configuration: str
    preview: str
    ready: str
    preparing_generation: str
    cancelling: str
    operation_cancelled: str
    operation_failed: str
    
    # CSV section
    csv_file: str
    load_csv: str
    csv_not_loaded: str
    csv_loaded: str
    csv_ready: str
    csv_line_1: str
    csv_line_2: str
    csv_line_3: str
    csv_line_4: str
    
    # Page section
    page_and_margins: str
    preset: str
    width: str
    height: str
    unit: str
    margin_top: str
    margin_bottom: str
    margin_left: str
    margin_right: str
    
    # Puzzle section
    puzzle: str
    rows: str
    columns: str
    allow_reversed: str
    allow_diagonals: str
    allow_intersections: str
    
    # Layout section
    words_and_layout: str
    title: str
    subtitle: str
    grid_position: str
    position_x: str
    position_y: str
    font: str
    title_size: str
    subtitle_size: str
    grid_font_size: str
    words_font_size: str
    cell_size: str
    line_width: str
    word_columns: str
    order: str
    word_list: str
    auto_fit: str
    
    # Export section
    solutions_and_export: str
    include_solutions: str
    style: str
    export_order: str
    selected_puzzles: str
    output_pdf: str
    folder: str
    open_folder: str
    
    # Config section
    config_json: str
    save: str
    load: str
    reset: str
    
    # Preview controls
    previous: str
    next: str
    view_solution: str
    preview_button: str
    generate_pdf: str
    cancel: str
    no_pages: str
    solution: str
    puzzle: str
    
    # Dialogs
    select_csv: str
    invalid_csv: str
    save_config: str
    load_config: str
    reset_config: str
    save_pdf: str
    config_invalid: str
    config_saved: str
    config_loaded: str
    defaults_restored: str
    missing_csv: str
    cannot_open_folder: str
    pdf_generated: str
    generation_error: str
    
    # Progress messages
    generating_puzzle: str
    puzzle_generated: str
    rendering_puzzle: str
    rendering_solutions: str
    page_prepared: str
    
    # New features
    language: str
    theme: str
    regenerate_puzzle: str
    regenerating_puzzle: str
    puzzle_regenerated: str
    other_unchanged: str


class PDFTranslations(TypedDict):
    # PDF labels
    word_search: str
    solution: str
    puzzle_number: str
    solution_prefix: str
    words: str
    
    # Error messages
    no_space_vertical: str
    no_space_horizontal: str
    no_space_solution: str
    no_space_grid: str


class Translations(TypedDict):
    ui: UITranslations
    pdf: PDFTranslations


TRANSLATIONS: dict[str, Translations] = {
    "en": {
        "ui": {
            "app_title": "Word Search Book Maker",
            "configuration": "CONFIGURATION",
            "preview": "PREVIEW",
            "ready": "Ready.",
            "preparing_generation": "Preparing generation…",
            "cancelling": "Cancelling safely…",
            "operation_cancelled": "Operation cancelled; no incomplete PDF was created.",
            "operation_failed": "The operation could not be completed.",
            "csv_file": "1. CSV File",
            "load_csv": "LOAD CSV",
            "csv_not_loaded": "No CSV loaded yet.",
            "csv_loaded": "CSV loaded successfully\nPuzzles: {puzzles}\nTotal words: {total}\nWords per puzzle: {range}",
            "csv_ready": "CSV ready to generate.",
            "csv_line_1": "Puzzles:",
            "csv_line_2": "Total words:",
            "csv_line_3": "Words per puzzle:",
            "csv_line_4": "No CSV loaded.",
            "page_and_margins": "2. Page and margins",
            "preset": "Preset",
            "width": "Width",
            "height": "Height",
            "unit": "Unit",
            "margin_top": "Top margin",
            "margin_bottom": "Bottom margin",
            "margin_left": "Left margin",
            "margin_right": "Right margin",
            "puzzle": "3. Puzzle",
            "rows": "Rows",
            "columns": "Columns",
            "allow_reversed": "Allow reversed words",
            "allow_diagonals": "Allow diagonals",
            "allow_intersections": "Allow intersections",
            "words_and_layout": "4. Words and layout",
            "title": "Title",
            "subtitle": "Subtitle",
            "grid_position": "Grid position",
            "position_x": "Position X (%)",
            "position_y": "Position Y (%)",
            "font": "Font",
            "title_size": "Title size",
            "subtitle_size": "Subtitle size",
            "grid_font_size": "Grid letter size",
            "words_font_size": "Words letter size",
            "cell_size": "Cell (pt)",
            "line_width": "Line width",
            "word_columns": "Word columns",
            "order": "Order",
            "word_list": "List",
            "auto_fit": "Auto fit",
            "solutions_and_export": "5. Solutions and export",
            "include_solutions": "Include solutions",
            "style": "Style",
            "export_order": "Order",
            "selected_puzzles": "Puzzles (all/1-3)",
            "output_pdf": "PDF file",
            "folder": "Folder",
            "open_folder": "OPEN FOLDER",
            "config_json": "6. Configuration JSON",
            "save": "Save",
            "load": "Load",
            "reset": "Reset",
            "previous": "← Previous",
            "next": "Next →",
            "view_solution": "View solution",
            "preview_button": "PREVIEW",
            "generate_pdf": "GENERATE PDF",
            "cancel": "Cancel",
            "no_pages": "No pages",
            "solution": "Solution",
            "puzzle": "Puzzle",
            "select_csv": "Select CSV",
            "invalid_csv": "Invalid CSV",
            "save_config": "Save configuration",
            "load_config": "Load configuration",
            "reset_config": "Reset configuration",
            "save_pdf": "Save PDF book",
            "config_invalid": "Invalid configuration",
            "config_saved": "Configuration saved: {name}",
            "config_loaded": "Configuration loaded: {name}",
            "defaults_restored": "Default values restored.",
            "missing_csv": "Missing CSV",
            "cannot_open_folder": "Could not open folder",
            "pdf_generated": "PDF generated",
            "generation_error": "Generation error",
            "generating_puzzle": "Generating puzzle {current} of {total}",
            "puzzle_generated": "Puzzle {number} generated",
            "rendering_puzzle": "Rendering puzzle {number}",
            "rendering_solutions": "Rendering solutions {numbers}",
            "page_prepared": "Page {current} of {total} prepared",
            "language": "Language",
            "theme": "Theme",
            "regenerate_puzzle": "REGENERATE PUZZLE",
            "regenerating_puzzle": "Regenerating puzzle {number}…",
            "puzzle_regenerated": "Puzzle {number} regenerated. Other puzzles unchanged.",
            "other_unchanged": "Other puzzles remain unchanged.",
        },
        "pdf": {
            "word_search": "Word Search",
            "solution": "Solution",
            "puzzle_number": "Puzzle {number}",
            "solution_prefix": "Solution — ",
            "words": "Words",
            "no_space_vertical": "Not enough vertical space for the grid and word list.",
            "no_space_horizontal": "Not enough horizontal space for the grid.",
            "no_space_solution": "Not enough space for four solutions on the page.",
            "no_space_grid": "Not enough space for the grid; reduce content or margins.",
            "no_margin_space": "Margins leave no usable space on the page.",
            # v3.0.0 additions
            "difficulty_easy": "Easy",
            "difficulty_medium": "Medium",
            "difficulty_hard": "Hard",
            "difficulty_expert": "Expert",
            "mass_generation": "Mass Generation",
            "regenerate_selected": "Regenerate Selected",
            "regenerate_all": "Regenerate All",
            "validation_report": "Validation Report",
            "export_puzzles_only": "Export Puzzles Only",
            "export_solutions_only": "Export Solutions Only",
        },
    },
    "es": {
        "ui": {
            "app_title": "Word Search Book Maker",
            "configuration": "CONFIGURACIÓN",
            "preview": "PREVISUALIZACIÓN",
            "ready": "Listo.",
            "preparing_generation": "Preparando generación…",
            "cancelling": "Cancelando de forma segura…",
            "operation_cancelled": "Operación cancelada; no se creó un PDF incompleto.",
            "operation_failed": "La operación no pudo completarse.",
            "csv_file": "1. Archivo CSV",
            "load_csv": "CARGAR CSV",
            "csv_not_loaded": "Aún no se ha cargado ningún CSV.",
            "csv_loaded": "CSV cargado correctamente\nSopas: {puzzles}\nPalabras totales: {total}\nPalabras por sopa: {range}",
            "csv_ready": "CSV listo para generar.",
            "csv_line_1": "Sopas:",
            "csv_line_2": "Palabras totales:",
            "csv_line_3": "Palabras por sopa:",
            "csv_line_4": "No se ha cargado ningún CSV.",
            "page_and_margins": "2. Página y márgenes",
            "preset": "Preset",
            "width": "Ancho",
            "height": "Alto",
            "unit": "Unidad",
            "margin_top": "Margen superior",
            "margin_bottom": "Margen inferior",
            "margin_left": "Margen izquierdo",
            "margin_right": "Margen derecho",
            "puzzle": "3. Sopa",
            "rows": "Filas",
            "columns": "Columnas",
            "allow_reversed": "Permitir palabras invertidas",
            "allow_diagonals": "Permitir diagonales",
            "allow_intersections": "Permitir cruces",
            "words_and_layout": "4. Palabras y diseño",
            "title": "Título",
            "subtitle": "Subtítulo",
            "grid_position": "Posición sopa",
            "position_x": "Posición X (%)",
            "position_y": "Posición Y (%)",
            "font": "Fuente",
            "title_size": "Tamaño título",
            "subtitle_size": "Tamaño subtítulo",
            "grid_font_size": "Letra cuadrícula",
            "words_font_size": "Letra palabras",
            "cell_size": "Casilla (pt)",
            "line_width": "Grosor línea",
            "word_columns": "Columnas palabras",
            "order": "Orden",
            "word_list": "Lista",
            "auto_fit": "Ajustar automáticamente",
            "solutions_and_export": "5. Soluciones y exportación",
            "include_solutions": "Incluir soluciones",
            "style": "Estilo",
            "export_order": "Orden",
            "selected_puzzles": "Sopas (todas/1-3)",
            "output_pdf": "Archivo PDF",
            "folder": "Carpeta",
            "open_folder": "ABRIR CARPETA",
            "config_json": "6. Configuración JSON",
            "save": "Guardar",
            "load": "Cargar",
            "reset": "Restablecer",
            "previous": "← Anterior",
            "next": "Siguiente →",
            "view_solution": "Ver solución",
            "preview_button": "PREVISUALIZAR",
            "generate_pdf": "GENERAR PDF",
            "cancel": "Cancelar",
            "no_pages": "Sin páginas",
            "solution": "Solución",
            "puzzle": "Sopa",
            "select_csv": "Seleccionar CSV",
            "invalid_csv": "CSV inválido",
            "save_config": "Guardar configuración",
            "load_config": "Cargar configuración",
            "reset_config": "Restablecer configuración",
            "save_pdf": "Guardar libro PDF",
            "config_invalid": "Configuración inválida",
            "config_saved": "Configuración guardada: {name}",
            "config_loaded": "Configuración cargada: {name}",
            "defaults_restored": "Valores predeterminados restaurados.",
            "missing_csv": "Falta el CSV",
            "cannot_open_folder": "No se pudo abrir la carpeta",
            "pdf_generated": "PDF generado",
            "generation_error": "Error de generación",
            "generating_puzzle": "Generando sopa {current} de {total}",
            "puzzle_generated": "Sopa {number} generada",
            "rendering_puzzle": "Renderizando sopa {number}",
            "rendering_solutions": "Renderizando soluciones {numbers}",
            "page_prepared": "Página {current} de {total} preparada",
            "language": "Idioma",
            "theme": "Tema",
            "regenerate_puzzle": "REGENERAR SOPA",
            "regenerating_puzzle": "Regenerando sopa {number}…",
            "puzzle_regenerated": "Sopa {number} regenerada. Otras sopas sin cambios.",
            "other_unchanged": "Otras sopas permanecen sin cambios.",
        },
        "pdf": {
            "word_search": "Sopa de letras",
            "solution": "Solución",
            "puzzle_number": "Sopa {number}",
            "solution_prefix": "Solución — ",
            "words": "Palabras",
            "no_space_vertical": "No hay espacio vertical suficiente para la cuadrícula y la lista de palabras.",
            "no_space_horizontal": "No hay espacio horizontal suficiente para la cuadrícula.",
            "no_space_solution": "No hay espacio suficiente para cuatro soluciones en la página.",
            "no_space_grid": "No hay espacio suficiente para la cuadrícula; reduzca el contenido o los márgenes.",
            "no_margin_space": "Los márgenes no dejan espacio útil en la página.",
            # v3.0.0 additions
            "difficulty_easy": "Fácil",
            "difficulty_medium": "Medio",
            "difficulty_hard": "Difícil",
            "difficulty_expert": "Experto",
            "mass_generation": "Generación Masiva",
            "regenerate_selected": "Regenerar Seleccionados",
            "regenerate_all": "Regenerar Todos",
            "validation_report": "Informe de Validación",
            "export_puzzles_only": "Exportar Solo Puzzles",
            "export_solutions_only": "Exportar Solo Soluciones",
        },
    },
}

SUPPORTED_LANGUAGES = list(TRANSLATIONS.keys())

# Additional language translations for v3.0.0
TRANSLATIONS["fr"] = {
    "ui": {
        "app_title": "Word Search Book Maker",
        "configuration": "CONFIGURATION",
        "preview": "APERÇU",
        "ready": "Prêt.",
        "preparing_generation": "Préparation de la génération…",
        "cancelling": "Annulation en cours…",
        "operation_cancelled": "Opération annulée; aucun PDF incomplet n'a été créé.",
        "operation_failed": "L'opération n'a pas pu être terminée.",
        "csv_file": "1. Fichier CSV",
        "load_csv": "CHARGER CSV",
        "csv_not_loaded": "Aucun CSV chargé.",
        "csv_loaded": "CSV chargé avec succès\nMots fléchés: {puzzles}\nMots totaux: {total}\nMots par puzzle: {range}",
        "csv_ready": "CSV prêt à générer.",
        "csv_line_1": "Mots fléchés:",
        "csv_line_2": "Mots totaux:",
        "csv_line_3": "Mots par puzzle:",
        "csv_line_4": "Aucun CSV chargé.",
        "page_and_margins": "2. Page et marges",
        "preset": "Préréglage",
        "width": "Largeur",
        "height": "Hauteur",
        "unit": "Unité",
        "margin_top": "Marge supérieure",
        "margin_bottom": "Marge inférieure",
        "margin_left": "Marge gauche",
        "margin_right": "Marge droite",
        "puzzle": "3. Mots fléchés",
        "rows": "Lignes",
        "columns": "Colonnes",
        "allow_reversed": "Autoriser les mots inversés",
        "allow_diagonals": "Autoriser les diagonales",
        "allow_intersections": "Autoriser les intersections",
        "words_and_layout": "4. Mots et mise en page",
        "title": "Titre",
        "subtitle": "Sous-titre",
        "grid_position": "Position grille",
        "position_x": "Position X (%)",
        "position_y": "Position Y (%)",
        "font": "Police",
        "title_size": "Taille titre",
        "subtitle_size": "Taille sous-titre",
        "grid_font_size": "Taille lettres grille",
        "words_font_size": "Taille lettres mots",
        "cell_size": "Cellule (pt)",
        "line_width": "Épaisseur ligne",
        "word_columns": "Colonnes mots",
        "order": "Ordre",
        "word_list": "Liste",
        "auto_fit": "Ajustement auto",
        "solutions_and_export": "5. Solutions et export",
        "include_solutions": "Inclure solutions",
        "style": "Style",
        "export_order": "Ordre",
        "selected_puzzles": "Mots fléchés (tous/1-3)",
        "output_pdf": "Fichier PDF",
        "folder": "Dossier",
        "open_folder": "OUVRIR DOSSIER",
        "config_json": "6. Configuration JSON",
        "save": "Enregistrer",
        "load": "Charger",
        "reset": "Réinitialiser",
        "previous": "← Précédent",
        "next": "Suivant →",
        "view_solution": "Voir solution",
        "preview_button": "APERÇU",
        "generate_pdf": "GÉNÉRER PDF",
        "cancel": "Annuler",
        "no_pages": "Aucune page",
        "solution": "Solution",
        "puzzle": "Mots fléchés",
        "select_csv": "Sélectionner CSV",
        "invalid_csv": "CSV invalide",
        "save_config": "Enregistrer configuration",
        "load_config": "Charger configuration",
        "reset_config": "Réinitialiser configuration",
        "save_pdf": "Enregistrer livre PDF",
        "config_invalid": "Configuration invalide",
        "config_saved": "Configuration enregistrée: {name}",
        "config_loaded": "Configuration chargée: {name}",
        "defaults_restored": "Valeurs par défaut restaurées.",
        "missing_csv": "CSV manquant",
        "cannot_open_folder": "Impossible d'ouvrir le dossier",
        "pdf_generated": "PDF généré",
        "generation_error": "Erreur de génération",
        "generating_puzzle": "Génération puzzle {current} sur {total}",
        "puzzle_generated": "Puzzle {number} généré",
        "rendering_puzzle": "Rendu puzzle {number}",
        "rendering_solutions": "Rendu solutions {numbers}",
        "page_prepared": "Page {current} sur {total} préparée",
        "language": "Langue",
        "theme": "Thème",
        "regenerate_puzzle": "RÉGÉNÉRER PUZZLE",
        "regenerating_puzzle": "Régénération puzzle {number}…",
        "puzzle_regenerated": "Puzzle {number} régénéré. Autres puzzles inchangés.",
        "other_unchanged": "Les autres puzzles restent inchangés.",
    },
    "pdf": {
        "word_search": "Mots fléchés",
        "solution": "Solution",
        "puzzle_number": "Puzzle {number}",
        "solution_prefix": "Solution — ",
        "words": "Mots",
        "no_space_vertical": "Pas assez d'espace vertical pour la grille et la liste de mots.",
        "no_space_horizontal": "Pas assez d'espace horizontal pour la grille.",
        "no_space_solution": "Pas assez d'espace pour quatre solutions sur la page.",
        "no_space_grid": "Pas assez d'espace pour la grille; réduisez le contenu ou les marges.",
        "no_margin_space": "Les marges ne laissent aucun espace utilisable sur la page.",
        "difficulty_easy": "Facile",
        "difficulty_medium": "Moyen",
        "difficulty_hard": "Difficile",
        "difficulty_expert": "Expert",
        "mass_generation": "Génération en Masse",
        "regenerate_selected": "Régénérer Sélectionnés",
        "regenerate_all": "Régénérer Tous",
        "validation_report": "Rapport de Validation",
        "export_puzzles_only": "Exporter Uniquement Puzzles",
        "export_solutions_only": "Exporter Uniquement Solutions",
    },
}

TRANSLATIONS["de"] = {
    "ui": {
        "app_title": "Word Search Book Maker",
        "configuration": "KONFIGURATION",
        "preview": "VORSCHAU",
        "ready": "Bereit.",
        "preparing_generation": "Generierung wird vorbereitet…",
        "cancelling": "Wird sicher abgebrochen…",
        "operation_cancelled": "Vorgang abgebrochen; kein unvollständiges PDF erstellt.",
        "operation_failed": "Der Vorgang konnte nicht abgeschlossen werden.",
        "csv_file": "1. CSV-Datei",
        "load_csv": "CSV LADEN",
        "csv_not_loaded": "Noch keine CSV geladen.",
        "csv_loaded": "CSV erfolgreich geladen\nRätsel: {puzzles}\nGesamtwörter: {total}\nWörter pro Rätsel: {range}",
        "csv_ready": "CSV bereit zum Generieren.",
        "csv_line_1": "Rätsel:",
        "csv_line_2": "Gesamtwörter:",
        "csv_line_3": "Wörter pro Rätsel:",
        "csv_line_4": "Keine CSV geladen.",
        "page_and_margins": "2. Seite und Ränder",
        "preset": "Voreinstellung",
        "width": "Breite",
        "height": "Höhe",
        "unit": "Einheit",
        "margin_top": "Oberer Rand",
        "margin_bottom": "Unterer Rand",
        "margin_left": "Linker Rand",
        "margin_right": "Rechter Rand",
        "puzzle": "3. Rätsel",
        "rows": "Zeilen",
        "columns": "Spalten",
        "allow_reversed": "Umgekehrte Wörter zulassen",
        "allow_diagonals": "Diagonalen zulassen",
        "allow_intersections": "Schnittpunkte zulassen",
        "words_and_layout": "4. Wörter und Layout",
        "title": "Titel",
        "subtitle": "Untertitel",
        "grid_position": "Gitterposition",
        "position_x": "Position X (%)",
        "position_y": "Position Y (%)",
        "font": "Schriftart",
        "title_size": "Titelgröße",
        "subtitle_size": "Untertitelgröße",
        "grid_font_size": "Gitterbuchstabengröße",
        "words_font_size": "Wortbuchstabengröße",
        "cell_size": "Zelle (pt)",
        "line_width": "Linienbreite",
        "word_columns": "Wortspalten",
        "order": "Reihenfolge",
        "word_list": "Liste",
        "auto_fit": "Auto-Anpassung",
        "solutions_and_export": "5. Lösungen und Export",
        "include_solutions": "Lösungen einschließen",
        "style": "Stil",
        "export_order": "Reihenfolge",
        "selected_puzzles": "Rätsel (alle/1-3)",
        "output_pdf": "PDF-Datei",
        "folder": "Ordner",
        "open_folder": "ORDNER ÖFFNEN",
        "config_json": "6. JSON-Konfiguration",
        "save": "Speichern",
        "load": "Laden",
        "reset": "Zurücksetzen",
        "previous": "← Zurück",
        "next": "Weiter →",
        "view_solution": "Lösung anzeigen",
        "preview_button": "VORSCHAU",
        "generate_pdf": "PDF ERSTELLEN",
        "cancel": "Abbrechen",
        "no_pages": "Keine Seiten",
        "solution": "Lösung",
        "puzzle": "Rätsel",
        "select_csv": "CSV auswählen",
        "invalid_csv": "Ungültige CSV",
        "save_config": "Konfiguration speichern",
        "load_config": "Konfiguration laden",
        "reset_config": "Konfiguration zurücksetzen",
        "save_pdf": "PDF-Buch speichern",
        "config_invalid": "Ungültige Konfiguration",
        "config_saved": "Konfiguration gespeichert: {name}",
        "config_loaded": "Konfiguration geladen: {name}",
        "defaults_restored": "Standardwerte wiederhergestellt.",
        "missing_csv": "CSV fehlt",
        "cannot_open_folder": "Ordner konnte nicht geöffnet werden",
        "pdf_generated": "PDF erstellt",
        "generation_error": "Generierungsfehler",
        "generating_puzzle": "Rätsel {current} von {total} wird generiert",
        "puzzle_generated": "Rätsel {number} generiert",
        "rendering_puzzle": "Rätsel {number} wird gerendert",
        "rendering_solutions": "Lösungen {numbers} werden gerendert",
        "page_prepared": "Seite {current} von {total} vorbereitet",
        "language": "Sprache",
        "theme": "Design",
        "regenerate_puzzle": "RÄTSEL REGENERIEREN",
        "regenerating_puzzle": "Rätsel {number} wird regeneriert…",
        "puzzle_regenerated": "Rätsel {number} regeneriert. Andere Rätsel unverändert.",
        "other_unchanged": "Andere Rätsel bleiben unverändert.",
    },
    "pdf": {
        "word_search": "Wortsuche",
        "solution": "Lösung",
        "puzzle_number": "Rätsel {number}",
        "solution_prefix": "Lösung — ",
        "words": "Wörter",
        "no_space_vertical": "Nicht genug vertikaler Platz für das Gitter und die Wortliste.",
        "no_space_horizontal": "Nicht genug horizontaler Platz für das Gitter.",
        "no_space_solution": "Nicht genug Platz für vier Lösungen auf der Seite.",
        "no_space_grid": "Nicht genug Platz für das Gitter; reduzieren Sie den Inhalt oder die Ränder.",
        "no_margin_space": "Die Ränder lassen keinen nutzbaren Platz auf der Seite.",
        "difficulty_easy": "Einfach",
        "difficulty_medium": "Mittel",
        "difficulty_hard": "Schwer",
        "difficulty_expert": "Experte",
        "mass_generation": "Massengenerierung",
        "regenerate_selected": "Ausgewählte regenerieren",
        "regenerate_all": "Alle regenerieren",
        "validation_report": "Validierungsbericht",
        "export_puzzles_only": "Nur Rätsel exportieren",
        "export_solutions_only": "Nur Lösungen exportieren",
    },
}

TRANSLATIONS["it"] = {
    "ui": {
        "app_title": "Word Search Book Maker",
        "configuration": "CONFIGURAZIONE",
        "preview": "ANTEPRIMA",
        "ready": "Pronto.",
        "preparing_generation": "Preparazione generazione…",
        "cancelling": "Annullamento in corso…",
        "operation_cancelled": "Operazione annullata; nessun PDF incompleto creato.",
        "operation_failed": "L'operazione non ha potuto essere completata.",
        "csv_file": "1. File CSV",
        "load_csv": "CARICA CSV",
        "csv_not_loaded": "Nessun CSV caricato.",
        "csv_loaded": "CSV caricato con successo\nParole nascoste: {puzzles}\nParole totali: {total}\nParole per puzzle: {range}",
        "csv_ready": "CSV pronto per generare.",
        "csv_line_1": "Parole nascoste:",
        "csv_line_2": "Parole totali:",
        "csv_line_3": "Parole per puzzle:",
        "csv_line_4": "Nessun CSV caricato.",
        "page_and_margins": "2. Pagina e margini",
        "preset": "Preset",
        "width": "Larghezza",
        "height": "Altezza",
        "unit": "Unità",
        "margin_top": "Margine superiore",
        "margin_bottom": "Margine inferiore",
        "margin_left": "Margine sinistro",
        "margin_right": "Margine destro",
        "puzzle": "3. Parole nascoste",
        "rows": "Righe",
        "columns": "Colonne",
        "allow_reversed": "Consenti parole invertite",
        "allow_diagonals": "Consenti diagonali",
        "allow_intersections": "Consenti intersezioni",
        "words_and_layout": "4. Parole e layout",
        "title": "Titolo",
        "subtitle": "Sottotitolo",
        "grid_position": "Posizione griglia",
        "position_x": "Posizione X (%)",
        "position_y": "Posizione Y (%)",
        "font": "Carattere",
        "title_size": "Dimensione titolo",
        "subtitle_size": "Dimensione sottotitolo",
        "grid_font_size": "Dimensione lettere griglia",
        "words_font_size": "Dimensione lettere parole",
        "cell_size": "Cella (pt)",
        "line_width": "Spessore linea",
        "word_columns": "Colonne parole",
        "order": "Ordine",
        "word_list": "Lista",
        "auto_fit": "Adattamento auto",
        "solutions_and_export": "5. Soluzioni ed esportazione",
        "include_solutions": "Includi soluzioni",
        "style": "Stile",
        "export_order": "Ordine",
        "selected_puzzles": "Parole nascoste (tutte/1-3)",
        "output_pdf": "File PDF",
        "folder": "Cartella",
        "open_folder": "APRI CARTELLA",
        "config_json": "6. Configurazione JSON",
        "save": "Salva",
        "load": "Carica",
        "reset": "Ripristina",
        "previous": "← Precedente",
        "next": "Successivo →",
        "view_solution": "Vedi soluzione",
        "preview_button": "ANTEPRIMA",
        "generate_pdf": "GENERA PDF",
        "cancel": "Annulla",
        "no_pages": "Nessuna pagina",
        "solution": "Soluzione",
        "puzzle": "Parole nascoste",
        "select_csv": "Seleziona CSV",
        "invalid_csv": "CSV non valido",
        "save_config": "Salva configurazione",
        "load_config": "Carica configurazione",
        "reset_config": "Ripristina configurazione",
        "save_pdf": "Salva libro PDF",
        "config_invalid": "Configurazione non valida",
        "config_saved": "Configurazione salvata: {name}",
        "config_loaded": "Configurazione caricata: {name}",
        "defaults_restored": "Valori predefiniti ripristinati.",
        "missing_csv": "CSV mancante",
        "cannot_open_folder": "Impossibile aprire la cartella",
        "pdf_generated": "PDF generato",
        "generation_error": "Errore di generazione",
        "generating_puzzle": "Generazione puzzle {current} di {total}",
        "puzzle_generated": "Puzzle {number} generato",
        "rendering_puzzle": "Rendering puzzle {number}",
        "rendering_solutions": "Rendering soluzioni {numbers}",
        "page_prepared": "Pagina {current} di {total} preparata",
        "language": "Lingua",
        "theme": "Tema",
        "regenerate_puzzle": "RIGENERA PUZZLE",
        "regenerating_puzzle": "Rigenerazione puzzle {number}…",
        "puzzle_regenerated": "Puzzle {number} rigenerato. Altri puzzle invariati.",
        "other_unchanged": "Gli altri puzzle rimangono invariati.",
    },
    "pdf": {
        "word_search": "Parole nascoste",
        "solution": "Soluzione",
        "puzzle_number": "Puzzle {number}",
        "solution_prefix": "Soluzione — ",
        "words": "Parole",
        "no_space_vertical": "Spazio verticale insufficiente per la griglia e la lista di parole.",
        "no_space_horizontal": "Spazio orizzontale insufficiente per la griglia.",
        "no_space_solution": "Spazio insufficiente per quattro soluzioni sulla pagina.",
        "no_space_grid": "Spazio insufficiente per la griglia; ridurre il contenuto o i margini.",
        "no_margin_space": "I margini non lasciano spazio utilizzabile sulla pagina.",
        "difficulty_easy": "Facile",
        "difficulty_medium": "Medio",
        "difficulty_hard": "Difficile",
        "difficulty_expert": "Esperto",
        "mass_generation": "Generazione in Massa",
        "regenerate_selected": "Rigenera Selezionati",
        "regenerate_all": "Rigenera Tutti",
        "validation_report": "Rapporto di Validazione",
        "export_puzzles_only": "Esporta Solo Puzzle",
        "export_solutions_only": "Esporta Solo Soluzioni",
    },
}

TRANSLATIONS["pt"] = {
    "ui": {
        "app_title": "Word Search Book Maker",
        "configuration": "CONFIGURAÇÃO",
        "preview": "PRÉ-VISUALIZAÇÃO",
        "ready": "Pronto.",
        "preparing_generation": "Preparando geração…",
        "cancelling": "Cancelando com segurança…",
        "operation_cancelled": "Operação cancelada; nenhum PDF incompleto foi criado.",
        "operation_failed": "A operação não pôde ser concluída.",
        "csv_file": "1. Arquivo CSV",
        "load_csv": "CARREGAR CSV",
        "csv_not_loaded": "Nenhum CSV carregado ainda.",
        "csv_loaded": "CSV carregado com sucesso\nCaça-palavras: {puzzles}\nPalavras totais: {total}\nPalavras por puzzle: {range}",
        "csv_ready": "CSV pronto para gerar.",
        "csv_line_1": "Caça-palavras:",
        "csv_line_2": "Palavras totais:",
        "csv_line_3": "Palavras por puzzle:",
        "csv_line_4": "Nenhum CSV carregado.",
        "page_and_margins": "2. Página e margens",
        "preset": "Predefinição",
        "width": "Largura",
        "height": "Altura",
        "unit": "Unidade",
        "margin_top": "Margem superior",
        "margin_bottom": "Margem inferior",
        "margin_left": "Margem esquerda",
        "margin_right": "Margem direita",
        "puzzle": "3. Caça-palavras",
        "rows": "Linhas",
        "columns": "Colunas",
        "allow_reversed": "Permitir palavras invertidas",
        "allow_diagonals": "Permitir diagonais",
        "allow_intersections": "Permitir interseções",
        "words_and_layout": "4. Palavras e layout",
        "title": "Título",
        "subtitle": "Subtítulo",
        "grid_position": "Posição grade",
        "position_x": "Posição X (%)",
        "position_y": "Posição Y (%)",
        "font": "Fonte",
        "title_size": "Tamanho título",
        "subtitle_size": "Tamanho subtítulo",
        "grid_font_size": "Tamanho letras grade",
        "words_font_size": "Tamanho letras palavras",
        "cell_size": "Célula (pt)",
        "line_width": "Espessura linha",
        "word_columns": "Colunas palavras",
        "order": "Ordem",
        "word_list": "Lista",
        "auto_fit": "Ajuste automático",
        "solutions_and_export": "5. Soluções e exportação",
        "include_solutions": "Incluir soluções",
        "style": "Estilo",
        "export_order": "Ordem",
        "selected_puzzles": "Caça-palavras (todos/1-3)",
        "output_pdf": "Arquivo PDF",
        "folder": "Pasta",
        "open_folder": "ABRIR PASTA",
        "config_json": "6. Configuração JSON",
        "save": "Salvar",
        "load": "Carregar",
        "reset": "Redefinir",
        "previous": "← Anterior",
        "next": "Próximo →",
        "view_solution": "Ver solução",
        "preview_button": "PRÉ-VISUALIZAR",
        "generate_pdf": "GERAR PDF",
        "cancel": "Cancelar",
        "no_pages": "Sem páginas",
        "solution": "Solução",
        "puzzle": "Caça-palavras",
        "select_csv": "Selecionar CSV",
        "invalid_csv": "CSV inválido",
        "save_config": "Salvar configuração",
        "load_config": "Carregar configuração",
        "reset_config": "Redefinir configuração",
        "save_pdf": "Salvar livro PDF",
        "config_invalid": "Configuração inválida",
        "config_saved": "Configuração salva: {name}",
        "config_loaded": "Configuração carregada: {name}",
        "defaults_restored": "Valores padrão restaurados.",
        "missing_csv": "CSV ausente",
        "cannot_open_folder": "Não foi possível abrir a pasta",
        "pdf_generated": "PDF gerado",
        "generation_error": "Erro de geração",
        "generating_puzzle": "Gerando puzzle {current} de {total}",
        "puzzle_generated": "Puzzle {number} gerado",
        "rendering_puzzle": "Renderizando puzzle {number}",
        "rendering_solutions": "Renderizando soluções {numbers}",
        "page_prepared": "Página {current} de {total} preparada",
        "language": "Idioma",
        "theme": "Tema",
        "regenerate_puzzle": "REGERAR PUZZLE",
        "regenerating_puzzle": "Regenerando puzzle {number}…",
        "puzzle_regenerated": "Puzzle {number} regenerado. Outros puzzles inalterados.",
        "other_unchanged": "Outros puzzles permanecem inalterados.",
    },
    "pdf": {
        "word_search": "Caça-palavras",
        "solution": "Solução",
        "puzzle_number": "Puzzle {number}",
        "solution_prefix": "Solução — ",
        "words": "Palavras",
        "no_space_vertical": "Espaço vertical insuficiente para a grade e a lista de palavras.",
        "no_space_horizontal": "Espaço horizontal insuficiente para a grade.",
        "no_space_solution": "Espaço insuficiente para quatro soluções na página.",
        "no_space_grid": "Espaço insuficiente para a grade; reduza o conteúdo ou as margens.",
        "no_margin_space": "As margens não deixam espaço utilizável na página.",
        "difficulty_easy": "Fácil",
        "difficulty_medium": "Médio",
        "difficulty_hard": "Difícil",
        "difficulty_expert": "Experto",
        "mass_generation": "Geração em Massa",
        "regenerate_selected": "Regenerar Selecionados",
        "regenerate_all": "Regenerar Todos",
        "validation_report": "Relatório de Validação",
        "export_puzzles_only": "Exportar Apenas Puzzles",
        "export_solutions_only": "Exportar Apenas Soluções",
    },
}

SUPPORTED_LANGUAGES = list(TRANSLATIONS.keys())
