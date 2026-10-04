"""Enhanced book preview with full navigation."""

from __future__ import annotations

from typing import Any

import customtkinter as ctk
from PIL import Image

from app.models import AppConfig, Puzzle, PuzzleBook
from app.pdf import PdfBookRenderer
from app.pdf.preview import render_preview


class BookPreviewWindow(ctk.CTkToplevel):
    """Enhanced book preview with full navigation."""

    def __init__(self, parent: ctk.CTk, book: PuzzleBook, config: AppConfig) -> None:
        super().__init__(parent)
        self.title("Book Preview")
        self.geometry("1000x800")
        self.book = book
        self.config = config
        self.renderer = PdfBookRenderer()
        self.renderer.set_language(config.language)
        
        self.current_page = 0
        self.total_pages = 0
        self.preview_pages: list[tuple[Any, bool]] = []  # (puzzle_or_group, is_solution)
        self._zoom_level = 1.0
        self._preview_image: ctk.CTkImage | None = None
        
        self._build_interface()
        self._calculate_pages()
        self._show_page(0)

    def _build_interface(self) -> None:
        """Build the preview interface."""
        # Top toolbar
        toolbar = ctk.CTkFrame(self, height=50)
        toolbar.pack(fill="x", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(toolbar, text="Book Preview", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", padx=10)
        
        # Navigation buttons
        ctk.CTkButton(toolbar, text="First", width=70, command=lambda: self._show_page(0)).pack(side="left", padx=2)
        ctk.CTkButton(toolbar, text="Previous", width=70, command=lambda: self._show_page(self.current_page - 1)).pack(side="left", padx=2)
        ctk.CTkButton(toolbar, text="Next", width=70, command=lambda: self._show_page(self.current_page + 1)).pack(side="left", padx=2)
        ctk.CTkButton(toolbar, text="Last", width=70, command=lambda: self._show_page(self.total_pages - 1)).pack(side="left", padx=2)
        
        # Page jump
        ctk.CTkLabel(toolbar, text="Go to:").pack(side="left", padx=(10, 5))
        self.page_entry = ctk.CTkEntry(toolbar, width=60)
        self.page_entry.pack(side="left", padx=2)
        self.page_entry.bind("<Return>", self._on_page_jump)
        ctk.CTkButton(toolbar, text="Go", width=40, command=self._on_page_jump).pack(side="left", padx=2)
        
        # Zoom controls
        ctk.CTkButton(toolbar, text="−", width=35, command=lambda: self._change_zoom(-0.1)).pack(side="right", padx=2)
        ctk.CTkButton(toolbar, text="+", width=35, command=lambda: self._change_zoom(0.1)).pack(side="right", padx=2)
        self.zoom_label = ctk.CTkLabel(toolbar, text="100%")
        self.zoom_label.pack(side="right", padx=5)
        
        # Page counter
        self.page_counter = ctk.CTkLabel(toolbar, text="Page 0 of 0")
        self.page_counter.pack(side="right", padx=10)
        
        # Preview area
        self.preview_frame = ctk.CTkScrollableFrame(self)
        self.preview_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.preview_label = ctk.CTkLabel(self.preview_frame, text="", anchor="center")
        self.preview_label.pack(expand=True, padx=20, pady=20)
        
        # Page type indicator
        self.page_type_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(weight="bold"))
        self.page_type_label.pack(pady=5)

    def _calculate_pages(self) -> None:
        """Calculate the total number of pages and their types."""
        if not self.book.puzzles:
            self.total_pages = 0
            return
        
        # Get page sequence from renderer
        page_sequence = self.renderer.page_sequence(self.book, self.config)
        self.preview_pages = page_sequence
        self.total_pages = len(page_sequence)

    def _show_page(self, page_num: int) -> None:
        """Show a specific page."""
        if not self.preview_pages or page_num < 0 or page_num >= self.total_pages:
            return
        
        self.current_page = page_num
        page_content, is_solution = self.preview_pages[page_num]
        
        self.page_counter.configure(text=f"Page {page_num + 1} of {self.total_pages}")
        self.page_entry.delete(0, "end")
        self.page_entry.insert(0, str(page_num + 1))
        
        # Determine page type
        if is_solution:
            page_type = f"Solution Page ({len(page_content)} solution(s))"
        else:
            page_type = f"Puzzle Page - Puzzle {page_content[0].number}"
        self.page_type_label.configure(text=page_type)
        
        # Render preview
        try:
            if is_solution and len(page_content) > 1:
                # Multiple solutions on one page (2 or 4)
                self._render_multi_solution_page(page_content)
            else:
                # Single puzzle or single solution
                puzzle = page_content[0] if page_content else None
                if puzzle:
                    image: Image.Image = render_preview(puzzle, self.config, is_solution, max_width=800)
                    self._display_image(image)
        except Exception as exc:
            self.preview_label.configure(image=None, text=f"Error rendering page:\n{exc}")

    def _render_multi_solution_page(self, puzzles: list[Puzzle]) -> None:
        """Render a page with multiple solutions (2 or 4)."""
        # For simplicity, render the first solution as a preview
        # A full implementation would composite all solutions
        if puzzles:
            image: Image.Image = render_preview(puzzles[0], self.config, True, max_width=600)
            self._display_image(image)
            self.preview_label.configure(text=f"Preview: {len(puzzles)} solutions on this page (showing first)")

    def _display_image(self, image: Image.Image) -> None:
        """Display an image in the preview area."""
        # Apply zoom
        if self._zoom_level != 1.0:
            new_size = (int(image.width * self._zoom_level), int(image.height * self._zoom_level))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        self._preview_image = ctk.CTkImage(light_image=image, dark_image=image, size=image.size)
        self.preview_label.configure(image=self._preview_image, text="")

    def _change_zoom(self, delta: float) -> None:
        """Change zoom level."""
        new_zoom = max(0.5, min(2.0, self._zoom_level + delta))
        self._zoom_level = new_zoom
        self.zoom_label.configure(text=f"{int(new_zoom * 100)}%")
        self._show_page(self.current_page)

    def _on_page_jump(self, event: Any = None) -> None:
        """Handle page jump input."""
        try:
            page_num = int(self.page_entry.get()) - 1
            if 0 <= page_num < self.total_pages:
                self._show_page(page_num)
            else:
                messagebox.showwarning("Invalid Page", f"Page number must be between 1 and {self.total_pages}")
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid page number")
