# Whisper Timestamped Microservice Makefile

# Variables
IMAGE_NAME = whisper-timestamped
SERVICE_NAME = whisper-service
CPU_PORT = 8000
GPU_PORT = 8001

# Default target
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  build          - Build Docker image"
	@echo "  run-cpu        - Run CPU-only service"
	@echo "  run-gpu        - Run GPU-enabled service (requires NVIDIA Docker)"
	@echo "  run-both       - Run both CPU and GPU services"
	@echo "  stop           - Stop all services"
	@echo "  logs           - Show service logs"
	@echo "  test           - Test the service endpoints"
	@echo "  clean          - Clean up containers and images"
	@echo "  health         - Check service health"

# Build Docker image
.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

# Run CPU-only service
.PHONY: run-cpu
run-cpu: build
	docker-compose up -d whisper-cpu

# Run GPU service (requires nvidia-docker)
.PHONY: run-gpu
run-gpu: build
	docker-compose --profile gpu up -d whisper-gpu

# Run both services
.PHONY: run-both
run-both: build
	docker-compose --profile gpu up -d

# Stop all services
.PHONY: stop
stop:
	docker-compose down

# Show logs
.PHONY: logs
logs:
	docker-compose logs -f

# Test endpoints
.PHONY: test
test:
	@echo "Testing CPU service health..."
	@curl -s http://localhost:$(CPU_PORT)/health | python -m json.tool || echo "CPU service not available"
	@echo "\nTesting GPU service health (if running)..."
	@curl -s http://localhost:$(GPU_PORT)/health | python -m json.tool || echo "GPU service not available"

# Check health
.PHONY: health
health:
	@echo "CPU Service Health:"
	@docker-compose ps whisper-cpu
	@echo "\nGPU Service Health:"
	@docker-compose ps whisper-gpu

# Clean up
.PHONY: clean
clean:
	docker-compose down -v
	docker rmi $(IMAGE_NAME) || true
	docker system prune -f

# Development mode (with auto-reload)
.PHONY: dev
dev:
	python app.py

# Install dependencies locally (for development)
.PHONY: install
install:
	pip install -r requirements.txt
	pip install git+https://github.com/linto-ai/whisper-timestamped.git

# Run tests with sample audio
.PHONY: test-transcribe
test-transcribe:
	@echo "Testing transcription endpoint..."
	@echo "Note: This requires a sample audio file. Create one or use the URL endpoint instead."
	@curl -X POST "http://localhost:$(CPU_PORT)/transcribe-url" \
		-H "Content-Type: application/json" \
		-d '{"url": "https://www.soundjay.com/misc/sounds/bell-ringing-05.wav"}' || echo "Test failed"