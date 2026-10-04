from __future__ import annotations

import unittest

from app.core.book_service import BookGenerationService
from app.core.book_validator import BookValidator, validate_before_export
from app.core.generator import generate_puzzle
from app.models import AppConfig, GridConfig, Puzzle, PuzzleBook, Word
from app.pdf.layout import get_solution_layout, solution_cell_rects


class V3FeaturesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = AppConfig()
        self.config.grid = GridConfig(rows=12, columns=12, seed=42, max_attempts=200)
        self.service = BookGenerationService()
    
    def _create_test_puzzle(self, number: int = 1) -> Puzzle:
        words = [Word(f"WORD{i}") for i in range(5)]
        result = generate_puzzle(Puzzle(number, words), self.config.grid)
        self.assertTrue(result.success, result.errors)
        assert result.puzzle is not None
        return result.puzzle
    
    def test_solutions_per_page_1(self) -> None:
        """Test 1 solution per page layout."""
        cols, rows = get_solution_layout(1)
        self.assertEqual(cols, 1)
        self.assertEqual(rows, 1)
    
    def test_solutions_per_page_2(self) -> None:
        """Test 2 solutions per page layout."""
        cols, rows = get_solution_layout(2)
        self.assertEqual(cols, 1)
        self.assertEqual(rows, 2)
    
    def test_solutions_per_page_4(self) -> None:
        """Test 4 solutions per page layout (2x2 grid)."""
        cols, rows = get_solution_layout(4)
        self.assertEqual(cols, 2)
        self.assertEqual(rows, 2)
    
    def test_solutions_per_page_default(self) -> None:
        """Test default layout for invalid solutions per page."""
        cols, rows = get_solution_layout(3)
        self.assertEqual(cols, 2)
        self.assertEqual(rows, 2)
    
    def test_solution_cell_rects_with_different_counts(self) -> None:
        """Test solution cell rectangles with different occupied counts."""
        puzzle = self._create_test_puzzle()
        book = PuzzleBook([puzzle])
        
        # Test with 1 solution
        cells_1 = solution_cell_rects(self.config, occupied=1)
        self.assertEqual(len(cells_1), 1)
        
        # Test with 2 solutions
        self.config.export.solutions_per_page = 2
        cells_2 = solution_cell_rects(self.config, occupied=2)
        self.assertEqual(len(cells_2), 2)
        
        # Test with 4 solutions
        self.config.export.solutions_per_page = 4
        cells_4 = solution_cell_rects(self.config, occupied=4)
        self.assertEqual(len(cells_4), 4)
    
    def test_mass_generation_with_failures(self) -> None:
        """Test mass generation that continues on failures."""
        # Create a book with one impossible puzzle (too long for grid)
        words = [Word("WAYTOOLONGWORD")]
        impossible_puzzle = Puzzle(1, words)
        
        # Create valid puzzles
        valid_puzzles = [self._create_test_puzzle(i) for i in range(2, 5)]
        
        book = PuzzleBook([impossible_puzzle] + valid_puzzles)
        
        generated_book, failures = self.service.generate_mass(book, self.config.grid)
        
        # Should have at least one failure (the impossible puzzle)
        self.assertGreater(len(failures), 0)
        self.assertEqual(failures[0][0], 1)
        
        # Should have generated all puzzles (with placeholders for failures)
        self.assertEqual(len(generated_book.puzzles), 4)
    
    def test_regenerate_multiple_puzzles(self) -> None:
        """Test regenerating multiple selected puzzles."""
        puzzles = [self._create_test_puzzle(i) for i in range(1, 6)]
        book = PuzzleBook(puzzles)
        
        # Save original grids
        original_grids = [p.grid for p in book.puzzles]
        
        # Regenerate puzzles 2 and 4
        new_book = self.service.regenerate_multiple_puzzles(
            book, [2, 4], self.config.grid
        )
        
        # Check that puzzles 2 and 4 changed
        self.assertIsNot(new_book.puzzles[1].grid, original_grids[1])
        self.assertIsNot(new_book.puzzles[3].grid, original_grids[3])
        
        # Check that other puzzles remained unchanged
        self.assertIs(new_book.puzzles[0].grid, original_grids[0])
        self.assertIs(new_book.puzzles[2].grid, original_grids[2])
        self.assertIs(new_book.puzzles[4].grid, original_grids[4])
    
    def test_difficulty_presets(self) -> None:
        """Test difficulty preset application."""
        from app.models import DIFFICULTY_PRESETS
        
        self.assertIn("fácil", DIFFICULTY_PRESETS)
        self.assertIn("medio", DIFFICULTY_PRESETS)
        self.assertIn("difícil", DIFFICULTY_PRESETS)
        self.assertIn("experto", DIFFICULTY_PRESETS)
        
        # Apply easy preset
        config = GridConfig()
        config.apply_difficulty_preset("fácil")
        self.assertEqual(config.difficulty, "fácil")
        self.assertEqual(config.rows, 10)
        self.assertEqual(config.columns, 10)
        self.assertFalse(config.allow_intersections)
    
    def test_validation_empty_book(self) -> None:
        """Test validation of empty book."""
        book = PuzzleBook([])
        report = validate_before_export(book, self.config)
        
        self.assertFalse(report.is_valid)
        self.assertTrue(report.has_errors)
        self.assertTrue(any("no puzzles" in r.message.lower() for r in report.results))
    
    def test_validation_unplaced_words(self) -> None:
        """Test validation detects unplaced words."""
        puzzle = Puzzle(1, [Word("WORD1"), Word("WORD2")])
        puzzle.grid = [["W", "O", "R", "D"]]
        puzzle.placements = []  # No placements
        book = PuzzleBook([puzzle])
        
        report = validate_before_export(book, self.config)
        
        self.assertFalse(report.is_valid)
        # Check that there's an error related to unplaced words
        error_messages = [r.message for r in report.results if r.status == "error"]
        self.assertTrue(len(error_messages) > 0, f"No errors found in report: {[r.message for r in report.results]}")
    
    def test_validation_invalid_solutions_per_page(self) -> None:
        """Test validation detects invalid solutions per page."""
        puzzle = self._create_test_puzzle()
        book = PuzzleBook([puzzle])
        
        self.config.export.solutions_per_page = 3  # Invalid
        report = validate_before_export(book, self.config)
        
        self.assertFalse(report.is_valid)
        self.assertTrue(any("solutions per page" in r.message.lower() for r in report.results))
    
    def test_page_presets_v3(self) -> None:
        """Test v3.0.0 page presets."""
        from app.models import PAGE_PRESETS
        
        self.assertIn("A4", PAGE_PRESETS)
        self.assertIn("Letter", PAGE_PRESETS)
        self.assertIn("6 × 9 in", PAGE_PRESETS)
        self.assertIn("7 × 10 in", PAGE_PRESETS)  # New in v3.0.0
        self.assertIn("8.5 × 11 in", PAGE_PRESETS)
    
    def test_enhanced_export_config(self) -> None:
        """Test enhanced export configuration."""
        self.config.export.solutions_per_page = 4
        self.config.export.solution_spacing = 12.0
        self.config.export.solution_cell_size = 20.0
        self.config.export.show_puzzle_number_in_solution = True
        self.config.export.show_title_in_solution = False
        
        # Serialize and deserialize
        config_dict = self.config.to_dict()
        loaded_config = AppConfig.from_dict(config_dict)
        
        self.assertEqual(loaded_config.export.solutions_per_page, 4)
        self.assertEqual(loaded_config.export.solution_spacing, 12.0)
        self.assertEqual(loaded_config.export.solution_cell_size, 20.0)
        self.assertTrue(loaded_config.export.show_puzzle_number_in_solution)
        self.assertFalse(loaded_config.export.show_title_in_solution)


if __name__ == "__main__":
    unittest.main()
