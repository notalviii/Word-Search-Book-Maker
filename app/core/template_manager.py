"""Template system for reusable configurations."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from app.models import AppConfig


@dataclass(slots=True)
class Template:
    """A reusable template configuration."""
    name: str
    description: str = ""
    category: str = "general"  # general | puzzle | solution | cover
    config: AppConfig = field(default_factory=AppConfig)
    created_date: str = ""
    modified_date: str = ""
    
    def __post_init__(self) -> None:
        from datetime import datetime
        if not self.created_date:
            self.created_date = datetime.now().isoformat()
        if not self.modified_date:
            self.modified_date = datetime.now().isoformat()
    
    def to_dict(self) -> dict[str, Any]:
        """Convert template to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "config": self.config.to_dict(),
            "created_date": self.created_date,
            "modified_date": self.modified_date,
        }
    
    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Template":
        """Load template from dictionary."""
        config = AppConfig.from_dict(raw.get("config", {}))
        return cls(
            name=raw.get("name", ""),
            description=raw.get("description", ""),
            category=raw.get("category", "general"),
            config=config,
            created_date=raw.get("created_date", ""),
            modified_date=raw.get("modified_date", ""),
        )


class TemplateManager:
    """Manages template operations."""
    
    def __init__(self, templates_dir: str | Path = "templates") -> None:
        self.templates_dir = Path(templates_dir)
        self.templates_dir.mkdir(parents=True, exist_ok=True)
    
    def save_template(self, template: Template) -> None:
        """Save a template to file."""
        from datetime import datetime
        template.modified_date = datetime.now().isoformat()
        
        filename = f"{template.name}.json"
        file_path = self.templates_dir / filename
        file_path.write_text(json.dumps(template.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    
    def load_template(self, name: str) -> Template:
        """Load a template from file."""
        file_path = self.templates_dir / f"{name}.json"
        if not file_path.exists():
            raise FileNotFoundError(f"Template '{name}' not found")
        raw = json.loads(file_path.read_text(encoding="utf-8"))
        return Template.from_dict(raw)
    
    def list_templates(self, category: str | None = None) -> list[str]:
        """List all templates, optionally filtered by category."""
        templates = []
        for file_path in self.templates_dir.glob("*.json"):
            raw = json.loads(file_path.read_text(encoding="utf-8"))
            if category is None or raw.get("category") == category:
                templates.append(file_path.stem)
        return sorted(templates)
    
    def delete_template(self, name: str) -> None:
        """Delete a template."""
        file_path = self.templates_dir / f"{name}.json"
        if file_path.exists():
            file_path.unlink()
        else:
            raise FileNotFoundError(f"Template '{name}' not found")
    
    def create_template_from_config(
        self,
        name: str,
        config: AppConfig,
        category: str = "general",
        description: str = "",
    ) -> Template:
        """Create a template from current configuration."""
        template = Template(
            name=name,
            description=description,
            category=category,
            config=config,
        )
        self.save_template(template)
        return template
    
    def apply_template(self, name: str, config: AppConfig) -> AppConfig:
        """Apply a template to a configuration."""
        template = self.load_template(name)
        # Merge template config with existing config
        template_dict = template.config.to_dict()
        existing_dict = config.to_dict()
        
        # Deep merge
        def merge_dicts(base: dict[str, Any], update: dict[str, Any]) -> dict[str, Any]:
            result = base.copy()
            for key, value in update.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = merge_dicts(result[key], value)
                else:
                    result[key] = value
            return result
        
        merged_dict = merge_dicts(existing_dict, template_dict)
        return AppConfig.from_dict(merged_dict)
