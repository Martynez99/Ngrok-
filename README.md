# Ngrok Project

A comprehensive solution for exposing local services to the internet using Ngrok tunneling technology.

## Features

- 🚀 Easy tunnel creation and management
- 🔒 Secure connections with authentication
- 📊 Real-time monitoring and logging
- 🔄 Automatic reconnection handling
- 📱 REST API for programmatic control

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from ngrok_app import NgrokManager

manager = NgrokManager()
tunnel = manager.create_tunnel('http', 'localhost', 8000)
print(f"Tunnel URL: {tunnel.public_url}")
```

## Configuration

Create a `.env` file in the project root:

```env
NGROK_AUTHTOKEN=your_auth_token_here
LOG_LEVEL=INFO
```

## API Documentation

See [API.md](./docs/API.md) for detailed endpoint documentation.

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](./CONTRIBUTING.md).