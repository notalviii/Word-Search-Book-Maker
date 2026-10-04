"""Cover creator for puzzle books."""

from __future__ import annotations

import customtkinter as ctk

from app.models import AppConfig


class CoverCreatorDialog(ctk.CTkToplevel):
    """Dialog for creating book covers."""

    def __init__(self, parent: ctk.CTk, config: AppConfig) -> None:
        super().__init__(parent)
        self.title("Cover Creator")
        self.geometry("800x600")
        self.config = config
        
        self._build_interface()

    def _build_interface(self) -> None:
        """Build the cover creator interface."""
        # Toolbar
        toolbar = ctk.CTkFrame(self, height=50)
        toolbar.pack(fill="x", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(toolbar, text="Cover Creator", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", padx=10)
        ctk.CTkButton(toolbar, text="Save Cover", fg_color="#257B3F", hover_color="#17612D", command=self._save_cover).pack(side="right", padx=5)
        ctk.CTkButton(toolbar, text="Cancel", command=self.destroy).pack(side="right", padx=5)
        
        # Main content
        content = ctk.CTkFrame(self)
        content.pack(fill="both", expand=True, padx=10, pady=5)
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(0, weight=1)
        
        # Cover preview
        self.preview_frame = ctk.CTkFrame(content, width=300, height=450)
        self.preview_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Draw cover preview
        self._draw_cover_preview()
        
        # Sidebar for cover properties
        sidebar = ctk.CTkScrollableFrame(content, width=400)
        sidebar.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        self._build_cover_controls(sidebar)

    def _build_cover_controls(self, parent: ctk.CTkFrame) -> None:
        """Build controls for cover properties."""
        ctk.CTkLabel(parent, text="Cover Properties", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        
        # Title
        title_frame = ctk.CTkFrame(parent)
        title_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(title_frame, text="Book Title:").pack(anchor="w")
        self.cover_title = ctk.CTkEntry(title_frame)
        self.cover_title.pack(fill="x", pady=2)
        self.cover_title.insert(0, "Word Search Book")
        
        # Subtitle
        subtitle_frame = ctk.CTkFrame(parent)
        subtitle_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(subtitle_frame, text="Subtitle:").pack(anchor="w")
        self.cover_subtitle = ctk.CTkEntry(subtitle_frame)
        self.cover_subtitle.pack(fill="x", pady=2)
        self.cover_subtitle.insert(0, "100 Puzzles")
        
        # Author
        author_frame = ctk.CTkFrame(parent)
        author_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(author_frame, text="Author:").pack(anchor="w")
        self.cover_author = ctk.CTkEntry(author_frame)
        self.cover_author.pack(fill="x", pady=2)
        
        # Background color
        bg_frame = ctk.CTkFrame(parent)
        bg_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(bg_frame, text="Background Color:").pack(anchor="w")
        self.bg_color = ctk.CTkComboBox(bg_frame, values=["#FFFFFF", "#F5F5DC", "#E6E6FA", "#FFB6C1", "#98FB98"])
        self.bg_color.pack(fill="x", pady=2)
        self.bg_color.set("#FFFFFF")
        
        # Theme
        theme_frame = ctk.CTkFrame(parent)
        theme_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(theme_frame, text="Theme:").pack(anchor="w")
        self.cover_theme = ctk.CTkComboBox(theme_frame, values=["Classic", "Modern", "Kids", "Elegant"])
        self.cover_theme.pack(fill="x", pady=2)
        self.cover_theme.set("Classic")

    def _draw_cover_preview(self) -> None:
        """Draw a simple cover preview."""
        # Draw cover background
        self.preview_canvas = ctk.CTkCanvas(self.preview_frame, bg="white", width=280, height=430)
        self.preview_canvas.pack(padx=10, pady=10)
        
        # Draw cover rectangle
        self.preview_canvas.create_rectangle(10, 10, 270, 420, fill="#F5F5DC", outline="black", width=2)
        
        # Draw title
        self.preview_canvas.create_text(140, 100, text="Word Search Book", font=("Arial", 20, "bold"), fill="black")
        
        # Draw subtitle
        self.preview_canvas.create_text(140, 150, text="100 Puzzles", font=("Arial", 14), fill="gray")
        
        # Draw author
        self.preview_canvas.create_text(140, 380, text="Author Name", font=("Arial", 12), fill="black")

    def _save_cover(self) -> None:
        """Save the cover configuration."""
        # For now, just show a message
        # In a full implementation, this would save the cover as an image or PDF
        messagebox.showinfo("Cover Saved", "Cover configuration saved (image export not implemented in this version).")
        self.destroy()
