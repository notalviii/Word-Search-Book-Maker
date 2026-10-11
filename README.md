# Word Search Book Maker v3.0.1

A professional Windows desktop application for creating word search puzzle books and their solutions in PDF format. The application maintains the grid, words and coordinates as domain data; solutions are drawn over **the same grid**, never over a regenerated puzzle. 

## Version 3.0.1 New Features

### About Dialog
- **Creator Information**: Displays app creator "not_alviii"
- **Version Display**: Shows current version v3.0.1
- **Application Info**: Displays application name and other metadata

## Version 3.0.0 New Features

### Enhanced Solutions System
- **Flexible Solutions per Page**: Choose between 1, 2, or 4 solutions per page
- **4 Solutions per Page**: Optimised 2×2 grid layout for efficient solution pages
- **Advanced Solution Configuration**: Customise spacing, cell size, line width, highlight colour, and form
- **Solution Display Options**: Show/hide puzzle numbers, titles, and word lists in solutions
- **Automatic Page Calculation**: System automatically calculates required solution pages based on puzzle count
- **Clean Last Page**: When puzzle count isn't a multiple of 4, the last page uses only necessary spaces

### Mass Generation
- **Generate Hundreds of Puzzles**: Generate large quantities of puzzles in a single operation
- **Progress Tracking**: Real-time progress display during mass generation
- **Failure Recovery**: Continues generating even if individual puzzles fail
- **Failure Reporting**: Identifies which puzzles failed and why
- **Retry Failed Puzzles**: Regenerate only the puzzles that failed

### Enhanced Individual Regeneration
- **Regenerate Single Puzzle**: Regenerate only the currently selected puzzle
- **Regenerate Multiple**: Regenerate multiple selected puzzles at once
- **Regenerate All**: Regenerate all puzzles in the book
- **Preserve Others**: Other puzzles remain completely unchanged during regeneration
- **Configuration Preservation**: Each puzzle retains its generation configuration
- **Valid Solutions**: Each regenerated puzzle receives a new valid solution matching its grid

### Difficulty Levels
- **Preset Difficulties**: Easy, Medium, Hard, Expert, and Custom
- **Difficulty-Based Generation**: Difficulty affects the generation algorithm
- **Automatic Configuration**: Each preset configures grid size, intersections, spacing, and attempts
- **Custom Override**: Use Custom mode to manually configure all parameters

### Enhanced Page Formats
- **US Letter**: Standard letter size (8.5 × 11 in)
- **A4**: European standard (210 × 297 mm)
- **6 × 9 in**: Compact book format
- **7 × 10 in**: Popular trade paperback size (NEW in v3.0.0)
- **8.5 × 11 in**: Standard letter format
- **Custom**: Any custom dimensions

### Comprehensive Validation
- **Pre-Export Validation**: Complete validation before PDF generation
- **Error Detection**: Identifies unplaced words, invalid grids, coordinate mismatches
- **Warning System**: Reports potential issues without blocking export
- **Detailed Reports**: Clear categorisation of correct, warning, and error states
- **Margin Validation**: Ensures all elements stay within page margins
- **Solution Validation**: Verifies solution configurations are valid

### Enhanced Project Metadata
- **Project Information**: Project name, theme, language, and status tracking
- **Creation Tracking**: Created date and last modification date
- **Status Management**: Track project status (draft, ready, exported)
- **Source Preservation**: CSV source path preserved in project

### Enhanced Generation Options
- **Word Length Constraints**: Minimum and maximum word length filtering
- **Configurable Spacing**: Toggle prefer spacing for less crowded arrangements
- **Direction Control**: Individual activation/deactivation of all 8 directions
- **Custom Difficulty Override**: Override preset difficulty with custom settings

### Full Project Management System
- **Create Projects**: Create new projects with metadata and configuration
- **Open Projects**: Load existing projects from the projects directory
- **Save Projects**: Save current configuration and puzzles as a project
- **Duplicate Projects**: Create copies of existing projects
- **Rename Projects**: Rename project files
- **Delete Projects**: Remove projects from the projects directory
- **Project Metadata**: Track name, theme, language, status, creation date, and modification date

### Puzzle Organization Overview
- **Grid View**: Visual grid view of all puzzles in the book
- **Puzzle Information**: Display puzzle number, word count, grid size, and generation status
- **Select Puzzles**: Select single or multiple puzzles for batch operations
- **Delete Puzzles**: Remove puzzles from the book
- **Duplicate Puzzles**: Create copies of existing puzzles
- **Regenerate Puzzles**: Regenerate selected puzzles individually or in batches
- **Navigation**: Navigate to specific puzzles from the overview

