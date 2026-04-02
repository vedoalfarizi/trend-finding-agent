# ============================================================================
# FastAPI Sequential Agent - Makefile
# ============================================================================
# Commands for environment setup, Docker operations, and Cloud Run deployment
# ============================================================================

# Configuration Variables
PROJECT_ID := engineering-trend-scout
SERVICE_NAME := sequential-agent-api
IMAGE_NAME := sequential-agent
IMAGE_TAG := latest
REGION := us-central1
PORT := 8080
VENV_DIR := venv
PYTHON := python3

# Derived variables
DOCKER_REGISTRY := gcr.io
DOCKER_IMAGE_URL := $(DOCKER_REGISTRY)/$(PROJECT_ID)/$(IMAGE_NAME):$(IMAGE_TAG)
VENV_BIN := $(VENV_DIR)/bin

# Color output
.DEFAULT_GOAL := help
CYAN := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
NC := \033[0m # No Color

# ============================================================================
# HELP TARGET
# ============================================================================

.PHONY: help
help: ## Display this help message
	@echo "$(CYAN)FastAPI Sequential Agent - Available Commands$(NC)"
	@echo ""
	@echo "$(YELLOW)Environment Setup:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '(venv|install)' | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(CYAN)make %-30s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Docker Operations:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '(docker)' | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(CYAN)make %-30s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Cloud Run Deployment:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '(deploy|push)' | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(CYAN)make %-30s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Development:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '(run|test|lint)' | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(CYAN)make %-30s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Utility:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '(clean|info)' | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(CYAN)make %-30s$(NC) %s\n", $$1, $$2}'
	@echo ""

# ============================================================================
# ENVIRONMENT & SETUP TARGETS
# ============================================================================

.PHONY: venv-create
venv-create: ## Create Python virtual environment
	@echo "$(GREEN)Creating Python virtual environment...$(NC)"
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "$(GREEN)✅ Virtual environment created at $(VENV_DIR)$(NC)"

.PHONY: venv-activate
venv-activate: ## Activate Python virtual environment
	@echo "$(GREEN)To activate the virtual environment, run:$(NC)"
	@echo "$(CYAN)  source $(VENV_BIN)/activate$(NC)"

.PHONY: venv-deactivate
venv-deactivate: ## Deactivate Python virtual environment
	@echo "$(GREEN)To deactivate the virtual environment, run:$(NC)"
	@echo "$(CYAN)  deactivate$(NC)"

.PHONY: install
install: ## Install dependencies (requires activated venv in shell)
	@echo "$(GREEN)Installing dependencies...$(NC)"
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "$(RED)❌ Virtual environment not activated!$(NC)"; \
		echo "$(YELLOW)First run: source $(VENV_BIN)/activate$(NC)"; \
		exit 1; \
	fi
	pip install --upgrade pip
	pip install -r requirements.txt
	@echo "$(GREEN)✅ Dependencies installed successfully$(NC)"

.PHONY: install-dev
install-dev: ## Install dependencies including dev tools
	@echo "$(GREEN)Installing dependencies with dev tools...$(NC)"
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "$(RED)❌ Virtual environment not activated!$(NC)"; \
		echo "$(YELLOW)First run: source $(VENV_BIN)/activate$(NC)"; \
		exit 1; \
	fi
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install pytest pytest-asyncio black flake8
	@echo "$(GREEN)✅ Dependencies installed successfully$(NC)"

# ============================================================================
# DOCKER TARGETS
# ============================================================================

.PHONY: docker-build
docker-build: ## Build Docker image locally
	@echo "$(GREEN)Building Docker image: $(IMAGE_NAME):$(IMAGE_TAG)$(NC)"
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .
	@echo "$(GREEN)✅ Docker image built successfully$(NC)"
	@echo "  Image: $(IMAGE_NAME):$(IMAGE_TAG)"

.PHONY: docker-build-prod
docker-build-prod: ## Build Docker image with production flags
	@echo "$(GREEN)Building production Docker image...$(NC)"
	docker build \
		--build-arg BUILDKIT_INLINE_CACHE=1 \
		-t $(IMAGE_NAME):$(IMAGE_TAG) \
		.
	@echo "$(GREEN)✅ Production Docker image built$(NC)"

.PHONY: docker-run
docker-run: ## Run Docker container locally
	@echo "$(GREEN)Running Docker container...$(NC)"
	docker run \
		--rm \
		-p $(PORT):$(PORT) \
		-e GOOGLE_CLOUD_PROJECT=$(PROJECT_ID) \
		-e GOOGLE_CLOUD_LOCATION=$(REGION) \
		--name $(SERVICE_NAME) \
		$(IMAGE_NAME):$(IMAGE_TAG)

