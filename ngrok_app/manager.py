"""Ngrok tunnel manager module."""

import logging
import threading
from typing import Dict, List, Optional
from pyngrok import ngrok
from .config import config

logger = logging.getLogger(__name__)
logging.basicConfig(level=config.log_level)


class NgrokManager:
    """Manages Ngrok tunnels and connections."""

    def __init__(self):
        """Initialize the Ngrok manager."""
        if config.ngrok_authtoken:
            ngrok.set_auth_token(config.ngrok_authtoken)
        self.tunnels: Dict[str, object] = {}
        self._lock = threading.Lock()

    def create_tunnel(
        self, protocol: str, local_addr: str, local_port: int, name: Optional[str] = None
    ) -> Dict:
        """
        Create a new tunnel.

        Args:
            protocol: Protocol type (http, tcp, tls)
            local_addr: Local address (localhost, 127.0.0.1)
            local_port: Local port number
            name: Optional tunnel name

        Returns:
            Dictionary containing tunnel information
        """
        try:
            tunnel = ngrok.connect((local_addr, local_port), proto=protocol)
            tunnel_name = name or f"{protocol}_{local_port}"
            with self._lock:
                self.tunnels[tunnel_name] = tunnel

            tunnel_info = {
                "name": tunnel_name,
                "public_url": tunnel.public_url,
                "protocol": protocol,
                "local_addr": local_addr,
                "local_port": local_port,
                "status": "active",
            }

            logger.info(f"Tunnel created: {tunnel_name} -> {tunnel.public_url}")
            return tunnel_info
        except Exception as e:
            logger.error(f"Failed to create tunnel: {str(e)}")
            raise

    def close_tunnel(self, name: str) -> bool:
        """
        Close a tunnel.

        Args:
            name: Tunnel name

        Returns:
            True if successful, False otherwise
        """
        try:
            with self._lock:
                if name in self.tunnels:
                    ngrok.disconnect(self.tunnels[name].public_url)
                    del self.tunnels[name]
                    logger.info(f"Tunnel closed: {name}")
                    return True
                return False
        except Exception as e:
            logger.error(f"Failed to close tunnel: {str(e)}")
            return False

    def list_tunnels(self) -> List[Dict]:
        """
        List all active tunnels.

        Returns:
            List of tunnel information dictionaries
        """
        with self._lock:
            tunnels_list = []
            for name, tunnel in self.tunnels.items():
                tunnels_list.append(
                    {
                        "name": name,
                        "public_url": tunnel.public_url,
                        "status": "active",
                    }
                )
            return tunnels_list

    def get_tunnel(self, name: str) -> Optional[Dict]:
        """
        Get tunnel information.

        Args:
            name: Tunnel name

        Returns:
            Tunnel information or None if not found
        """
        with self._lock:
            if name in self.tunnels:
                tunnel = self.tunnels[name]
                return {
                    "name": name,
                    "public_url": tunnel.public_url,
                    "status": "active",
                }
            return None

    def close_all(self) -> None:
        """Close all tunnels."""
        try:
            with self._lock:
                ngrok.kill()
                self.tunnels.clear()
            logger.info("All tunnels closed")
        except Exception as e:
            logger.error(f"Failed to close all tunnels: {str(e)}")