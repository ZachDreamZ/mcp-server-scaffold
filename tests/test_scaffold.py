"""Tests for mcp-server-scaffold."""
from pathlib import Path
import tempfile
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from mcp_scaffold.cli import scaffold


def test_scaffold_creates_project():
    """Scaffolding a server creates all expected files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir)
        package = scaffold("test-server", "A test server", "0.1.0", output / "test-server")
        
        assert package == "test_server"
        assert (output / "test-server" / "src" / "test_server" / "server.py").exists()
        assert (output / "test-server" / "README.md").exists()
        assert (output / "test-server" / "pyproject.toml").exists()
        assert (output / "test-server" / ".gitignore").exists()
        assert (output / "test-server" / "tests" / "test_server.py").exists()
        
        server_py = (output / "test-server" / "src" / "test_server" / "server.py").read_text()
        assert "test-server" in server_py
        assert "0.1.0" in server_py


def test_scaffold_package_naming():
    """Package names correctly convert hyphens to underscores."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir)
        package = scaffold("my-cool-server", "desc", "1.0.0", output / "my-cool-server")
        assert package == "my_cool_server"
