# Whisper Timestamped FastAPI

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1+-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A production-ready, cross-platform Docker microservice for speech-to-text transcription with precise timestamps using [whisper-timestamped](https://github.com/linto-ai/whisper-timestamped). Perfect for building AI-powered applications that need accurate speech recognition with word-level timing information.

## ✨ Features

- **🎯 Precise Timestamps**: Word-level and segment-level timestamps with confidence scores
- **🚀 Cross-platform**: Works seamlessly on Mac, Windows, and Linux
- **⚡ GPU/CPU Flexibility**: Automatic device detection with CUDA, MPS, and CPU fallback
- **📊 Multiple Models**: Support for tiny, base, small, medium, large, large-v2, large-v3
- **🌐 Multiple Input Methods**: File upload or direct URL transcription
- **🔧 Production Ready**: RESTful API with FastAPI, health checks, and monitoring
- **🐳 Containerized**: Docker and Docker Compose ready for easy deployment
- **📈 Scalable**: Support for both CPU and GPU services

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- For GPU support: NVIDIA Docker runtime

### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/WhisperTimestampedFastAPI.git
cd WhisperTimestampedFastAPI
```

### 2. Build and Run

```bash
# CPU-only service (recommended for most users)
make run-cpu

# GPU-enabled service (requires NVIDIA Docker)
make run-gpu

# Both services
make run-both
```

### 3. Test the Service

```bash
# Check health
curl http://localhost:8000/health

# Test transcription with file upload
curl -X POST "http://localhost:8000/transcribe" \
  -F "file=@test.wav" \
  -F "model=base"

# Test transcription with URL
curl -X POST "http://localhost:8000/transcribe-url?url=https://example.com/audio.wav&model=base"
```

## 📖 API Documentation

Once the service is running, visit `http://localhost:8000/docs` for interactive API documentation.

### Core Endpoints

#### Health Check
```http
GET /health
```

#### Transcribe File
```http
POST /transcribe
```
**Parameters:**
- `file`: Audio file (mp3, wav, m4a, flac, ogg, wma, aac)
- `model`: Model size (default: "base")
- `language`: Language code (optional, auto-detect)
- `device`: Device to use (optional, auto-select)
- `verbose`: Verbose output (default: false)

#### Transcribe from URL
```http
POST /transcribe-url
```
**Parameters:**
- `url`: Audio file URL
- Same parameters as `/transcribe`

#### List Models
```http
GET /models
```

## 🎯 Demo

Here's a quick example of the transcription output:

```json
{
  "text": "So, Aaron, in your email you said you wanted to talk about the exam.",
  "language": "en",
  "segments": [
    {
      "id": 0,
      "start": 0.34,
      "end": 3.84,
      "text": "So, Aaron, in your email you said you wanted to talk about the exam.",
      "confidence": 0.926,
      "words": [
        {
          "text": "So,",
          "start": 0.34,
          "end": 0.52,
          "confidence": 0.942
        },
        {
          "text": "Aaron,",
          "start": 0.7,
          "end": 0.88,
          "confidence": 0.566
        }
      ]
    }
  ],
  "model_used": "base",
  "device_used": "cpu"
}
```

## ⚙️ Configuration

### Environment Variables

- `PORT`: Service port (default: 8000)
- `HOST`: Service host (default: 0.0.0.0)
- `CUDA_VISIBLE_DEVICES`: GPU device selection

### Docker Compose Services

- `whisper-cpu`: CPU-only service on port 8000
- `whisper-gpu`: GPU-enabled service on port 8001

## 🛠️ Development

### Local Development

```bash
# Install dependencies
make install

# Run in development mode
make dev
```

### Available Commands

```bash
make help          # Show all available commands
make build         # Build Docker image
make run-cpu       # Run CPU service
make run-gpu       # Run GPU service
make stop          # Stop all services
make logs          # Show logs
make test          # Test endpoints
make clean         # Clean up containers
```

## 🖥️ Platform-Specific Notes

### Windows
- Install Docker Desktop with WSL2 backend
- For GPU: Install NVIDIA Container Toolkit

### Mac
- Install Docker Desktop
- M1/M2 Macs: Uses Metal Performance Shaders (MPS) when available
- Intel Macs: CPU-only unless external GPU

### Linux
- Install Docker and Docker Compose
- For GPU: Install NVIDIA Container Runtime
```bash
# Ubuntu/Debian GPU setup
sudo apt install nvidia-container-runtime
sudo systemctl restart docker
```

## ⚡ Performance Optimization

### Model Selection
- `tiny`: Fastest, lowest accuracy (~39 MB)
- `base`: Good balance (~74 MB) ⭐ **Recommended**
- `small`: Better accuracy (~244 MB)
- `medium`: High accuracy (~769 MB)
- `large`: Highest accuracy (~1550 MB)

### Device Selection
- **CUDA**: Best performance with NVIDIA GPUs
- **MPS**: Good performance on Apple Silicon
- **CPU**: Fallback option, slower but universal

## 📝 API Usage Examples

### Python
```python
import requests

# Transcribe file
with open('audio.wav', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/transcribe',
        files={'file': f},
        params={'model': 'base'}
    )
result = response.json()
print(result['text'])

# Get word-level timestamps
for segment in result['segments']:
    for word in segment['words']:
        print(f"{word['start']:.2f}s - {word['end']:.2f}s: {word['text']}")
```

### cURL
```bash
# File upload
curl -X POST "http://localhost:8000/transcribe" \
  -F "file=@audio.wav" \
  -F "model=base"

# URL transcription
curl -X POST "http://localhost:8000/transcribe-url?url=https://example.com/audio.mp3&model=base"
```

### JavaScript/Node.js
```javascript
const formData = new FormData();
formData.append('file', audioFile);
formData.append('model', 'base');

fetch('http://localhost:8000/transcribe', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  console.log('Transcription:', data.text);
  console.log('Segments:', data.segments);
});
```

## 📊 Monitoring and Logging

### Health Checks
The service includes built-in health checks:
- Basic health: `GET /health`
- Device information and capabilities
- Model loading status

### Logs
```bash
# View logs
make logs

# Or with Docker Compose
docker-compose logs -f whisper-cpu
```

## 🔧 Troubleshooting

### Common Issues

1. **GPU not detected**
   - Ensure NVIDIA Docker runtime is installed
   - Check `nvidia-smi` works on host
   - Verify CUDA compatibility

2. **Model loading fails**
   - Check internet connection (models download on first use)
   - Ensure sufficient disk space
   - Check memory availability

3. **Audio format not supported**
   - Convert to supported format: mp3, wav, m4a, flac, ogg, wma, aac
   - Use FFmpeg for conversion

4. **Service fails to start**
   - Check port availability
   - Verify Docker and Docker Compose versions
   - Check system resources

### Performance Tips

- Use GPU when available for better performance
- Choose appropriate model size for your accuracy/speed needs
- For batch processing, keep the service running to avoid model reloading
- Monitor memory usage with larger models

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

This project uses [whisper-timestamped](https://github.com/linto-ai/whisper-timestamped), which is based on OpenAI Whisper. Please refer to their respective licenses for usage terms.

## 🙏 Acknowledgments

- [whisper-timestamped](https://github.com/linto-ai/whisper-timestamped) for the core transcription functionality
- [OpenAI Whisper](https://github.com/openai/whisper) for the base model
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [Docker](https://www.docker.com/) for containerization

## 📞 Support

If you encounter any issues or have questions, please:

1. Check the [troubleshooting section](#troubleshooting)
2. Search existing [issues](https://github.com/yourusername/WhisperTimestampedFastAPI/issues)
3. Create a new issue with detailed information about your problem

---

⭐ If this project helps you, please give it a star!