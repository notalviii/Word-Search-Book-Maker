"""Modelos de dominio independientes de la interfaz."""

from .domain import (
    AppConfig,
    Coordinate,
    DIFFICULTY_PRESETS,
    ExportConfig,
    GenerationResult,
    GridConfig,
    LayoutConfig,
    MarginConfig,
    PageConfig,
    PAGE_PRESETS,
    Puzzle,
    PuzzleBook,
    ValidationError,
    Word,
    WordPlacement,
    word_list_rows,
)
from .project import Project, ProjectMetadata

__all__ = [
    "AppConfig", "Coordinate", "DIFFICULTY_PRESETS", "ExportConfig", "GenerationResult", "GridConfig", "PAGE_PRESETS",
    "LayoutConfig", "MarginConfig", "PageConfig", "Puzzle", "PuzzleBook",
    "ValidationError", "Word", "WordPlacement",
    "word_list_rows",
]
