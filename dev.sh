#!/bin/bash

# GCT Assistant Local Development Launcher
# Optimized for Apple Silicon M4 Max
# Single command to start everything with hot-reloading

echo "🚀 Starting GCT Assistant in Local Development Mode"
echo "=================================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}Shutting down services...${NC}"
    kill $(jobs -p) 2>/dev/null
    exit
}

# Set up trap for cleanup
trap cleanup INT TERM

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    cd ..
else
    echo -e "${GREEN}✓ Python virtual environment found${NC}"
fi

# Check if node_modules exists for frontend
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}Installing frontend dependencies...${NC}"
    cd frontend
    npm install
    cd ..
else
    echo -e "${GREEN}✓ Frontend dependencies found${NC}"
fi

# Export environment variables
export FLASK_ENV=development
export FLASK_DEBUG=1
export NEXT_PUBLIC_API_URL=http://localhost:5000

# Start Backend
echo -e "\n${BLUE}Starting Flask Backend on port 5000...${NC}"
cd backend
source venv/bin/activate
python gct_backend.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo -e "${YELLOW}Waiting for backend to initialize...${NC}"
sleep 3

# Check if backend is running
if curl -s http://localhost:5000/health > /dev/null; then
    echo -e "${GREEN}✓ Backend is running${NC}"
else
    echo -e "${RED}✗ Backend failed to start${NC}"
    exit 1
fi

# Start Frontend
echo -e "\n${BLUE}Starting Next.js Frontend on port 3000...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Display startup information
echo -e "\n${GREEN}=================================================="
echo "🎉 GCT Assistant is running!"
echo "=================================================="
echo -e "${NC}"
echo "Backend API: http://localhost:5000"
echo "Frontend UI: http://localhost:3000"
echo ""
echo "Features enabled:"
echo "  ✓ Hot-reloading for both backend and frontend"
echo "  ✓ SQLite with Write-Ahead Logging"
echo "  ✓ Optimized for Apple Silicon"
echo "  ✓ CORS configured for local development"
echo ""
echo "Press Ctrl+C to stop all services"
echo -e "${GREEN}==================================================${NC}\n"

# Keep script running
wait