"""Tests for NgrokManager."""

import pytest
from ngrok_app import NgrokManager


class TestNgrokManager:
    """Test suite for NgrokManager."""

    @pytest.fixture
    def manager(self):
        """Create a manager instance."""
        return NgrokManager()

    def test_manager_initialization(self, manager):
        """Test manager initializes without errors."""
        assert manager is not None
        assert isinstance(manager.tunnels, dict)

    def test_list_tunnels_empty(self, manager):
        """Test listing tunnels when none exist."""
        tunnels = manager.list_tunnels()
        assert isinstance(tunnels, list)
        assert len(tunnels) == 0

    def test_get_tunnel_not_found(self, manager):
        """Test getting a non-existent tunnel."""
        result = manager.get_tunnel("nonexistent")
        assert result is None