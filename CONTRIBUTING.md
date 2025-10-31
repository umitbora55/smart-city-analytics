# Contributing Guide

Thank you for your interest in contributing to Smart City Analytics!

## Development Workflow

### 1. Fork and Clone
```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/smart-city-analytics.git
cd smart-city-analytics
```

### 2. Create a Branch
```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or a bugfix branch
git checkout -b bugfix/issue-description
```

### 3. Make Changes

- Write clean, readable code
- Follow PEP 8 for Python code
- Add comments for complex logic
- Update documentation if needed

### 4. Test Your Changes
```bash
# Run tests (will be added in Phase 2)
pytest tests/

# Check code quality
flake8 src/
black src/
```

### 5. Commit Your Changes
```bash
# Stage your changes
git add .

# Commit with descriptive message
git commit -m "feat: Add feature description

- Detailed explanation of changes
- Why the change was needed
- Any breaking changes"
```

### Commit Message Convention

Follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

### 6. Push and Create Pull Request
```bash
# Push to your fork
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Code Style

### Python
- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use docstrings for functions and classes

### Documentation
- Clear and concise
- Include code examples
- Update relevant docs with code changes

## Project Structure Guidelines

- Keep components modular
- Each service should be independently testable
- Use configuration files for environment-specific settings
- Avoid hardcoded values

## Testing

- Write unit tests for new features
- Ensure integration tests pass
- Aim for >80% code coverage

## Questions?

Open an issue for discussion before starting major changes.

---

**Happy Contributing!**
