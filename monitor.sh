#!/bin/bash

# Performance Monitor for GCT Assistant
# Shows real-time stats optimized for M4 Max

echo "📊 GCT Assistant Performance Monitor"
echo "==================================="

# Function to get process stats
get_stats() {
    # Backend stats
    BACKEND_PID=$(lsof -ti:5000 2>/dev/null | head -1)
    if [ ! -z "$BACKEND_PID" ]; then
        BACKEND_CPU=$(ps -p $BACKEND_PID -o %cpu | tail -1 | xargs)
        BACKEND_MEM=$(ps -p $BACKEND_PID -o %mem | tail -1 | xargs)
        echo "Backend (PID: $BACKEND_PID):"
        echo "  CPU: $BACKEND_CPU%"
        echo "  Memory: $BACKEND_MEM%"
    else
        echo "Backend: Not running"
    fi
    
    echo ""
    
    # Frontend stats
    FRONTEND_PID=$(lsof -ti:3000 2>/dev/null | head -1)
    if [ ! -z "$FRONTEND_PID" ]; then
        FRONTEND_CPU=$(ps -p $FRONTEND_PID -o %cpu | tail -1 | xargs)
        FRONTEND_MEM=$(ps -p $FRONTEND_PID -o %mem | tail -1 | xargs)
        echo "Frontend (PID: $FRONTEND_PID):"
        echo "  CPU: $FRONTEND_CPU%"
        echo "  Memory: $FRONTEND_MEM%"
    else
        echo "Frontend: Not running"
    fi
    
    echo ""
    
    # Database size
    if [ -f "backend/gct_data.db" ]; then
        DB_SIZE=$(du -h backend/gct_data.db | cut -f1)
        echo "Database size: $DB_SIZE"
    fi
    
    # System stats
    echo ""
    echo "System Resources:"
    echo "  Load average: $(uptime | awk -F'load average:' '{print $2}')"
    
    # M4 Max specific - check if we can get GPU usage
    if command -v powermetrics &> /dev/null; then
        echo "  Note: Run 'sudo powermetrics --samplers gpu_power' for GPU stats"
    fi
}

# Continuous monitoring
while true; do
    clear
    echo "📊 GCT Assistant Performance Monitor"
    echo "==================================="
    echo "Time: $(date)"
    echo ""
    get_stats
    echo ""
    echo "Press Ctrl+C to exit"
    sleep 2
done