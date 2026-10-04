"""Puzzle organization overview dialog."""

from __future__ import annotations

from typing import Callable

import customtkinter as ctk

from app.models import Puzzle, PuzzleBook


class PuzzleOverviewDialog(ctk.CTkToplevel):
    """Dialog showing overview of all puzzles in a book."""

    def __init__(
        self,
        parent: ctk.CTk,
        book: PuzzleBook,
        on_select: Callable[[list[int]], None] | None = None,
        on_delete: Callable[[list[int]], None] | None = None,
        on_duplicate: Callable[[list[int]], None] | None = None,
        on_regenerate: Callable[[list[int]], None] | None = None,
    ) -> None:
        super().__init__(parent)
        self.title("Puzzle Overview")
        self.geometry("1000x700")
        self.book = book
        self.selected_puzzles: set[int] = set()
        self.on_select = on_select
        self.on_delete = on_delete
        self.on_duplicate = on_duplicate
        self.on_regenerate = on_regenerate
        
        self._build_interface()
        self._refresh_puzzle_list()

    def _build_interface(self) -> None:
        """Build the puzzle overview interface."""
        # Top toolbar
        toolbar = ctk.CTkFrame(self, height=60)
        toolbar.pack(fill="x", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(toolbar, text="Puzzle Overview", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left", padx=10)
        
        ctk.CTkButton(toolbar, text="Select All", width=100, command=self._select_all).pack(side="left", padx=5)
        ctk.CTkButton(toolbar, text="Deselect All", width=100, command=self._deselect_all).pack(side="left", padx=5)
        
        ctk.CTkButton(toolbar, text="Delete Selected", width=120, fg_color="#D22C2C", hover_color="#A32222", command=self._delete_selected).pack(side="right", padx=5)
        ctk.CTkButton(toolbar, text="Duplicate Selected", width=140, command=self._duplicate_selected).pack(side="right", padx=5)
        ctk.CTkButton(toolbar, text="Regenerate Selected", width=140, fg_color="#257B3F", hover_color="#17612D", command=self._regenerate_selected).pack(side="right", padx=5)
        
        # Scrollable puzzle grid
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Puzzle grid will be populated in _refresh_puzzle_list

    def _refresh_puzzle_list(self) -> None:
        """Refresh the puzzle list display."""
        # Clear existing widgets
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        if not self.book.puzzles:
            ctk.CTkLabel(self.scroll_frame, text="No puzzles available").pack(pady=20)
            return
        
        # Create grid layout (3 columns)
        columns = 3
        for index, puzzle in enumerate(self.book.puzzles):
            row = index // columns
            col = index % columns
            
            frame = self._create_puzzle_card(puzzle, index)
            frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        # Configure grid weights
        for i in range(columns):
            self.scroll_frame.grid_columnconfigure(i, weight=1)

    def _create_puzzle_card(self, puzzle: Puzzle, index: int) -> ctk.CTkFrame:
        """Create a card widget for a single puzzle."""
        card = ctk.CTkFrame(self.scroll_frame, border_width=2, border_color="gray")
        
        # Header with checkbox
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=5, pady=5)
        
        checkbox = ctk.CTkCheckBox(
            header,
            text=f"Puzzle {puzzle.number}",
            variable=ctk.BooleanVar(value=index in self.selected_puzzles),
            command=lambda idx=index, chk=checkbox: self._toggle_selection(idx, chk)
        )
        checkbox.pack(side="left")
        
        # Puzzle info
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(fill="x", padx=10, pady=5)
        
        word_count = len(puzzle.words)
        grid_size = f"{len(puzzle.grid)}×{len(puzzle.grid[0])}" if puzzle.grid else "Not generated"
        status = "Generated" if puzzle.is_generated else "Not generated"
        
        ctk.CTkLabel(info_frame, text=f"Words: {word_count}", anchor="w").pack(fill="x")
        ctk.CTkLabel(info_frame, text=f"Grid: {grid_size}", anchor="w").pack(fill="x")
        ctk.CTkLabel(info_frame, text=f"Status: {status}", anchor="w").pack(fill="x")
        
        # Individual action buttons
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(fill="x", padx=5, pady=(0, 5))
        
        ctk.CTkButton(button_frame, text="Regenerate", width=80, height=25, command=lambda idx=index: self._regenerate_single(idx)).pack(side="left", padx=2)
        ctk.CTkButton(button_frame, text="Duplicate", width=80, height=25, command=lambda idx=index: self._duplicate_single(idx)).pack(side="left", padx=2)
        ctk.CTkButton(button_frame, text="Delete", width=80, height=25, fg_color="#D22C2C", hover_color="#A32222", command=lambda idx=index: self._delete_single(idx)).pack(side="right", padx=2)
        
        return card

    def _toggle_selection(self, index: int, checkbox: ctk.CTkCheckBox) -> None:
        """Toggle selection of a puzzle."""
        if index in self.selected_puzzles:
            self.selected_puzzles.remove(index)
        else:
            self.selected_puzzles.add(index)

    def _select_all(self) -> None:
        """Select all puzzles."""
        self.selected_puzzles = set(range(len(self.book.puzzles)))
        self._refresh_puzzle_list()

    def _deselect_all(self) -> None:
        """Deselect all puzzles."""
        self.selected_puzzles.clear()
        self._refresh_puzzle_list()

    def _delete_selected(self) -> None:
        """Delete selected puzzles."""
        if not self.selected_puzzles:
            return
        
        if self.on_delete:
            self.on_delete(list(self.selected_puzzles))
        self.selected_puzzles.clear()
        self._refresh_puzzle_list()

    def _duplicate_selected(self) -> None:
        """Duplicate selected puzzles."""
        if not self.selected_puzzles:
            return
        
        if self.on_duplicate:
            self.on_duplicate(list(self.selected_puzzles))
        self.selected_puzzles.clear()
        self._refresh_puzzle_list()

    def _regenerate_selected(self) -> None:
        """Regenerate selected puzzles."""
        if not self.selected_puzzles:
            return
        
        if self.on_regenerate:
            self.on_regenerate(list(self.selected_puzzles))
        self.selected_puzzles.clear()
        self._refresh_puzzle_list()

    def _delete_single(self, index: int) -> None:
        """Delete a single puzzle."""
        if self.on_delete:
            self.on_delete([index])
        self._refresh_puzzle_list()

    def _duplicate_single(self, index: int) -> None:
        """Duplicate a single puzzle."""
        if self.on_duplicate:
            self.on_duplicate([index])
        self._refresh_puzzle_list()

    def _regenerate_single(self, index: int) -> None:
        """Regenerate a single puzzle."""
        if self.on_regenerate:
            self.on_regenerate([index])
        self._refresh_puzzle_list()