### Book Preview with Navigation
- **Full Book Preview**: Preview all pages including puzzles and solutions
- **Navigation Controls**: First, previous, next, and last page buttons
- **Page Jump**: Go directly to a specific page number
- **Zoom Controls**: Zoom in and out of the preview
- **Page Type Indicator**: Shows whether the current page is a puzzle or solution
- **Solution Grouping**: Displays when multiple solutions are grouped on one page

### Mass Export
- **Generate Multiple PDFs**: Export multiple PDFs from configuration variations
- **Solution Variations**: Export with 1, 2, or 4 solutions per page
- **Page Format Variations**: Export with different page formats (A4, Letter, 6×9, etc.)
- **Progress Tracking**: Real-time progress during mass export
- **Failure Recovery**: Continues exporting even if individual PDFs fail
- **Summary Report**: Shows completed, failed, and total exports

### Template System
- **Save Templates**: Save current configuration as a reusable template
- **Load Templates**: Apply saved templates to current configuration
- **Delete Templates**: Remove templates from the templates directory
- **Template Categories**: Organise templates by category (general, puzzle, solution, cover)
- **Deep Merge**: Template settings merge with existing configuration
- **Template Metadata**: Track template name, description, creation date, and modification date

### Visual Editor with Drag & Drop
- **Visual Layout Editor**: Visual representation of puzzle page layout
- **Drag & Drop**: Drag elements to reposition them on the page
- **Title Editing**: Edit title text and position
- **Subtitle Editing**: Edit subtitle text and position
- **Font Size Control**: Adjust title and subtitle font sizes
- **Grid Positioning**: Set grid position using X/Y percentages
- **Cell Size Adjustment**: Modify grid cell size
- **Word List Position**: Choose word list position (above, below, left, right)
- **Real-time Preview**: See changes reflected immediately in the preview

### Cover Creator
- **Book Title**: Set the main title for the book cover
- **Subtitle**: Add a subtitle with puzzle count or description
- **Author**: Set the author name
- **Background Colour**: Choose from predefined background colours
- **Theme Selection**: Select from Classic, Modern, Kids, or Elegant themes
- **Visual Preview**: Preview the cover before saving
- **Cover Configuration**: Save cover settings for reuse

### Advanced Theme System
- **Complete Colour Themes**: Full control over UI and PDF colours
- **UI Colours**: Background, panel, button, text, border, and input colours
- **PDF Grid Colours**: Grid background, border, and letter colours
- **PDF Solution Colours**: Highlight, circle, and line colours
- **PDF Word List Colours**: Background and text colours for word lists
- **PDF Title Colours**: Title and subtitle text colours
- **Typography Settings**: Font families and sizes for both UI and PDF
- **Predefined Themes**: Classic, Minimal, Modern, Kids, Elegant, and Large Print
- **Custom Themes**: Create and save custom theme configurations

### Enhanced PDF Export Modes
- **Complete Export**: Export full book with puzzles and solutions (default)
- **Puzzles Only**: Export only puzzle pages without solutions
- **Solutions Only**: Export only solution pages without puzzles
- **Export Mode Selection**: Choose export mode from the interface

### Extended Multi-language Support
- **Six Languages**: English, Spanish, French, German, Italian, and Portuguese
- **Complete Translations**: Full UI and PDF translations for all languages
- **Language Selection**: Choose language from settings panel
- **PDF Language**: Selected language determines PDF labels and headings
- **Language Preservation**: Language choice persisted in configuration
- **Extensible Architecture**: Easy to add additional languages

## Requirements and Installation

- Windows and Python 3.12 or later
- Updated `pip`

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

If PowerShell does not allow activating the environment, you can run `.\.venv\Scripts\python.exe main.py` directly.

## Usage

### Basic Workflow
1. Click **LOAD CSV** and select a UTF-8 file
2. Configure page, margins, grid, directions, and layout
3. Choose difficulty preset or configure custom settings
4. Click **PREVIEW** to generate and preview puzzles
5. Navigate between puzzles, enable *View solution*, and use `+`/`−` to zoom
6. Configure solutions per page (1, 2, or 4)
7. Choose output path and click **GENERATE PDF**

### v3.0.0 Features

**Project Management:**
- Click **Nuevo** to create a new project with current configuration
- Click **Abrir** to load an existing project from the projects directory
- Click **Guardar** to save the current configuration and puzzles as a project
- Click **Duplicar** to create a copy of the current project
- Click **Renombrar** to rename the current project
- Click **Eliminar** to delete the current project
- Project metadata includes name, theme, language, status, and dates

