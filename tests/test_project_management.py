"""Tests for project management system."""

import os
import tempfile
import unittest
from pathlib import Path

from app.core import Project, ProjectManager, ProjectMetadata
from app.models import AppConfig, PuzzleBook, Puzzle, Word


class TestProjectManagement(unittest.TestCase):
    """Test project management functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = ProjectManager(self.temp_dir)
        self.config = AppConfig()
        self.book = PuzzleBook(
            puzzles=[
                Puzzle(
                    number=1,
                    words=[Word(text="TEST1"), Word(text="TEST2")],
                    grid=[["T", "E", "S", "T"], ["A", "B", "C", "D"]],
                )
            ]
        )

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_project(self):
        """Test creating a new project."""
        project = self.manager.create_project("test_project", self.config, self.book)
        
        self.assertIsNotNone(project)
        self.assertEqual(project.metadata.name, "test_project")
        self.assertIsNotNone(project.metadata.created_date)
        self.assertIsNotNone(project.metadata.modified_date)
        self.assertEqual(project.metadata.status, "draft")
        self.assertEqual(project.config, self.config)
        self.assertEqual(project.book, self.book)

    def test_save_and_load_project(self):
        """Test saving and loading a project."""
        project = self.manager.create_project("test_project", self.config, self.book)
        self.manager.save_project(project)
        
        loaded = self.manager.load_project("test_project")
        
        self.assertEqual(loaded.metadata.name, project.metadata.name)
        self.assertEqual(loaded.metadata.theme, project.metadata.theme)
        self.assertEqual(loaded.metadata.language, project.metadata.language)
        self.assertEqual(loaded.metadata.status, project.metadata.status)
        self.assertEqual(len(loaded.book.puzzles), len(project.book.puzzles))

    def test_list_projects(self):
        """Test listing all projects."""
        self.manager.create_project("project1", self.config, self.book)
        self.manager.create_project("project2", self.config, self.book)
        self.manager.create_project("project3", self.config, self.book)
        
        projects = self.manager.list_projects()
        
        self.assertEqual(len(projects), 3)
        self.assertIn("project1", projects)
        self.assertIn("project2", projects)
        self.assertIn("project3", projects)

    def test_delete_project(self):
        """Test deleting a project."""
        self.manager.create_project("test_project", self.config, self.book)
        
        self.manager.delete_project("test_project")
        
        projects = self.manager.list_projects()
        self.assertNotIn("test_project", projects)

    def test_duplicate_project(self):
        """Test duplicating a project."""
        original = self.manager.create_project("original", self.config, self.book)
        self.manager.save_project(original)
        
        duplicate = self.manager.duplicate_project("original", "copy")
        
        self.assertEqual(duplicate.metadata.name, "copy")
        self.assertEqual(duplicate.metadata.status, "draft")
        self.assertEqual(len(duplicate.book.puzzles), len(original.book.puzzles))
        self.assertIn("copy", self.manager.list_projects())

    def test_rename_project(self):
        """Test renaming a project."""
        self.manager.create_project("old_name", self.config, self.book)
        
        self.manager.rename_project("old_name", "new_name")
        
        projects = self.manager.list_projects()
        self.assertNotIn("old_name", projects)
        self.assertIn("new_name", projects)

    def test_load_nonexistent_project(self):
        """Test loading a project that doesn't exist."""
        with self.assertRaises(FileNotFoundError):
            self.manager.load_project("nonexistent")

    def test_delete_nonexistent_project(self):
        """Test deleting a project that doesn't exist."""
        with self.assertRaises(FileNotFoundError):
            self.manager.delete_project("nonexistent")

    def test_update_modified_date(self):
        """Test that modified date updates when project is saved."""
        project = self.manager.create_project("test_project", self.config, self.book)
        original_date = project.metadata.modified_date
        
        import time
        time.sleep(0.01)  # Small delay to ensure different timestamp
        
        self.manager.save_project(project)
        
        self.assertNotEqual(project.metadata.modified_date, original_date)

    def test_project_to_dict(self):
        """Test converting project to dictionary."""
        project = Project(
            metadata=ProjectMetadata(name="test", theme="dark", language="es"),
            config=self.config,
            book=self.book,
        )
        
        data = project.to_dict()
        
        self.assertIn("metadata", data)
        self.assertIn("config", data)
        self.assertIn("book", data)
        self.assertEqual(data["metadata"]["name"], "test")
        self.assertEqual(data["metadata"]["theme"], "dark")
        self.assertEqual(data["metadata"]["language"], "es")

    def test_project_from_dict(self):
        """Test loading project from dictionary."""
        data = {
            "metadata": {
                "name": "test",
                "theme": "dark",
                "language": "es",
                "created_date": "2024-01-01T00:00:00",
                "modified_date": "2024-01-01T00:00:00",
                "status": "ready",
                "description": "",
                "author": "",
            },
            "config": self.config.to_dict(),
            "book": self.book.to_dict(),
        }
        
        project = Project.from_dict(data)
        
        self.assertEqual(project.metadata.name, "test")
        self.assertEqual(project.metadata.theme, "dark")
        self.assertEqual(project.metadata.language, "es")
        self.assertEqual(project.metadata.status, "ready")
        self.assertEqual(len(project.book.puzzles), len(self.book.puzzles))

    def test_project_without_book(self):
        """Test project creation without a book."""
        project = self.manager.create_project("empty_project", self.config, None)
        
        self.assertIsNone(project.book)
        self.assertIsNotNone(project.metadata.created_date)
        self.assertIsNotNone(project.metadata.modified_date)


if __name__ == "__main__":
    unittest.main()
