# Contributing to FLUX API Image Generator

Thank you for your interest in contributing to FLUX API Image Generator! This document provides guidelines for contributing to the project.

## 🚀 Quick Start

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/flux-image-generator.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
5. Install in development mode: `pip install -e .`
6. Install dev dependencies: `pip install -e ".[dev]"`

## 📋 Development Setup

### Prerequisites

- Python 3.8+
- Git
- BFL.ai API key (for testing)

### Environment Setup

1. Copy the environment template:
   ```bash
   cp env.example .env
   ```

2. Add your API key to `.env`:
   ```
   BFL_API_KEY=your_api_key_here
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## 🔧 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Write your code
- Add tests for new functionality
- Update documentation if needed

### 3. Run Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src/flux_generator

# Run specific test file
python -m pytest tests/test_generator.py
```

### 4. Code Formatting

```bash
# Format code with black
black src/

# Check code style with flake8
flake8 src/

# Run both
black src/ && flake8 src/
```

### 5. Commit Your Changes

```bash
git add .
git commit -m "feat: add new feature description"
```

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 📝 Code Style

### Python Code

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Keep functions small and focused

### Commit Messages

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(generator): add support for custom prompts
fix(api): handle 403 errors properly
docs(readme): update installation instructions
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run specific test
python -m pytest tests/test_generator.py::test_create_generation_request

# Run with coverage
python -m pytest --cov=src/flux_generator --cov-report=html
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with `test_` prefix
- Use descriptive test names
- Test both success and failure cases
- Mock external API calls

Example test:

```python
import pytest
from flux_generator import FluxImageGenerator

def test_generator_initialization():
    """Test that generator initializes correctly."""
    generator = FluxImageGenerator()
    assert generator.api_key is not None
    assert generator.base_url == "https://api.bfl.ai/v1/flux-kontext-pro"
```

## 📚 Documentation

### Code Documentation

- Use docstrings for all public functions and classes
- Follow Google docstring format
- Include type hints

Example:

```python
def generate_images(self, count: int = 15) -> None:
    """Generate the specified number of images.
    
    Args:
        count: Number of images to generate. Defaults to 15.
        
    Raises:
        ValueError: If count is less than 1.
        Exception: If API request fails.
    """
```

### README Updates

- Update README.md for new features
- Add usage examples
- Update installation instructions if needed

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Description**: Clear description of the bug
2. **Steps to reproduce**: Step-by-step instructions
3. **Expected behavior**: What you expected to happen
4. **Actual behavior**: What actually happened
5. **Environment**: OS, Python version, package versions
6. **Error messages**: Full error traceback if applicable

## 💡 Feature Requests

When requesting features, please include:

1. **Description**: Clear description of the feature
2. **Use case**: Why this feature would be useful
3. **Implementation ideas**: Any thoughts on how to implement it
4. **Alternatives**: Any existing workarounds

## 🔄 Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** your changes thoroughly
5. **Update** documentation if needed
6. **Commit** with conventional commit messages
7. **Push** to your fork
8. **Create** a Pull Request
9. **Wait** for review and address feedback

### Pull Request Guidelines

- Provide a clear description of changes
- Include tests for new functionality
- Update documentation if needed
- Ensure all tests pass
- Follow the code style guidelines

## 📋 Review Process

1. **Automated checks** must pass (tests, linting)
2. **Code review** by maintainers
3. **Address feedback** if any
4. **Merge** when approved

## 🏷️ Release Process

1. **Update version** in `pyproject.toml` and `setup.py`
2. **Update changelog** if applicable
3. **Create release** on GitHub
4. **Tag** the release
5. **Publish** to PyPI (if applicable)

## 🤝 Community Guidelines

- Be respectful and inclusive
- Help others learn
- Provide constructive feedback
- Follow the project's code of conduct

## 📞 Getting Help

- **Issues**: Use GitHub Issues for bugs and feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Email**: Contact maintainers directly for sensitive issues

## 🙏 Acknowledgments

Thank you for contributing to FLUX API Image Generator! Your contributions help make this project better for everyone. 