**Puzzle Overview:**
- Click **VER SOPAS** to open the puzzle organization overview
- View all puzzles in a grid with word count, grid size, and status
- Select multiple puzzles using checkboxes
- Click **Regenerate Selected** to regenerate selected puzzles
- Click **Duplicate Selected** to create copies of selected puzzles
- Click **Delete Selected** to remove selected puzzles from the book
- Individual action buttons for each puzzle (Regenerate, Duplicate, Delete)

**Book Preview:**
- Click **PREVIEW BOOK** to open the enhanced book preview window
- Navigate through all pages using First, Previous, Next, Last buttons
- Jump to a specific page using the page number input
- Zoom in and out using the + and - buttons
- Page type indicator shows whether viewing a puzzle or solution page
- Solution grouping displayed when multiple solutions are on one page

**Mass Export:**
- Click **MASS EXPORT** to open the mass export dialog
- Select variations to export (solutions per page, page formats)
- Choose output directory for exported PDFs
- Click **Start Export** to begin mass export
- Progress shows current export and any failures
- Failed exports are reported but don't stop the process
- Summary shows completed, failed, and total exports

**Template System:**
- Enter a template name and click **Guardar** to save current configuration as a template
- Click **Cargar** to apply a saved template to current configuration
- Click **Eliminar** to remove a template
- Templates are stored in the templates directory
- Template settings merge with existing configuration

**Visual Editor:**
- Click **Editor Visual** to open the visual layout editor
- Drag elements on the canvas to reposition them
- Edit title and subtitle text
- Adjust title and subtitle font sizes
- Set grid position using X/Y percentages
- Modify grid cell size
- Choose word list position (above, below, left, right)
- Click **Apply** to save changes to configuration

**Cover Creator:**
- Click **Creador Portada** to open the cover creator
- Enter book title, subtitle, and author
- Choose background colour from predefined options
- Select theme (Classic, Modern, Kids, Elegant)
- Preview the cover before saving
- Click **Save Cover** to save cover configuration

**Mass Generation:**
- Click **GENERACIÓN MASIVA** to generate all puzzles at once
- Progress shows current puzzle and any failures
- Failed puzzles are reported but don't stop generation
- Retry failed puzzles individually

**Individual Regeneration:**
- Navigate to a puzzle and click **REGENERAR SOPA** to regenerate just that puzzle
- Other puzzles remain unchanged
- Preview the regenerated puzzle before export

**Difficulty Presets:**
- Choose from Easy, Medium, Hard, Expert, or Custom
- Each preset automatically configures grid size and generation parameters
- Custom mode allows full manual control

**Solutions Configuration:**
- Select export mode (completo, puzzles_solamente, soluciones_solamente)
- Select 1, 2, or 4 solutions per page
- 4 solutions per page uses an optimised 2×2 grid layout
- Configure solution spacing, cell size, and display options
- Solutions automatically adapt to page format

**Validation:**
- Validation runs automatically before export
- Errors and warnings are reported
- Export is blocked for critical errors

**Language Selection:**
- Choose from English, Spanish, French, German, Italian, or Portuguese
- Selected language affects both UI and PDF labels
- Language choice is persisted in configuration

**Theme Selection:**
- Choose from Light, Dark, Soft, or High Contrast themes
- Advanced themes available through theme system
- Theme choice is persisted in configuration

### Advanced Usage

**Puzzle Selection:**
- The panel allows selecting `all` puzzles, specific numbers (`1,4,8`), or ranges (`1-5,9`)
- Selection applies to generation and export

**Solution Order:**
- **Consecutive**: Puzzle + solution for each group
- **Solutions at End**: All puzzles followed by all solutions

**Solutions per Page:**
- **1 per page**: Full-size solution on each page
- **2 per page**: Two solutions stacked vertically
- **4 per page**: 2×2 grid layout (most efficient)

## CSV Format

No header. Each line is a puzzle and each comma-separated field is a word. Lines may have different numbers of words.

```csv
perro,gato,tigre,león,oso
caballo,VACA,cerdo,oveja,gallina
árbol,niño,pingüino,ÑANDÚ,camión
```

The application removes external spaces and converts internally to uppercase: ` árbol ` becomes `ÁRBOL`. It preserves accents, `Ñ` and `Ü`. Before generation, it blocks empty files, empty lines, empty fields (including trailing commas), duplicates within the same puzzle, non-UTF-8 encoding and words incompatible with the grid.

