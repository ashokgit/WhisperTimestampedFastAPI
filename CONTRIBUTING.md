# Contributing to WhisperTimestampedFastAPI

Thank you for your interest in contributing to WhisperTimestampedFastAPI! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

Before creating an issue, please:

1. **Search existing issues** to see if your problem has already been reported
2. **Check the troubleshooting section** in the README
3. **Provide detailed information** including:
   - Your operating system and version
   - Docker version
   - Steps to reproduce the issue
   - Expected vs actual behavior
   - Error messages or logs

### Suggesting Features

We welcome feature suggestions! Please:

1. **Search existing issues** to see if the feature has been requested
2. **Provide a clear description** of the feature and its benefits
3. **Include use cases** where the feature would be helpful

### Code Contributions

#### Development Setup

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/WhisperTimestampedFastAPI.git
   cd WhisperTimestampedFastAPI
   ```

3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Set up the development environment**:
   ```bash
   # Install dependencies
   make install
   
   # Run the service locally
   make dev
   ```

5. **Make your changes** and test them thoroughly

6. **Commit your changes** with clear, descriptive commit messages:
   ```bash
   git commit -m "Add feature: description of what was added"
   ```

7. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request** with a clear description of your changes

#### Code Style Guidelines

- **Python**: Follow PEP 8 style guidelines
- **Comments**: Write clear, descriptive comments
- **Documentation**: Update README.md if you add new features
- **Tests**: Add tests for new functionality when possible
- **Type hints**: Use type hints for function parameters and return values

#### Testing Your Changes

Before submitting a PR, please:

1. **Test locally** with Docker:
   ```bash
   make clean
   make run-cpu
   # Test your changes
   ```

2. **Test with different models** (tiny, base, small)

3. **Test with different audio formats** (wav, mp3, etc.)

4. **Check for any linting issues**:
   ```bash
   # If you have flake8 installed
   flake8 app.py
   ```

## 📋 Pull Request Guidelines

### Before Submitting

- [ ] Code follows the project's style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated (if applicable)
- [ ] Commit messages are clear and descriptive
- [ ] Changes are focused and atomic

### PR Description Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Other (please describe)

## Testing
Describe how you tested your changes.

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have tested my changes
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
```

## 🏗️ Project Structure

```
WhisperTimestampedFastAPI/
├── app.py                 # Main FastAPI application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose services
├── Makefile              # Build and deployment commands
├── test-client.py        # Test client for the API
├── nginx.conf            # Nginx configuration (optional)
├── README.md             # Project documentation
├── LICENSE               # MIT License
├── CONTRIBUTING.md       # This file
└── .gitignore           # Git ignore rules
```

## 🧪 Testing

### Running Tests

```bash
# Test the API endpoints
make test

# Test with the test client
python3 test-client.py --health
python3 test-client.py --file test.wav --model base
```

### Test Audio Files

You can use any audio file for testing. The service supports:
- mp3, wav, m4a, flac, ogg, wma, aac

## 🐛 Debugging

### Common Issues

1. **Service won't start**: Check Docker logs
   ```bash
   make logs
   ```

2. **Model loading fails**: Check internet connection and disk space

3. **Transcription errors**: Verify audio file format and size

### Development Tips

- Use `make dev` for local development with auto-reload
- Check the FastAPI docs at `http://localhost:8000/docs`
- Use the test client for quick API testing

## 📝 Documentation

When adding new features:

1. **Update the README.md** with new endpoints or features
2. **Add examples** in the API usage section
3. **Update the troubleshooting section** if needed
4. **Add comments** to your code explaining complex logic

## 🎯 Areas for Contribution

We're particularly interested in contributions in these areas:

- **Performance improvements**: Optimize model loading and inference
- **Additional audio formats**: Support for more audio formats
- **Better error handling**: More descriptive error messages
- **Monitoring and metrics**: Add Prometheus metrics
- **Authentication**: Add API key authentication
- **Rate limiting**: Implement request rate limiting
- **Batch processing**: Support for processing multiple files
- **Web UI**: Add a simple web interface
- **Tests**: Add comprehensive test suite

## 📞 Getting Help

If you need help with contributing:

1. **Check the README** for setup instructions
2. **Search existing issues** for similar problems
3. **Create a new issue** with detailed information
4. **Join discussions** in existing issues

## 🙏 Recognition

Contributors will be recognized in the project's README and release notes. Significant contributions may be invited to become maintainers.

Thank you for contributing to WhisperTimestampedFastAPI! 🚀 