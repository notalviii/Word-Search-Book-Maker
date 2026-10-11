"""About dialog for Word Search Book Maker."""

from __future__ import annotations

import customtkinter as ctk


class AboutDialog(ctk.CTkToplevel):
    """About dialog showing application information."""

    def __init__(self, parent: ctk.CTk) -> None:
        super().__init__(parent)
        self.title("About")
        self.geometry("400x350")
        
        self._build_interface()

    def _build_interface(self) -> None:
        """Build the about dialog interface."""
        # Main content frame
        content = ctk.CTkFrame(self)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # App name
        title_label = ctk.CTkLabel(
            content,
            text="Word Search Book Maker",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(10, 5))
        
        # Version
        version_label = ctk.CTkLabel(
            content,
            text="Version 3.0.1",
            font=ctk.CTkFont(size=14)
        )
        version_label.pack(pady=5)
        
        # Separator
        separator = ctk.CTkFrame(content, height=2)
        separator.pack(fill="x", pady=15)
        
        # Creator
        creator_label = ctk.CTkLabel(
            content,
            text="Creator: not_alviii",
            font=ctk.CTkFont(size=12)
        )
        creator_label.pack(pady=5)
        
        # Description
        description = "A professional Windows desktop application for creating\nword search puzzle books and their solutions in PDF format."
        desc_label = ctk.CTkLabel(
            content,
            text=description,
            font=ctk.CTkFont(size=10),
            justify="center"
        )
        desc_label.pack(pady=10)
        
        # Core principles
        principles = "Core Principles:\n• Solution Integrity\n• No Automatic Translation\n• CSV Preservation\n• Architecture Separation"
        principles_label = ctk.CTkLabel(
            content,
            text=principles,
            font=ctk.CTkFont(size=9),
            justify="left"
        )
        principles_label.pack(pady=10)
        
        # Close button
        close_button = ctk.CTkButton(
            content,
            text="Close",
            width=100,
            command=self.destroy
        )
        close_button.pack(pady=10)