.PHONY: docker-run-detached
docker-run-detached: ## Run Docker container in detached mode
	@echo "$(GREEN)Running Docker container in detached mode...$(NC)"
	docker run \
		-d \
		-p $(PORT):$(PORT) \
		-e GOOGLE_CLOUD_PROJECT=$(PROJECT_ID) \
		-e GOOGLE_CLOUD_LOCATION=$(REGION) \
		--name $(SERVICE_NAME) \
		$(IMAGE_NAME):$(IMAGE_TAG)
	@echo "$(GREEN)✅ Container started: $(SERVICE_NAME)$(NC)"
	@echo "$(CYAN)  Access at: http://localhost:$(PORT)$(NC)"
	@echo "$(CYAN)  View logs: docker logs -f $(SERVICE_NAME)$(NC)"

.PHONY: docker-stop
docker-stop: ## Stop running Docker container
	@echo "$(GREEN)Stopping Docker container...$(NC)"
	docker stop $(SERVICE_NAME) || true
	@echo "$(GREEN)✅ Container stopped$(NC)"

.PHONY: docker-logs
docker-logs: ## View Docker container logs
	docker logs -f $(SERVICE_NAME)

.PHONY: docker-shell
docker-shell: ## Open shell in running container
	docker exec -it $(SERVICE_NAME) /bin/bash

.PHONY: docker-tag
docker-tag: ## Tag Docker image for registry (requires PROJECT_ID set)
	@echo "$(GREEN)Tagging Docker image for GCR...$(NC)"
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) $(DOCKER_IMAGE_URL)
	@echo "$(GREEN)✅ Image tagged: $(DOCKER_IMAGE_URL)$(NC)"

.PHONY: docker-push
docker-push: docker-tag ## Push Docker image to Google Container Registry
	@echo "$(GREEN)Pushing Docker image to GCR...$(NC)"
	@echo "$(YELLOW)Make sure you're authenticated: gcloud auth configure-docker$(NC)"
	docker push $(DOCKER_IMAGE_URL)
	@echo "$(GREEN)✅ Image pushed to GCR$(NC)"
	@echo "  URL: $(DOCKER_IMAGE_URL)"

.PHONY: docker-clean
docker-clean: ## Remove local Docker image
	@echo "$(GREEN)Removing Docker image: $(IMAGE_NAME):$(IMAGE_TAG)$(NC)"
	docker rmi $(IMAGE_NAME):$(IMAGE_TAG) || true
	docker rmi $(DOCKER_IMAGE_URL) || true
	@echo "$(GREEN)✅ Docker image removed$(NC)"

# ============================================================================
# CLOUD RUN DEPLOYMENT TARGETS
# ============================================================================

.PHONY: gcloud-auth
gcloud-auth: ## Authenticate with Google Cloud and configure Docker
	@echo "$(GREEN)Authenticating with Google Cloud...$(NC)"
	gcloud auth login
	gcloud config set project $(PROJECT_ID)
	gcloud auth configure-docker
	@echo "$(GREEN)✅ Authentication configured$(NC)"

.PHONY: deploy
deploy: docker-push ## Deploy to Cloud Run (builds, tags, pushes, and deploys image)
	@echo "$(GREEN)Deploying to Cloud Run...$(NC)"
	gcloud run deploy $(SERVICE_NAME) \
		--image $(DOCKER_IMAGE_URL) \
		--platform managed \
		--region $(REGION) \
		--allow-unauthenticated \
		--port $(PORT) \
		--memory 512Mi \
		--cpu 1 \
		--timeout 3600 \
		--max-instances 100 \
		--set-env-vars GOOGLE_CLOUD_PROJECT=$(PROJECT_ID),GOOGLE_CLOUD_LOCATION=$(REGION)
	@echo "$(GREEN)✅ Deployment to Cloud Run completed$(NC)"

.PHONY: deploy-authenticated
deploy-authenticated: docker-push ## Deploy to Cloud Run with authentication required
	@echo "$(GREEN)Deploying to Cloud Run (authenticated)...$(NC)"
	gcloud run deploy $(SERVICE_NAME) \
		--image $(DOCKER_IMAGE_URL) \
		--platform managed \
		--region $(REGION) \
		--no-allow-unauthenticated \
		--port $(PORT) \
		--memory 512Mi \
		--cpu 1 \
		--timeout 3600 \
		--max-instances 100 \
		--set-env-vars GOOGLE_CLOUD_PROJECT=$(PROJECT_ID),GOOGLE_CLOUD_LOCATION=$(REGION)
	@echo "$(GREEN)✅ Deployment to Cloud Run completed (authenticated)$(NC)"

.PHONY: deploy-view
deploy-view: ## View deployed service on Cloud Run
	@echo "$(GREEN)Cloud Run Service Details:$(NC)"
	gcloud run services describe $(SERVICE_NAME) --region $(REGION)

.PHONY: deploy-logs
deploy-logs: ## View Cloud Run service logs
	@echo "$(GREEN)Cloud Run Service Logs:$(NC)"
	gcloud run services log read $(SERVICE_NAME) --region $(REGION) --limit 50

.PHONY: deploy-delete
deploy-delete: ## Delete Cloud Run service
	@echo "$(RED)Deleting Cloud Run service: $(SERVICE_NAME)$(NC)"
	gcloud run services delete $(SERVICE_NAME) --region $(REGION)
	@echo "$(GREEN)✅ Service deleted$(NC)"

