"""Servicio de alto nivel para generar libros sin depender de la interfaz."""

from __future__ import annotations

from dataclasses import replace
from typing import Callable

from app.models import GridConfig, Puzzle, PuzzleBook, ValidationError
from .generator import generate_puzzle


ProgressCallback = Callable[[int, int, str], None]
CancelCheck = Callable[[], bool]


class BookGenerationCancelled(Exception):
    """Señal explícita de cancelación, nunca produce un libro parcial válido."""


class BookGenerationService:
    def generate(
        self,
        book: PuzzleBook,
        grid_config: GridConfig,
        selected_numbers: list[int] | None = None,
        progress: ProgressCallback | None = None,
        cancelled: CancelCheck | None = None,
    ) -> PuzzleBook:
        selected = set(selected_numbers or [puzzle.number for puzzle in book.puzzles])
        originals = [puzzle for puzzle in book.puzzles if puzzle.number in selected]
        generated: list[Puzzle] = []
        for index, puzzle in enumerate(originals, start=1):
            if cancelled and cancelled():
                raise BookGenerationCancelled()
            if progress:
                progress(index - 1, len(originals), f"Generando sopa {puzzle.number} de {len(originals)}")
            result = generate_puzzle(puzzle, grid_config, cancelled)
            if result.errors:
                if cancelled and cancelled():
                    raise BookGenerationCancelled()
                joined = "\n".join(error.display() for error in result.errors)
                raise ValueError(joined)
            generated.append(result.puzzle)  # success guarantees this is Puzzle
            if progress:
                progress(index, len(originals), f"Sopa {puzzle.number} generada")
        return PuzzleBook(puzzles=generated, source_path=book.source_path)

    def generate_mass(
        self,
        book: PuzzleBook,
        grid_config: GridConfig,
        progress: ProgressCallback | None = None,
        cancelled: CancelCheck | None = None,
    ) -> tuple[PuzzleBook, list[tuple[int, list[str]]]]:
        """Generate all puzzles with failure tracking. Returns (book, failures)."""
        generated: list[Puzzle] = []
        failures: list[tuple[int, list[str]]] = []
        
        for index, puzzle in enumerate(book.puzzles, start=1):
            if cancelled and cancelled():
                raise BookGenerationCancelled()
            if progress:
                progress(index - 1, len(book.puzzles), f"Generando sopa {puzzle.number} de {len(book.puzzles)}")
            
            result = generate_puzzle(puzzle, grid_config, cancelled)
            
            if result.success:
                generated.append(result.puzzle)  # success guarantees this is Puzzle
                if progress:
                    progress(index, len(book.puzzles), f"Sopa {puzzle.number} generada")
            else:
                # Record failure but continue with other puzzles
                errors = [error.display() for error in result.errors]
                failures.append((puzzle.number, errors))
                # Keep original puzzle placeholder
                generated.append(puzzle)
                if progress:
                    progress(index, len(book.puzzles), f"Sopa {puzzle.number} falló - continuando")
        
        return PuzzleBook(puzzles=generated, source_path=book.source_path), failures

    def regenerate_single_puzzle(
        self,
        book: PuzzleBook,
        puzzle_number: int,
        grid_config: GridConfig,
        progress: ProgressCallback | None = None,
        cancelled: CancelCheck | None = None,
    ) -> PuzzleBook:
        """Regenerate a single puzzle while keeping all other puzzles unchanged."""
        # Find the puzzle to regenerate
        target_puzzle = None
        target_index = -1
        for index, puzzle in enumerate(book.puzzles):
            if puzzle.number == puzzle_number:
                target_puzzle = puzzle
                target_index = index
                break
        
        if target_puzzle is None:
            raise ValueError(f"Puzzle {puzzle_number} not found in book.")
        
        if cancelled and cancelled():
            raise BookGenerationCancelled()
        
        if progress:
            progress(0, 1, f"Regenerating puzzle {puzzle_number}")
        
        # Generate new version of the puzzle
        result = generate_puzzle(target_puzzle, grid_config, cancelled)
        
        if result.errors:
            if cancelled and cancelled():
                raise BookGenerationCancelled()
            joined = "\n".join(error.display() for error in result.errors)
            raise ValueError(joined)
        
        # Create new book with the regenerated puzzle
        new_puzzles = list(book.puzzles)
        new_puzzles[target_index] = result.puzzle  # success guarantees this is Puzzle
        
        if progress:
            progress(1, 1, f"Puzzle {puzzle_number} regenerated")
        
        return PuzzleBook(puzzles=new_puzzles, source_path=book.source_path)

    def regenerate_multiple_puzzles(
        self,
        book: PuzzleBook,
        puzzle_numbers: list[int],
        grid_config: GridConfig,
        progress: ProgressCallback | None = None,
        cancelled: CancelCheck | None = None,
    ) -> PuzzleBook:
        """Regenerate multiple selected puzzles while keeping others unchanged."""
        new_puzzles = list(book.puzzles)
        number_to_index = {puzzle.number: index for index, puzzle in enumerate(book.puzzles)}
        
        for index, puzzle_number in enumerate(puzzle_numbers, start=1):
            if cancelled and cancelled():
                raise BookGenerationCancelled()
            if progress:
                progress(index - 1, len(puzzle_numbers), f"Regenerando sopa {puzzle_number} de {len(puzzle_numbers)}")
            
            if puzzle_number not in number_to_index:
                continue
            
            target_index = number_to_index[puzzle_number]
            original_puzzle = book.puzzles[target_index]
            
            result = generate_puzzle(original_puzzle, grid_config, cancelled)
            
            if result.success:
                new_puzzles[target_index] = result.puzzle
                if progress:
                    progress(index, len(puzzle_numbers), f"Sopa {puzzle_number} regenerada")
            else:
                # Keep original if regeneration fails
                if progress:
                    progress(index, len(puzzle_numbers), f"Sopa {puzzle_number} falló - conservando original")
        
        if progress:
            progress(len(puzzle_numbers), len(puzzle_numbers), "Regeneración completada")
        
        return PuzzleBook(puzzles=new_puzzles, source_path=book.source_path)
