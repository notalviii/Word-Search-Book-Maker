"""Visual editor for puzzle page layout with drag & drop."""

from __future__ import annotations

import customtkinter as ctk

from app.models import AppConfig


class VisualEditorDialog(ctk.CTkToplevel):
    """Visual editor for puzzle page layout with drag & drop."""

    def __init__(self, parent: ctk.CTk, config: AppConfig) -> None:
        super().__init__(parent)
        self.title("Visual Editor")
        self.geometry("900x700")
        self.config = config
        self._drag_data = {"item": None, "x": 0, "y": 0}
        
        self._build_interface()

    def _build_interface(self) -> None:
        """Build the visual editor interface."""
        # Toolbar
        toolbar = ctk.CTkFrame(self, height=50)
        toolbar.pack(fill="x", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(toolbar, text="Visual Editor", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", padx=10)
        ctk.CTkButton(toolbar, text="Apply", fg_color="#257B3F", hover_color="#17612D", command=self._apply_changes).pack(side="right", padx=5)
        ctk.CTkButton(toolbar, text="Cancel", command=self.destroy).pack(side="right", padx=5)
        
        # Main content area with canvas and sidebar
        content = ctk.CTkFrame(self)
        content.pack(fill="both", expand=True, padx=10, pady=5)
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(0, weight=1)
        
        # Canvas for visual editing
        self.canvas = ctk.CTkCanvas(content, bg="white", width=500, height=600)
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Bind mouse events for drag & drop
        self.canvas.bind("<ButtonPress-1>", self._on_drag_start)
        self.canvas.bind("<B1-Motion>", self._on_drag_motion)
        self.canvas.bind("<ButtonRelease-1>", self._on_drag_release)
        
        # Sidebar for element properties
        sidebar = ctk.CTkScrollableFrame(content, width=300)
        sidebar.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Element selection
        self._build_element_controls(sidebar)
        
        # Draw initial layout
        self._draw_layout()

    def _build_element_controls(self, parent: ctk.CTkFrame) -> None:
        """Build controls for editing element properties."""
        ctk.CTkLabel(parent, text="Element Properties", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        
        # Title controls
        title_frame = ctk.CTkFrame(parent)
        title_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(title_frame, text="Title:").pack(anchor="w")
        self.title_entry = ctk.CTkEntry(title_frame)
        self.title_entry.pack(fill="x", pady=2)
        self.title_entry.insert(0, self.config.layout.title)
        
        # Subtitle controls
        subtitle_frame = ctk.CTkFrame(parent)
        subtitle_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(subtitle_frame, text="Subtitle:").pack(anchor="w")
        self.subtitle_entry = ctk.CTkEntry(subtitle_frame)
        self.subtitle_entry.pack(fill="x", pady=2)
        self.subtitle_entry.insert(0, self.config.layout.subtitle)
        
        # Font sizes
        sizes_frame = ctk.CTkFrame(parent)
        sizes_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(sizes_frame, text="Title Size:").pack(anchor="w")
        self.title_size_entry = ctk.CTkEntry(sizes_frame)
        self.title_size_entry.pack(fill="x", pady=2)
        self.title_size_entry.insert(0, str(self.config.layout.title_size))
        
        ctk.CTkLabel(sizes_frame, text="Subtitle Size:").pack(anchor="w")
        self.subtitle_size_entry = ctk.CTkEntry(sizes_frame)
        self.subtitle_size_entry.pack(fill="x", pady=2)
        self.subtitle_size_entry.insert(0, str(self.config.layout.subtitle_size))
        
        # Grid position
        grid_frame = ctk.CTkFrame(parent)
        grid_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(grid_frame, text="Grid Position X (%):").pack(anchor="w")
        self.grid_x_entry = ctk.CTkEntry(grid_frame)
        self.grid_x_entry.pack(fill="x", pady=2)
        self.grid_x_entry.insert(0, str(self.config.layout.custom_grid_x_percent))
        
        ctk.CTkLabel(grid_frame, text="Grid Position Y (%):").pack(anchor="w")
        self.grid_y_entry = ctk.CTkEntry(grid_frame)
        self.grid_y_entry.pack(fill="x", pady=2)
        self.grid_y_entry.insert(0, str(self.config.layout.custom_grid_y_percent))
        
        # Cell size
        cell_frame = ctk.CTkFrame(parent)
        cell_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(cell_frame, text="Cell Size (pt):").pack(anchor="w")
        self.cell_size_entry = ctk.CTkEntry(cell_frame)
        self.cell_size_entry.pack(fill="x", pady=2)
        self.cell_size_entry.insert(0, str(self.config.layout.cell_size))
        
        # Word list position
        word_frame = ctk.CTkFrame(parent)
        word_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(word_frame, text="Word List Position:").pack(anchor="w")
        self.word_position = ctk.CTkComboBox(
            word_frame,
            values=["abajo", "arriba", "izquierda", "derecha"],
            command=self._on_word_position_change
        )
        self.word_position.pack(fill="x", pady=2)
        self.word_position.set(self.config.layout.words_position)

    def _draw_layout(self) -> None:
        """Draw the page layout on the canvas."""
        self.canvas.delete("all")
        
        # Draw page outline
        self.canvas.create_rectangle(10, 10, 490, 590, outline="black", width=2)
        
        # Draw title (centered at top)
        title_y = 50
        self.canvas.create_text(250, title_y, text=self.config.layout.title, font=("Arial", 14, "bold"), fill="black", tags="title")
        
        # Draw subtitle (below title)
        subtitle_y = 80
        self.canvas.create_text(250, subtitle_y, text=self.config.layout.subtitle, font=("Arial", 10), fill="gray", tags="subtitle")
        
        # Draw grid (based on position)
        grid_x = 250  # Center horizontally
        grid_y = 250  # Middle vertically
        grid_size = 200
        
        self.canvas.create_rectangle(
            grid_x - grid_size//2, grid_y - grid_size//2,
            grid_x + grid_size//2, grid_y + grid_size//2,
            outline="blue", width=2, tags="grid"
        )
        
        # Draw grid lines (simplified representation)
        for i in range(1, 10):
            # Vertical lines
            x = grid_x - grid_size//2 + (i * grid_size // 10)
            self.canvas.create_line(x, grid_y - grid_size//2, x, grid_y + grid_size//2, fill="lightblue", tags="grid")
            # Horizontal lines
            y = grid_y - grid_size//2 + (i * grid_size // 10)
            self.canvas.create_line(grid_x - grid_size//2, y, grid_x + grid_size//2, y, fill="lightblue", tags="grid")
        
        # Draw word list (below grid)
        word_y = grid_y + grid_size//2 + 30
        self.canvas.create_text(grid_x, word_y, text="Word List", font=("Arial", 10), fill="green", tags="wordlist")

    def _on_drag_start(self, event) -> None:
        """Handle drag start."""
        item = self.canvas.find_closest(event.x, event.y)
        if item:
            self._drag_data["item"] = item
            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y

    def _on_drag_motion(self, event) -> None:
        """Handle drag motion."""
        if self._drag_data["item"]:
            dx = event.x - self._drag_data["x"]
            dy = event.y - self._drag_data["y"]
            self.canvas.move(self._drag_data["item"], dx, dy)
            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y

    def _on_drag_release(self, event) -> None:
        """Handle drag release."""
        self._drag_data["item"] = None

    def _on_word_position_change(self, value: str) -> None:
        """Handle word position change."""
        self.config.layout.words_position = value
        self._draw_layout()

    def _apply_changes(self) -> None:
        """Apply changes to the configuration."""
        try:
            self.config.layout.title = self.title_entry.get()
            self.config.layout.subtitle = self.subtitle_entry.get()
            self.config.layout.title_size = float(self.title_size_entry.get())
            self.config.layout.subtitle_size = float(self.subtitle_size_entry.get())
            self.config.layout.custom_grid_x_percent = float(self.grid_x_entry.get())
            self.config.layout.custom_grid_y_percent = float(self.grid_y_entry.get())
            self.config.layout.cell_size = float(self.cell_size_entry.get())
            self.config.layout.words_position = self.word_position.get()
            
            messagebox.showinfo("Success", "Changes applied successfully.")
            self.destroy()
        except ValueError as exc:
            messagebox.showerror("Error", f"Invalid input: {exc}")