# ============================================================================
# DEVELOPMENT TARGETS
# ============================================================================

.PHONY: run
run: ## Run FastAPI server locally (requires activated venv)
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "$(RED)❌ Virtual environment not activated!$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Starting FastAPI server...$(NC)"
	uvicorn main:app --reload --host 0.0.0.0 --port $(PORT)

.PHONY: test
test: ## Run tests (requires activated venv with pytest)
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "$(RED)❌ Virtual environment not activated!$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Running tests...$(NC)"
	pytest -v --tb=short

.PHONY: lint
lint: ## Run linting (requires activated venv with flake8)
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "$(RED)❌ Virtual environment not activated!$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Running linting...$(NC)"
	flake8 . --exclude venv,__pycache__ --max-line-length=100

.PHONY: format
format: ## Format code with Black (requires activated venv)
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "$(RED)❌ Virtual environment not activated!$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Formatting code...$(NC)"
	black . --exclude venv
	@echo "$(GREEN)✅ Code formatted$(NC)"

# ============================================================================
# UTILITY TARGETS
# ============================================================================

.PHONY: info
info: ## Display configuration variables
	@echo "$(CYAN)Project Configuration:$(NC)"
	@echo "  $(GREEN)PROJECT_ID:$(NC)        $(PROJECT_ID)"
	@echo "  $(GREEN)SERVICE_NAME:$(NC)      $(SERVICE_NAME)"
	@echo "  $(GREEN)IMAGE_NAME:$(NC)        $(IMAGE_NAME)"
	@echo "  $(GREEN)IMAGE_TAG:$(NC)         $(IMAGE_TAG)"
	@echo "  $(GREEN)REGION:$(NC)            $(REGION)"
	@echo "  $(GREEN)PORT:$(NC)              $(PORT)"
	@echo "  $(GREEN)VENV_DIR:$(NC)          $(VENV_DIR)"
	@echo ""
	@echo "$(CYAN)Docker Configuration:$(NC)"
	@echo "  $(GREEN)Registry:$(NC)          $(DOCKER_REGISTRY)"
	@echo "  $(GREEN)Full Image URL:$(NC)    $(DOCKER_IMAGE_URL)"

.PHONY: clean
clean: docker-stop docker-clean ## Clean up local Docker containers and images
	@echo "$(GREEN)Cleaning up build artifacts...$(NC)"
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✅ Cleanup complete$(NC)"

.PHONY: clean-all
clean-all: clean docker-clean ## Remove all generated files including venv
	@echo "$(RED)Removing virtual environment...$(NC)"
	rm -rf $(VENV_DIR)
	@echo "$(GREEN)✅ Full cleanup complete$(NC)"

.PHONY: doctor
doctor: ## Run diagnostic checks
	@echo "$(CYAN)Running diagnostic checks...$(NC)"
	@echo ""
	@echo "$(YELLOW)Python:$(NC)"
	@which python3 || echo "$(RED)❌ Python3 not found$(NC)"
	@python3 --version || echo "$(RED)❌ Python version check failed$(NC)"
	@echo ""
	@echo "$(YELLOW)Docker:$(NC)"
	@which docker || echo "$(RED)❌ Docker not found$(NC)"
	@docker --version || echo "$(RED)❌ Docker version check failed$(NC)"
	@echo ""
	@echo "$(YELLOW)Google Cloud SDK:$(NC)"
	@which gcloud || echo "$(RED)❌ gcloud CLI not found$(NC)"
	@gcloud --version 2>&1 | head -1 || echo "$(RED)❌ gcloud version check failed$(NC)"
	@echo ""
	@echo "$(YELLOW)Virtual Environment:$(NC)"
	@if [ -d "$(VENV_DIR)" ]; then echo "$(GREEN)✅ Virtual environment exists$(NC)"; else echo "$(RED)❌ Virtual environment not found$(NC)"; fi
	@echo ""
	@echo "$(GREEN)✅ Diagnostic checks complete$(NC)"

# ============================================================================
# QUICK START TARGETS
# ============================================================================

.PHONY: quick-start
quick-start: venv-create venv-activate ## Quick start: create virtual environment (run: source venv/bin/activate then make install)
	@echo ""
	@echo "$(GREEN)Quick start setup complete!$(NC)"
	@echo ""
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "  1. Activate environment: $(CYAN)source $(VENV_BIN)/activate$(NC)"
	@echo "  2. Install dependencies: $(CYAN)make install$(NC)"
	@echo "  3. Run locally: $(CYAN)make run$(NC)"
	@echo "  4. Or build & run with Docker: $(CYAN)make docker-build && make docker-run$(NC)"

.PHONY: quick-deploy
quick-deploy: docker-build docker-push deploy ## Quick deploy: build, tag, push, and deploy to Cloud Run
	@echo ""
	@echo "$(GREEN)✅ Quick deploy complete!$(NC)"

# ============================================================================
# .PHONY DECLARATIONS
# ============================================================================

.PHONY: all
all: help

# Make targets non-file-dependent
.PHONY: $(shell grep -E '^[a-zA-Z_-]+:' Makefile | sed 's/:.*//g')
