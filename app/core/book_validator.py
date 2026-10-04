"""Comprehensive validation system for puzzle books."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from app.models import AppConfig, Puzzle, PuzzleBook, ValidationError
from app.core.generator import validate_generated_puzzle


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Result of a validation check."""
    status: Literal["correct", "warning", "error"]
    message: str
    puzzle_number: int | None = None
    details: str = ""


@dataclass(slots=True)
class BookValidationReport:
    """Complete validation report for a puzzle book."""
    results: list[ValidationResult] = field(default_factory=list)
    
    @property
    def has_errors(self) -> bool:
        return any(r.status == "error" for r in self.results)
    
    @property
    def has_warnings(self) -> bool:
        return any(r.status == "warning" for r in self.results)
    
    @property
    def is_valid(self) -> bool:
        return not self.has_errors
    
    def add_result(self, status: Literal["correct", "warning", "error"], message: str, puzzle_number: int | None = None, details: str = "") -> None:
        self.results.append(ValidationResult(status, message, puzzle_number, details))


class BookValidator:
    """Comprehensive validator for puzzle books."""
    
    def __init__(self) -> None:
        self.report = BookValidationReport()
    
    def validate_book(self, book: PuzzleBook, config: AppConfig) -> BookValidationReport:
        """Run comprehensive validation on a puzzle book."""
        self.report = BookValidationReport()
        
        # Validate each puzzle
        for puzzle in book.puzzles:
            self._validate_puzzle(puzzle, config)
        
        # Validate overall book structure
        self._validate_book_structure(book, config)
        
        # Validate layout and margins
        self._validate_layout(book, config)
        
        # Validate solutions configuration
        self._validate_solutions_config(config)
        
        return self.report
    
    def _validate_puzzle(self, puzzle: Puzzle, config: AppConfig) -> None:
        """Validate a single puzzle."""
        # Check if puzzle is generated
        if not puzzle.is_generated:
            self.report.add_result("error", "Puzzle not generated", puzzle.number)
            return
        
        # Check for unplaced words
        if len(puzzle.placements) != len(puzzle.words):
            unplaced = len(puzzle.words) - len(puzzle.placements)
            self.report.add_result("error", f"{unplaced} word(s) not placed", puzzle.number)
        
        # Check for duplicates
        word_texts = [word.text for word in puzzle.words]
        if len(word_texts) != len(set(word_texts)):
            self.report.add_result("error", "Duplicate words found", puzzle.number)
        
        # Validate grid and coordinates
        grid_errors = validate_generated_puzzle(puzzle)
        for error in grid_errors:
            self.report.add_result("error", error.message, puzzle.number)
        
        # Check word length constraints
        for word in puzzle.words:
            if len(word.text) < config.grid.min_word_length:
                self.report.add_result("warning", f"Word '{word.text}' shorter than minimum", puzzle.number)
            if len(word.text) > config.grid.max_word_length:
                self.report.add_result("warning", f"Word '{word.text}' longer than maximum", puzzle.number)
        
        # Check if grid fits in configured size
        if puzzle.grid:
            expected_rows = config.grid.rows
            expected_cols = config.grid.columns
            actual_rows = len(puzzle.grid)
            actual_cols = len(puzzle.grid[0]) if puzzle.grid else 0
            
            if actual_rows != expected_rows or actual_cols != expected_cols:
                self.report.add_result("error", f"Grid size mismatch: expected {expected_rows}x{expected_cols}, got {actual_rows}x{actual_cols}", puzzle.number)
    
    def _validate_book_structure(self, book: PuzzleBook, config: AppConfig) -> None:
        """Validate overall book structure."""
        if not book.puzzles:
            self.report.add_result("error", "Book contains no puzzles")
            return
        
        # Check for empty puzzles
        for puzzle in book.puzzles:
            if not puzzle.words:
                self.report.add_result("error", "Puzzle has no words", puzzle.number)
        
        # Check puzzle numbering
        expected_numbers = list(range(1, len(book.puzzles) + 1))
        actual_numbers = [puzzle.number for puzzle in book.puzzles]
        if actual_numbers != expected_numbers:
            self.report.add_result("warning", "Puzzle numbering is not sequential")
    
    def _validate_layout(self, book: PuzzleBook, config: AppConfig) -> None:
        """Validate layout configuration."""
        # Check margins
        if config.page.margins.top < 0 or config.page.margins.bottom < 0:
            self.report.add_result("error", "Invalid vertical margins")
        if config.page.margins.left < 0 or config.page.margins.right < 0:
            self.report.add_result("error", "Invalid horizontal margins")
        
        # Check page size
        if config.page.width <= 0 or config.page.height <= 0:
            self.report.add_result("error", "Invalid page dimensions")
        
        # Check grid size
        if config.grid.rows < 2 or config.grid.columns < 2:
            self.report.add_result("error", "Grid too small (minimum 2x2)")
        
        # Check cell size
        if config.layout.cell_size <= 0:
            self.report.add_result("error", "Invalid cell size")
        
        # Check font sizes
        if config.layout.title_size <= 0:
            self.report.add_result("error", "Invalid title font size")
        if config.layout.grid_font_size <= 0:
            self.report.add_result("error", "Invalid grid font size")
        if config.layout.words_font_size <= 0:
            self.report.add_result("error", "Invalid words font size")
    
    def _validate_solutions_config(self, config: AppConfig) -> None:
        """Validate solutions configuration."""
        if not config.export.include_solutions:
            return
        
        # Check solutions per page
        if config.export.solutions_per_page not in (1, 2, 4):
            self.report.add_result("error", f"Invalid solutions per page: {config.export.solutions_per_page}")
        
        # Check solution spacing
        if config.export.solution_spacing < 0:
            self.report.add_result("error", "Invalid solution spacing")
        
        # Check solution cell size
        if config.export.solution_cell_size <= 0:
            self.report.add_result("error", "Invalid solution cell size")
        
        # Check solution line width
        if config.export.solution_line_width < 0:
            self.report.add_result("error", "Invalid solution line width")
        
        # Check solution font size
        if config.export.solution_font_size <= 0:
            self.report.add_result("error", "Invalid solution font size")


def validate_before_export(book: PuzzleBook, config: AppConfig) -> BookValidationReport:
    """Validate a book before export and return a detailed report."""
    validator = BookValidator()
    return validator.validate_book(book, config)
