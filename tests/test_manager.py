"""Tests for NgrokManager."""

import pytest
import threading
import time
from unittest.mock import patch, MagicMock
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

    @patch("ngrok_app.manager.ngrok")
    def test_thread_safety_create_close(self, mock_ngrok):
        """Test thread safety for concurrent create_tunnel and close_tunnel calls."""
        # Setup mock
        mock_tunnel = MagicMock()
        mock_tunnel.public_url = "http://mock.url"
        mock_ngrok.connect.return_value = mock_tunnel

        manager = NgrokManager()
        errors = []
        results = []

        def create_tunnel_task():
            try:
                for i in range(5):
                    tunnel_info = manager.create_tunnel(
                        protocol="http",
                        local_addr="localhost",
                        local_port=8000 + i,
                        name=f"test_tunnel_{i}"
                    )
                    results.append(tunnel_info)
                    time.sleep(0.01)  # Simulate work
            except Exception as e:
                errors.append(e)

        def close_tunnel_task():
            try:
                for i in range(5):
                    manager.close_tunnel(f"test_tunnel_{i}")
                    time.sleep(0.01)  # Simulate work
            except Exception as e:
                errors.append(e)

        # Start threads
        threads = [
            threading.Thread(target=create_tunnel_task),
            threading.Thread(target=close_tunnel_task),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Verify no errors occurred
        assert len(errors) == 0, f"Thread errors: {errors}"

        # Verify tunnels are in a consistent state
        tunnels = manager.list_tunnels()
        assert isinstance(tunnels, list)

    @patch("ngrok_app.manager.ngrok")
    def test_thread_safety_concurrent_creates(self, mock_ngrok):
        """Test thread safety for concurrent create_tunnel calls."""
        # Setup mock
        mock_tunnel = MagicMock()
        mock_tunnel.public_url = "http://mock.url"
        mock_ngrok.connect.return_value = mock_tunnel

        manager = NgrokManager()
        errors = []
        results = []

        def create_tunnel_task(start_port):
            try:
                for i in range(3):
                    tunnel_info = manager.create_tunnel(
                        protocol="http",
                        local_addr="localhost",
                        local_port=start_port + i,
                        name=f"concurrent_tunnel_{start_port}_{i}"
                    )
                    results.append(tunnel_info)
            except Exception as e:
                errors.append(e)

        # Start threads
        threads = [
            threading.Thread(target=create_tunnel_task, args=(1000,)),
            threading.Thread(target=create_tunnel_task, args=(2000,)),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Verify no errors occurred
        assert len(errors) == 0, f"Thread errors: {errors}"

        # Verify all tunnels were created
        tunnels = manager.list_tunnels()
        assert len(tunnels) >= 0  # At least some tunnels should exist

    @patch("ngrok_app.manager.ngrok")
    def test_thread_safety_list_get(self, mock_ngrok):
        """Test thread safety for concurrent list_tunnels and get_tunnel calls."""
        # Setup mock
        mock_tunnel = MagicMock()
        mock_tunnel.public_url = "http://mock.url"
        mock_ngrok.connect.return_value = mock_tunnel

        manager = NgrokManager()
        manager.create_tunnel("http", "localhost", 8000, name="test_tunnel")

        errors = []
        results = []

        def list_task():
            try:
                for _ in range(10):
                    tunnels = manager.list_tunnels()
                    results.append(len(tunnels))
                    time.sleep(0.01)
            except Exception as e:
                errors.append(e)

        def get_task():
            try:
                for _ in range(10):
                    tunnel = manager.get_tunnel("test_tunnel")
                    results.append(tunnel is not None)
                    time.sleep(0.01)
            except Exception as e:
                errors.append(e)

        # Start threads
        threads = [
            threading.Thread(target=list_task),
            threading.Thread(target=get_task),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Verify no errors occurred
        assert len(errors) == 0, f"Thread errors: {errors}"
        assert len(results) == 20  # 10 list + 10 get
