"""Mass export functionality for generating multiple PDFs."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable

from app.core import BookGenerationService
from app.models import AppConfig, PuzzleBook


@dataclass(slots=True)
class ExportTask:
    """A single export task."""
    name: str
    book: PuzzleBook
    config: AppConfig
    output_path: str
    status: str = "pending"  # pending | processing | completed | failed
    error: str = ""
    timestamp: str = ""


@dataclass(slots=True)
class MassExportResult:
    """Result of mass export operation."""
    total_tasks: int
    completed: int
    failed: int
    failures: list[tuple[str, str]] = field(default_factory=list)  # (task_name, error)
    start_time: str = ""
    end_time: str = ""


class MassExporter:
    """Handles mass export of multiple PDFs."""

    def __init__(self) -> None:
        self.service = BookGenerationService()
        self.tasks: list[ExportTask] = []
        self._cancel_requested = False

    def create_tasks_from_projects(
        self,
        projects: list[tuple[str, PuzzleBook, AppConfig]],
        output_dir: str,
    ) -> list[ExportTask]:
        """Create export tasks from multiple projects."""
        tasks = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for name, book, config in projects:
            output_path = os.path.join(output_dir, f"{name}_{timestamp}.pdf")
            task = ExportTask(
                name=name,
                book=book,
                config=config,
                output_path=output_path,
                timestamp=datetime.now().isoformat(),
            )
            tasks.append(task)
        
        self.tasks = tasks
        return tasks

    def create_tasks_from_variations(
        self,
        book: PuzzleBook,
        base_config: AppConfig,
        variations: list[tuple[str, AppConfig]],
        output_dir: str,
    ) -> list[ExportTask]:
        """Create export tasks from configuration variations."""
        tasks = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for variation_name, config in variations:
            output_path = os.path.join(output_dir, f"{variation_name}_{timestamp}.pdf")
            task = ExportTask(
                name=variation_name,
                book=book,
                config=config,
                output_path=output_path,
                timestamp=datetime.now().isoformat(),
            )
            tasks.append(task)
        
        self.tasks = tasks
        return tasks

    def execute(
        self,
        progress_callback: Callable[[int, int, str], None] | None = None,
        cancel_check: Callable[[], bool] | None = None,
    ) -> MassExportResult:
        """Execute all export tasks."""
        result = MassExportResult(
            total_tasks=len(self.tasks),
            completed=0,
            failed=0,
            start_time=datetime.now().isoformat(),
        )
        
        for index, task in enumerate(self.tasks):
            if cancel_check and cancel_check():
                result.end_time = datetime.now().isoformat()
                return result
            
            task.status = "processing"
            if progress_callback:
                progress_callback(index, len(self.tasks), f"Exporting {task.name}...")
            
            try:
                # Ensure output directory exists
                os.makedirs(os.path.dirname(task.output_path), exist_ok=True)
                
                # Generate PDF
                from app.pdf import PdfBookRenderer
                renderer = PdfBookRenderer()
                renderer.set_language(task.config.language)
                renderer.render_book(task.book, task.config, task.output_path)
                
                task.status = "completed"
                result.completed += 1
            except Exception as exc:
                task.status = "failed"
                task.error = str(exc)
                result.failed += 1
                result.failures.append((task.name, str(exc)))
            
            if progress_callback:
                progress_callback(index + 1, len(self.tasks), f"Completed {task.name}")
        
        result.end_time = datetime.now().isoformat()
        return result

    def cancel(self) -> None:
        """Request cancellation of the export."""
        self._cancel_requested = True

    def is_cancelled(self) -> bool:
        """Check if cancellation was requested."""
        return self._cancel_requested
