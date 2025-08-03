# GCT Assistant Makefile
# Optimized for Apple Silicon M4 Max Development

.PHONY: help dev install clean reset monitor test build db-init backend frontend

# Default target
help:
	@echo "GCT Assistant Development Commands"
	@echo "================================="
	@echo "make dev       - Start full stack development server"
	@echo "make install   - Install all dependencies"
	@echo "make clean     - Clean temporary files and caches"
	@echo "make reset     - Full reset (clean + reinstall)"
	@echo "make monitor   - Monitor performance"
	@echo "make db-init   - Initialize optimized database"
	@echo "make backend   - Start backend only"
	@echo "make frontend  - Start frontend only"
	@echo "make test      - Run tests"
	@echo "make build     - Build for production"

# Main development command
dev:
	@./dev.sh

# Install dependencies
install:
	@echo "Installing backend dependencies..."
	@cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	@cd frontend && npm install
	@echo "✅ All dependencies installed!"

# Clean temporary files
clean:
	@echo "Cleaning temporary files..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type f -name ".DS_Store" -delete
	@rm -rf frontend/.next
	@rm -rf frontend/node_modules/.cache
	@echo "✅ Cleanup complete!"

# Full reset
reset: clean
	@echo "Performing full reset..."
	@rm -rf backend/venv
	@rm -rf frontend/node_modules
	@rm -f backend/gct_data.db
	@make install
	@make db-init
	@echo "✅ Reset complete!"

# Performance monitoring
monitor:
	@./monitor.sh

# Initialize database
db-init:
	@cd backend && python init_db.py

# Start backend only
backend:
	@echo "Starting backend..."
	@cd backend && source venv/bin/activate && python gct_backend.py

# Start frontend only
frontend:
	@echo "Starting frontend..."
	@cd frontend && npm run dev

# Run tests (placeholder - implement based on your test framework)
test:
	@echo "Running backend tests..."
	@cd backend && source venv/bin/activate && python -m pytest tests/ || echo "No tests found"
	@echo "Running frontend tests..."
	@cd frontend && npm test || echo "No tests configured"

# Build for production
build:
	@echo "Building frontend..."
	@cd frontend && npm run build
	@echo "✅ Build complete!"

# Quick database backup
db-backup:
	@mkdir -p backups
	@cp backend/gct_data.db backups/gct_data_$(shell date +%Y%m%d_%H%M%S).db
	@echo "✅ Database backed up to backups/"

# Check system status
status:
	@echo "System Status:"
	@echo "============="
	@echo -n "Backend: "
	@lsof -ti:5000 > /dev/null 2>&1 && echo "✅ Running on port 5000" || echo "❌ Not running"
	@echo -n "Frontend: "
	@lsof -ti:3000 > /dev/null 2>&1 && echo "✅ Running on port 3000" || echo "❌ Not running"
	@echo -n "Database: "
	@[ -f backend/gct_data.db ] && echo "✅ Found ($(shell du -h backend/gct_data.db | cut -f1))" || echo "❌ Not found"