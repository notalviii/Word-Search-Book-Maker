"""Servicios de generación y validación del dominio."""

from .book_service import BookGenerationCancelled, BookGenerationService
from .book_validator import BookValidator, BookValidationReport, validate_before_export
from .generator import generate_puzzle, validate_generated_puzzle
from .mass_export import ExportTask, MassExporter, MassExportResult
from .project_manager import Project, ProjectManager, ProjectMetadata
from .template_manager import Template, TemplateManager
from .validation import validate_app_config

__all__ = [
    "BookGenerationCancelled", "BookGenerationService", "generate_puzzle",
    "validate_app_config", "validate_generated_puzzle",
    "BookValidator", "BookValidationReport", "validate_before_export",
    "Project", "ProjectManager", "ProjectMetadata",
    "ExportTask", "MassExporter", "MassExportResult",
    "Template", "TemplateManager",
]