A file ready for testing is available at [examples/palabras.csv](examples/palabras.csv) and a configuration at [examples/configuracion_animales.json](examples/configuracion_animales.json).

## Configuration and PDF

- Page sizes A4, Letter, 6 × 9 in, 7 × 10 in, 8.5 × 11 in and custom are independent of rows and columns
- The four margins are edited separately in the active page unit (`mm` or `in`)
- Activate directions individually; diagonals, reversed words and intersections are independent options
- *Auto fit* calculates the largest cell that fits together with titles and word list
- Difficulty presets automatically configure grid size and generation parameters
- Save/load configuration in JSON from the interface
- Configuration includes v3.0.0 settings (solutions per page, difficulty, word length constraints)

The PDF is created with ReportLab and uses lines, text and vector marks. Solutions use circles, lines or highlights over the coordinates preserved by the generator.

**v3.0.0 Configuration:**
- `solutions_per_page`: Number of solutions per page (1, 2, or 4)
- `solution_spacing`: Spacing between solutions on multi-solution pages
- `solution_cell_size`: Cell size for solution grids
- `solution_line_width`: Line width for solution highlights
- `solution_highlight_color`: Colour for solution highlights
- `show_puzzle_number_in_solution`: Show puzzle number in solution
- `show_title_in_solution`: Show title in solution
- `show_words_in_solution`: Show word list in solution
- `difficulty`: Difficulty preset (fácil, medio, difícil, experto, personalizado)
- `min_word_length`: Minimum word length
- `max_word_length`: Maximum word length

## Testing

```powershell
python -m unittest discover -s tests -v
```

The suite covers Spanish normalisation, variable/erroneous CSV, generation, direction constraints, coordinates, configurations, layout, valid PDF, language switching, theme loading, individual puzzle regeneration, word spacing behaviour, backwards compatibility, and v3.0.0 features including:
- 1/2/4 solutions per page layouts
- Mass generation with failure recovery
- Multiple puzzle regeneration
- Difficulty presets
- Enhanced validation
- Enhanced export configuration

## Windows Executable

After installing dependencies, run:

```powershell
.\build_windows.bat
```

The executable will appear in `dist\WordSearchBookMaker.exe`. The manual equivalent is:

```powershell
pyinstaller --noconfirm --clean WordSearchBookMaker.spec
```

**v3.0.1 Build:**
- Uses spec file for better packaging control
- Includes all dependencies, translation files, and theme resources
- No Python installation required on target computer
- Launches without console window

### Windows Defender SmartScreen Warning

When you first run the executable, Windows Defender SmartScreen may display a warning because the application is not digitally signed. This is normal for applications built with PyInstaller.

**To unblock the application:**

1. When SmartScreen displays the warning, click **"Más información"** (More info)
2. Click **"Ejecutar de todos modos"** (Run anyway)
3. Windows will remember this decision and will not block the application in the future

**Alternative: Add to Windows Defender exclusions**

If you prefer to add the application to Windows Defender exclusions:

1. Open Windows Defender
2. Go to **"Protección contra virus y amenazas"** > **"Configuración de protección"**
3. Go to **"Exclusiones"** > **"Agregar o quitar exclusiones"**
4. Add the file `WordSearchBookMaker.exe` or the entire `dist` folder

**Alternative: Disable SmartScreen temporarily**

If you prefer to disable the SmartScreen control temporarily:

1. Open Windows Security
2. Go to **"App y navegador"** > **"Control de aplicaciones"**
3. Change **"Control de aplicaciones"** to **"Desactivado"**
4. Run the application
5. Re-enable SmartScreen after running the application

**Note:** The application is safe and created by the developer "not_alviii". It does not contain any malicious code.

## Troubleshooting

- **`python` opens Microsoft Store or does not exist**: Install Python 3.12+ from python.org and check `py -3.12 --version`
- **CSV not loaded**: Save it as UTF-8 and check for trailing commas, duplicates and blank lines
- **Cannot place a puzzle**: Increase rows/columns, allow intersections or activate more directions
- **Layout does not fit**: Reduce margins, title/list or enable auto fit
- **Window does not open**: Confirm the virtual environment is active and that `customtkinter` was installed from `requirements.txt`
- **Solutions layout issues**: Check solutions per page setting and page format
- **Mass generation failures**: Check difficulty settings and word lengths
- **Validation errors**: Review validation report and adjust configuration accordingly

## Architecture

