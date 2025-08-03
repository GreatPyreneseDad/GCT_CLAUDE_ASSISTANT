# Local Development Guide - GCT Assistant

Optimized for Apple Silicon M4 Max MacBook Pro

## Quick Start

```bash
# One command to rule them all
make dev
```

This starts both backend and frontend with hot-reloading enabled. 
- Backend: http://localhost:5000
- Frontend: http://localhost:3000

## Features Enabled

### Performance Optimizations
- **SQLite with Write-Ahead Logging (WAL)** - Better concurrency for read/write operations
- **64MB In-Memory Cache** - Faster query performance
- **Memory-Mapped I/O** - Leverages M4 Max's fast SSD
- **Hot-Reloading** - Instant code updates without restart

### Development Features
- Single command startup
- Automatic dependency installation
- Performance monitoring
- Database management tools
- Separate backend/frontend options

## Available Commands

```bash
make dev        # Start everything (recommended)
make install    # Install dependencies
make db-init    # Initialize optimized database
make monitor    # Real-time performance monitoring
make status     # Check service status
make clean      # Clean temporary files
make reset      # Full reset and reinstall
```

## Manual Control

### Backend Only
```bash
make backend
# or
cd backend
source venv/bin/activate
python gct_backend.py
```

### Frontend Only
```bash
make frontend
# or
cd frontend
npm run dev
```

## Environment Variables

The `.env.local` file contains optimized settings:
- `WORKERS=8` - Tuned for M4 Max cores
- `SQLITE_WAL_MODE=1` - Enable Write-Ahead Logging
- `SQLITE_TEMP_STORE=memory` - Use RAM for temp operations

## Database Management

### Initialize Database
```bash
make db-init
```

### Backup Database
```bash
make db-backup
```

### Direct SQLite Access
```bash
cd backend
sqlite3 gct_data.db
.mode column
.headers on
SELECT * FROM assessments LIMIT 10;
```

## Performance Monitoring

```bash
make monitor
```

Shows real-time:
- CPU usage per service
- Memory usage
- Database size
- System load

## Troubleshooting

### Port Already in Use
```bash
# Find and kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Find and kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### Reset Everything
```bash
make reset
```

### Check Service Status
```bash
make status
```

## API Testing

### Health Check
```bash
curl http://localhost:5000/health
```

### Sample Assessment Request
```bash
curl -X POST http://localhost:5000/api/assessment/tier1 \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user",
    "responses": {
      "consistency": 0.8,
      "wisdom": 0.7,
      "energy": 0.6,
      "belonging": 0.75
    },
    "age": 30
  }'
```

## M4 Max Specific Optimizations

1. **Multi-threading**: Configured to use 8 workers
2. **Memory Usage**: Large cache sizes for SQLite
3. **I/O Performance**: Memory-mapped files up to 256MB
4. **Process Management**: Threading preferred over multiprocessing

## Development Workflow

1. Start development server: `make dev`
2. Make code changes (hot-reload active)
3. Monitor performance: `make monitor` (in new terminal)
4. Test API endpoints
5. Stop with Ctrl+C

## Next Steps

- Add GPU acceleration for ML models
- Implement Redis for caching (optional)
- Add WebSocket support for real-time features
- Configure pytest for backend testing
- Set up Jest for frontend testing