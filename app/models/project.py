"""Project models for Word Search Book Maker."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from app.models import AppConfig, PuzzleBook


@dataclass(slots=True)
class ProjectMetadata:
    """Metadata for a project."""
    name: str = ""
    theme: str = "light"
    language: str = "en"
    created_date: str = ""
    modified_date: str = ""
    status: str = "draft"  # draft | ready | exported
    description: str = ""
    author: str = ""


@dataclass(slots=True)
class Project:
    """Complete project with book and configuration."""
    metadata: ProjectMetadata = field(default_factory=ProjectMetadata)
    config: AppConfig = field(default_factory=AppConfig)
    book: PuzzleBook | None = None
    
    def __post_init__(self) -> None:
        """Set creation date if not set."""
        if not self.metadata.created_date:
            self.metadata.created_date = datetime.now().isoformat()
        if not self.metadata.modified_date:
            self.metadata.modified_date = datetime.now().isoformat()
    
    def update_modified_date(self) -> None:
        """Update the modified date to now."""
        self.metadata.modified_date = datetime.now().isoformat()
    
    def to_dict(self) -> dict[str, Any]:
        """Convert project to dictionary for saving."""
        return {
            "metadata": {
                "name": self.metadata.name,
                "theme": self.metadata.theme,
                "language": self.metadata.language,
                "created_date": self.metadata.created_date,
                "modified_date": self.metadata.modified_date,
                "status": self.metadata.status,
                "description": self.metadata.description,
                "author": self.metadata.author,
            },
            "config": self.config.to_dict(),
            "book": self.book.to_dict() if self.book else None,
        }
    
    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Project":
        """Load project from dictionary."""
        metadata_raw = raw.get("metadata", {})
        metadata = ProjectMetadata(**metadata_raw)
        config = AppConfig.from_dict(raw.get("config", {}))
        
        book = None
        if raw.get("book"):
            book = PuzzleBook.from_dict(raw["book"])
        
        return cls(metadata=metadata, config=config, book=book)