The application maintains clean separation of concerns:
- **Puzzle Engine**: Word search generation with configurable difficulty
- **Solution Engine**: Coordinate-based solution rendering
- **Project Manager**: Configuration and project metadata
- **Layout Engine**: Page layout calculation for puzzles and solutions
- **Renderer**: Vector PDF rendering with ReportLab
- **Validator**: Comprehensive validation before export
- **UI**: CustomTkinter-based interface

## Configuration Options (v3.0.0)

### New Settings
- `solutions_per_page`: Number of solutions per page (1, 2, or 4)
- `solution_spacing`: Spacing between solutions on multi-solution pages
- `solution_cell_size`: Cell size for solution grids
- `solution_line_width`: Line width for solution highlights
- `solution_highlight_color`: Colour for solution highlights
- `solution_highlight_form`: Form of solution highlight (círculo, línea, resaltado)
- `show_puzzle_number_in_solution`: Show puzzle number in solution
- `show_title_in_solution`: Show title in solution
- `show_words_in_solution`: Show word list in solution
- `solution_font_size`: Font size for solution text
- `difficulty`: Difficulty preset (fácil, medio, difícil, experto, personalizado)
- `min_word_length`: Minimum word length
- `max_word_length`: Maximum word length

### Enhanced PuzzleBook Metadata
- `project_name`: Project name
- `theme`: Visual theme
- `language`: Interface and PDF language
- `created_date`: Project creation date
- `modified_date`: Last modification date
- `status`: Project status (draft, ready, exported)

### Backwards Compatibility
- Old configuration files load with defaults for new settings
- All existing settings are preserved
- No existing functionality is removed

## Language Support

The application currently supports:
- **English (en)**: Full UI and PDF support
- **Spanish (es)**: Full UI and PDF support
- **French (fr)**: Full UI and PDF support
- **German (de)**: Full UI and PDF support
- **Italian (it)**: Full UI and PDF support
- **Portuguese (pt)**: Full UI and PDF support

Additional languages can be added by extending the translation dictionaries in `app/i18n/translations.py`.

## Theme Options

The application includes four built-in themes:
- **Light**: Clean, modern light theme (default)
- **Dark**: Sleek dark theme for reduced eye strain
- **Soft**: Gentle, minimal colour scheme
- **High Contrast**: High contrast theme for accessibility

## Version History

### v3.0.1
- **About Dialog**: Added About dialog showing version and creator information
- **Version Update**: Updated to version 3.0.1
- **Creator Credit**: Added creator "not_alviii" to About dialog

### v3.0.0
- **Solutions Enhancement**: Flexible 1/2/4 solutions per page with optimised 2×2 layout
- **Mass Generation**: Generate hundreds of puzzles with failure recovery
- **Enhanced Regeneration**: Regenerate single, multiple, or all puzzles
- **Difficulty Presets**: Easy, Medium, Hard, Expert, and Custom modes
- **Page Formats**: Added 7 × 10 in preset
- **Validation System**: Comprehensive pre-export validation with detailed reports
- **Project Metadata**: Enhanced project tracking with status and dates
- **Generation Options**: Word length constraints and enhanced spacing control
- **Full Project Management**: Create, open, save, duplicate, rename, and delete projects
- **Puzzle Organization Overview**: Grid view of all puzzles with batch operations
- **Book Preview with Navigation**: Full book preview with page navigation and zoom
- **Mass Export**: Export multiple PDFs from configuration variations
- **Template System**: Save, load, and delete reusable configuration templates
- **Visual Editor**: Drag & drop visual editor for page layout
- **Cover Creator**: Create and customise book covers
- **Advanced Theme System**: Complete colour and typography themes for UI and PDF
- **Enhanced PDF Export**: Export modes for complete, puzzles-only, or solutions-only
- **Extended Multi-language**: Added French, German, Italian, and Portuguese (6 languages total)
- **Testing**: Added comprehensive tests for all v3.0.0 features

### v2.0.0
- Multi-language support (English and Spanish)
- Custom visual themes (Light, Dark, Soft, High Contrast)
- Individual puzzle regeneration
- Improved word spacing algorithm
- Enhanced Windows executable packaging

## Credits

**Created by**: not_alviii 🧸 and Devin

## Core Principles

The application adheres to these core principles:
- **Solution Integrity**: Solutions always use the exact grid and coordinates from puzzle generation
- **No Automatic Translation**: User-provided puzzle words are never translated
- **CSV Preservation**: CSV files are never modified by the application
- **Architecture Separation**: Clean separation between generation, rendering, and UI
- **Backwards Compatibility**: Old configuration files load with sensible defaults
