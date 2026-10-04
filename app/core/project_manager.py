"""Project management service for Word Search Book Maker."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
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
            "metadata": asdict(self.metadata),
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


class ProjectManager:
    """Manages project operations."""
    
    def __init__(self, projects_dir: str | Path = "projects") -> None:
        self.projects_dir = Path(projects_dir)
        self.projects_dir.mkdir(parents=True, exist_ok=True)
    
    def create_project(self, name: str, config: AppConfig, book: PuzzleBook | None = None) -> Project:
        """Create a new project."""
        metadata = ProjectMetadata(name=name)
        project = Project(metadata=metadata, config=config, book=book)
        self.save_project(project)
        return project
    
    def save_project(self, project: Project) -> None:
        """Save a project to file."""
        project.update_modified_date()
        filename = f"{project.metadata.name or 'unnamed'}.json"
        file_path = self.projects_dir / filename
        file_path.write_text(json.dumps(project.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    
    def load_project(self, name: str) -> Project:
        """Load a project from file."""
        file_path = self.projects_dir / f"{name}.json"
        if not file_path.exists():
            raise FileNotFoundError(f"Project '{name}' not found")
        raw = json.loads(file_path.read_text(encoding="utf-8"))
        return Project.from_dict(raw)
    
    def list_projects(self) -> list[str]:
        """List all project names."""
        projects = []
        for file_path in self.projects_dir.glob("*.json"):
            projects.append(file_path.stem)
        return sorted(projects)
    
    def delete_project(self, name: str) -> None:
        """Delete a project."""
        file_path = self.projects_dir / f"{name}.json"
        if file_path.exists():
            file_path.unlink()
        else:
            raise FileNotFoundError(f"Project '{name}' not found")
    
    def duplicate_project(self, name: str, new_name: str) -> Project:
        """Duplicate a project with a new name."""
        original = self.load_project(name)
        original.metadata.name = new_name
        original.metadata.created_date = datetime.now().isoformat()
        original.metadata.modified_date = datetime.now().isoformat()
        original.metadata.status = "draft"
        self.save_project(original)
        return original
    
    def rename_project(self, old_name: str, new_name: str) -> None:
        """Rename a project."""
        old_path = self.projects_dir / f"{old_name}.json"
        new_path = self.projects_dir / f"{new_name}.json"
        if old_path.exists():
            old_path.rename(new_path)
        else:
            raise FileNotFoundError(f"Project '{old_name}' not found")
