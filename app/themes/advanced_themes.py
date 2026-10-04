"""Advanced theme system for puzzle books."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ThemeColors:
    """Complete color theme for the application and PDF."""
    # UI Colors
    ui_background: str = "#FFFFFF"
    ui_panel: str = "#F0F0F0"
    ui_button: str = "#3B8ED0"
    ui_button_hover: str = "#2C7AC0"
    ui_text: str = "#000000"
    ui_text_secondary: str = "#666666"
    ui_border: str = "#CCCCCC"
    ui_input: str = "#FFFFFF"
    ui_input_border: str = "#CCCCCC"
    
    # PDF Grid Colors
    pdf_grid_background: str = "#FFFFFF"
    pdf_grid_border: str = "#000000"
    pdf_grid_letter: str = "#000000"
    
    # PDF Solution Colors
    pdf_solution_highlight: str = "#D22C2C"
    pdf_solution_circle: str = "#D22C2C"
    pdf_solution_line: str = "#D22C2C"
    
    # PDF Word List Colors
    pdf_word_list_background: str = "#FFFFFF"
    pdf_word_list_text: str = "#000000"
    
    # PDF Title Colors
    pdf_title_text: str = "#000000"
    pdf_subtitle_text: str = "#666666"
    
    # PDF Margins
    pdf_margin_color: str = "#FFFFFF"


@dataclass(slots=True)
class ThemeTypography:
    """Typography settings for the theme."""
    # UI Fonts
    ui_font_family: str = "Arial"
    ui_font_size: int = 12
    ui_title_size: int = 16
    ui_subtitle_size: int = 14
    
    # PDF Fonts
    pdf_font_family: str = "Arial"
    pdf_title_size: float = 18.0
    pdf_subtitle_size: float = 10.0
    pdf_grid_font_size: float = 11.0
    pdf_words_font_size: float = 9.0
    pdf_solution_font_size: float = 8.0


@dataclass(slots=True)
class AdvancedTheme:
    """Complete advanced theme configuration."""
    name: str
    description: str = ""
    colors: ThemeColors = field(default_factory=ThemeColors)
    typography: ThemeTypography = field(default_factory=ThemeTypography)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert theme to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "colors": {
                "ui_background": self.colors.ui_background,
                "ui_panel": self.colors.ui_panel,
                "ui_button": self.colors.ui_button,
                "ui_button_hover": self.colors.ui_button_hover,
                "ui_text": self.colors.ui_text,
                "ui_text_secondary": self.colors.ui_text_secondary,
                "ui_border": self.colors.ui_border,
                "ui_input": self.colors.ui_input,
                "ui_input_border": self.colors.ui_input_border,
                "pdf_grid_background": self.colors.pdf_grid_background,
                "pdf_grid_border": self.colors.pdf_grid_border,
                "pdf_grid_letter": self.colors.pdf_grid_letter,
                "pdf_solution_highlight": self.colors.pdf_solution_highlight,
                "pdf_solution_circle": self.colors.pdf_solution_circle,
                "pdf_solution_line": self.colors.pdf_solution_line,
                "pdf_word_list_background": self.colors.pdf_word_list_background,
                "pdf_word_list_text": self.colors.pdf_word_list_text,
                "pdf_title_text": self.colors.pdf_title_text,
                "pdf_subtitle_text": self.colors.pdf_subtitle_text,
                "pdf_margin_color": self.colors.pdf_margin_color,
            },
            "typography": {
                "ui_font_family": self.typography.ui_font_family,
                "ui_font_size": self.typography.ui_font_size,
                "ui_title_size": self.typography.ui_title_size,
                "ui_subtitle_size": self.typography.ui_subtitle_size,
                "pdf_font_family": self.typography.pdf_font_family,
                "pdf_title_size": self.typography.pdf_title_size,
                "pdf_subtitle_size": self.typography.pdf_subtitle_size,
                "pdf_grid_font_size": self.typography.pdf_grid_font_size,
                "pdf_words_font_size": self.typography.pdf_words_font_size,
                "pdf_solution_font_size": self.typography.pdf_solution_font_size,
            },
        }
    
    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "AdvancedTheme":
        """Load theme from dictionary."""
        colors_raw = raw.get("colors", {})
        colors = ThemeColors(
            ui_background=colors_raw.get("ui_background", "#FFFFFF"),
            ui_panel=colors_raw.get("ui_panel", "#F0F0F0"),
            ui_button=colors_raw.get("ui_button", "#3B8ED0"),
            ui_button_hover=colors_raw.get("ui_button_hover", "#2C7AC0"),
            ui_text=colors_raw.get("ui_text", "#000000"),
            ui_text_secondary=colors_raw.get("ui_text_secondary", "#666666"),
            ui_border=colors_raw.get("ui_border", "#CCCCCC"),
            ui_input=colors_raw.get("ui_input", "#FFFFFF"),
            ui_input_border=colors_raw.get("ui_input_border", "#CCCCCC"),
            pdf_grid_background=colors_raw.get("pdf_grid_background", "#FFFFFF"),
            pdf_grid_border=colors_raw.get("pdf_grid_border", "#000000"),
            pdf_grid_letter=colors_raw.get("pdf_grid_letter", "#000000"),
            pdf_solution_highlight=colors_raw.get("pdf_solution_highlight", "#D22C2C"),
            pdf_solution_circle=colors_raw.get("pdf_solution_circle", "#D22C2C"),
            pdf_solution_line=colors_raw.get("pdf_solution_line", "#D22C2C"),
            pdf_word_list_background=colors_raw.get("pdf_word_list_background", "#FFFFFF"),
            pdf_word_list_text=colors_raw.get("pdf_word_list_text", "#000000"),
            pdf_title_text=colors_raw.get("pdf_title_text", "#000000"),
            pdf_subtitle_text=colors_raw.get("pdf_subtitle_text", "#666666"),
            pdf_margin_color=colors_raw.get("pdf_margin_color", "#FFFFFF"),
        )
        
        typography_raw = raw.get("typography", {})
        typography = ThemeTypography(
            ui_font_family=typography_raw.get("ui_font_family", "Arial"),
            ui_font_size=typography_raw.get("ui_font_size", 12),
            ui_title_size=typography_raw.get("ui_title_size", 16),
            ui_subtitle_size=typography_raw.get("ui_subtitle_size", 14),
            pdf_font_family=typography_raw.get("pdf_font_family", "Arial"),
            pdf_title_size=typography_raw.get("pdf_title_size", 18.0),
            pdf_subtitle_size=typography_raw.get("pdf_subtitle_size", 10.0),
            pdf_grid_font_size=typography_raw.get("pdf_grid_font_size", 11.0),
            pdf_words_font_size=typography_raw.get("pdf_words_font_size", 9.0),
            pdf_solution_font_size=typography_raw.get("pdf_solution_font_size", 8.0),
        )
        
        return cls(
            name=raw.get("name", ""),
            description=raw.get("description", ""),
            colors=colors,
            typography=typography,
        )


# Predefined advanced themes
ADVANCED_THEMES: dict[str, AdvancedTheme] = {
    "Classic": AdvancedTheme(
        name="Classic",
        description="Traditional black and white theme",
        colors=ThemeColors(
            ui_background="#FFFFFF",
            ui_panel="#F0F0F0",
            ui_button="#3B8ED0",
            ui_text="#000000",
            pdf_grid_background="#FFFFFF",
            pdf_grid_border="#000000",
            pdf_grid_letter="#000000",
            pdf_solution_highlight="#000000",
        ),
    ),
    "Minimal": AdvancedTheme(
        name="Minimal",
        description="Clean minimalist theme with soft grays",
        colors=ThemeColors(
            ui_background="#FAFAFA",
            ui_panel="#F5F5F5",
            ui_button="#757575",
            ui_text="#333333",
            pdf_grid_background="#FFFFFF",
            pdf_grid_border="#E0E0E0",
            pdf_grid_letter="#333333",
            pdf_solution_highlight="#999999",
        ),
    ),
    "Modern": AdvancedTheme(
        name="Modern",
        description="Modern theme with blue accents",
        colors=ThemeColors(
            ui_background="#FFFFFF",
            ui_panel="#F0F4F8",
            ui_button="#2563EB",
            ui_text="#1E293B",
            pdf_grid_background="#FFFFFF",
            pdf_grid_border="#2563EB",
            pdf_grid_letter="#1E293B",
            pdf_solution_highlight="#2563EB",
        ),
    ),
    "Kids": AdvancedTheme(
        name="Kids",
        description="Colorful theme for children",
        colors=ThemeColors(
            ui_background="#FFF9C4",
            ui_panel="#FFF59D",
            ui_button="#FF6B6B",
            ui_text="#333333",
            pdf_grid_background="#FFFFFF",
            pdf_grid_border="#FF6B6B",
            pdf_grid_letter="#333333",
            pdf_solution_highlight="#FF6B6B",
        ),
    ),
    "Elegant": AdvancedTheme(
        name="Elegant",
        description="Elegant theme with gold accents",
        colors=ThemeColors(
            ui_background="#FFFBF0",
            ui_panel="#F5F0E6",
            ui_button="#B8860B",
            ui_text="#2C1810",
            pdf_grid_background="#FFFBF0",
            pdf_grid_border="#B8860B",
            pdf_grid_letter="#2C1810",
            pdf_solution_highlight="#B8860B",
        ),
    ),
    "Large Print": AdvancedTheme(
        name="Large Print",
        description="High contrast theme for accessibility",
        colors=ThemeColors(
            ui_background="#FFFFFF",
            ui_panel="#FFFFFF",
            ui_button="#000000",
            ui_text="#000000",
            pdf_grid_background="#FFFFFF",
            pdf_grid_border="#000000",
            pdf_grid_letter="#000000",
            pdf_solution_highlight="#000000",
        ),
        typography=ThemeTypography(
            pdf_grid_font_size=14.0,
            pdf_words_font_size=12.0,
            pdf_solution_font_size=10.0,
        ),
    ),
}
