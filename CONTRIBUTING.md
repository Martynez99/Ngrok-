# Contributing to Ngrok Project

Thank you for considering contributing to this project! Here are some guidelines:

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a virtual environment: `python -m venv venv`
4. Activate it: `source venv/bin/activate` (Unix) or `venv\Scripts\activate` (Windows)
5. Install dependencies: `pip install -r requirements.txt`

## Making Changes

1. Create a new branch for your feature: `git checkout -b feature/my-feature`
2. Make your changes
3. Write tests for new functionality
4. Run tests: `pytest`
5. Commit with clear messages: `git commit -m "Add feature X"`
6. Push to your fork
7. Create a Pull Request

## Code Style

- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions focused and testable

## Testing

All new features must include tests. Run the test suite with:

```bash
pytest
```

## Reporting Issues

When reporting bugs, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior

Thank you for contributing!