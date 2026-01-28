"""Tests for MCP file upload tool."""
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock

import pytest


class TestMCPNotebookAddFile:
    """Test the notebook_add_file MCP tool."""

    def test_tool_exists(self):
        """Test that notebook_add_file tool is registered."""
        from notebooklm_tools.mcp import server

        # Check if function exists
        assert hasattr(server, 'notebook_add_file')

    def test_tool_calls_client_add_file(self):
        """Test that the MCP tool calls client.add_file correctly."""
        from notebooklm_tools.mcp import server

        # Create a test file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Test content")
            temp_path = f.name

        try:
            # Mock the client
            mock_client = Mock()
            mock_client.add_file = Mock(return_value={"id": "test-source-id", "title": "test.txt"})

            # Mock get_client to return our mock
            with patch.object(server, 'get_client', return_value=mock_client):
                # Get the wrapped function's original function
                tool_func = server.notebook_add_file
                # FastMCP wraps the function, access via fn attribute
                result = tool_func.fn(
                    notebook_id="test-notebook-123",
                    file_path=temp_path
                )

            # Verify client.add_file was called with correct args
            mock_client.add_file.assert_called_once_with("test-notebook-123", temp_path)

            # Verify return value
            assert result["id"] == "test-source-id"
            assert result["title"] == "test.txt"
        finally:
            Path(temp_path).unlink()

    def test_tool_docstring(self):
        """Test that the tool has correct documentation."""
        from notebooklm_tools.mcp import server

        tool_func = server.notebook_add_file
        # FastMCP tool should have description
        assert hasattr(tool_func, 'description')
        assert "resumable upload" in tool_func.description.lower()
