# FastAPI + PostgreSQL + Pyroscope Profiling Demo

A comprehensive FastAPI application with PostgreSQL database and Pyroscope profiling integration, fully containerized with Docker. This project demonstrates continuous profiling capabilities and provides various endpoints to test performance monitoring.

## 🚀 Features

- **FastAPI** - Modern, fast web framework for building APIs
- **PostgreSQL** - Robust relational database
- **Pyroscope** - Continuous profiling for performance analysis
- **Docker Compose** - Complete containerized setup
- **Multiple Endpoints** - RESTful API with CRUD operations
- **CPU-Intensive Tasks** - Fibonacci and sum computations for profiling
- **Load Testing Script** - Automated script to generate profiling data

## 📋 Prerequisites

- Docker Desktop (or Docker Engine + Docker Compose)
- Python 3.11+ (optional, for local development)
- Git

## 🏗️ Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application with Pyroscope integration
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models (User, Post)
│   ├── schemas.py           # Pydantic schemas for validation
│   └── crud.py              # Database CRUD operations
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile               # FastAPI application Dockerfile
├── requirements.txt         # Python dependencies
├── init.sql                 # Database initialization script
├── test_load.py             # Load testing script
├── .dockerignore            # Docker ignore file
└── README.md                # This file
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd pyroscope-profiling
```

### 2. Start All Services

```bash
docker-compose up -d
```

This command will:
- Start PostgreSQL database container
- Start Pyroscope server container
- Build and start FastAPI application container
- Create Docker volumes for data persistence
- Set up networking between containers

### 3. Wait for Services to be Ready

The services will take a few moments to start. Check the status:

```bash
docker-compose ps
```

All services should show as "Up" and healthy.

### 4. Verify Services are Running

**FastAPI Application:**
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "pyroscope": "configured"
}
```

**Pyroscope UI:**
Open in your browser: http://localhost:4040

## 📊 API Endpoints

### Health & Info

- `GET /` - Root endpoint with API information
- `GET /health` - Health check with database connectivity test

### User Management

- `POST /users/` - Create a new user
- `GET /users/` - Get all users (with pagination: `?skip=0&limit=100`)
- `GET /users/{user_id}` - Get a specific user by ID
- `DELETE /users/{user_id}` - Delete a user by ID

### Post Management

- `POST /users/{user_id}/posts/` - Create a post for a user
- `GET /posts/` - Get all posts (with pagination: `?skip=0&limit=100`)

### CPU-Intensive Operations (for Profiling)

- `GET /compute/fibonacci/{n}` - Compute Fibonacci number (CPU intensive)
- `GET /compute/sum/{n}` - Compute sum of numbers (CPU intensive)

### Interactive API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testing the Application

### Manual Testing

1. **Create a User:**
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "full_name": "John Doe",
    "is_active": true
  }'
```

2. **Get All Users:**
```bash
curl "http://localhost:8000/users/"
```

3. **Create a Post:**
```bash
curl -X POST "http://localhost:8000/users/1/posts/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "content": "This is the content of my first post.",
    "is_published": true
  }'
```

4. **Trigger CPU-Intensive Operation:**
```bash
curl "http://localhost:8000/compute/fibonacci/35"
```

### Automated Load Testing

Run the included load testing script to generate profiling data:

```bash
# Install aiohttp for the test script
pip install aiohttp

# Run the load test
python test_load.py
```

This script will:
- Create multiple users and posts
- Generate various API requests
- Execute CPU-intensive operations
- Run mixed continuous load for 60 seconds

**Expected Duration:** ~2-3 minutes

## 🔍 Using Pyroscope for Profiling

### Access Pyroscope UI

1. Open your browser and navigate to: **http://localhost:4040**

2. **Select Application:**
   - In the application dropdown, select `fastapi-app`
   - This is the application name configured in the FastAPI app

3. **Explore Profiling Data:**
   - View flame graphs showing where CPU time is spent
   - Analyze function call stacks
   - Identify performance bottlenecks
   - Compare different time ranges

### Understanding Flame Graphs

- **Width** represents the amount of time spent in a function
- **Color** represents different functions
- **Stack depth** shows the call hierarchy
- **Click** on any segment to zoom in

### Profiling Scenarios

1. **CPU-Intensive Operations:**
   - Call `/compute/fibonacci/{n}` with n=30-35
   - Call `/compute/sum/{n}` with n=1000000-10000000
   - Watch the flame graphs show CPU usage in these endpoints

2. **Database Operations:**
   - Create, read, update users and posts
   - Observe database query patterns in profiles

3. **Mixed Load:**
   - Run the load testing script
   - See how different endpoints affect performance

### Pyroscope Features to Explore

- **Query Builder:** Filter by tags, labels, and time ranges
- **Comparison View:** Compare different time periods
- **Export:** Download profiling data for offline analysis
- **Search:** Search for specific functions or modules

## 🔧 Configuration

### Environment Variables

The FastAPI application uses these environment variables (configured in `docker-compose.yml`):

- `DATABASE_URL` - PostgreSQL connection string
- `PYROSCOPE_APP_NAME` - Application name in Pyroscope (default: `fastapi-app`)
- `PYROSCOPE_SERVER` - Pyroscope server address (default: `http://pyroscope:4040`)
- `ENVIRONMENT` - Environment name (default: `development`)

### Database Configuration

- **Host:** postgres (internal Docker network)
- **Port:** 5432
- **Database:** fastapi_db
- **Username:** postgres
- **Password:** postgres

### Pyroscope Configuration

- **Port:** 4040
- **Storage:** Persistent volume `pyroscope_data`
- **Application Name:** `fastapi-app`

## 🛠️ Development

### Running Locally (without Docker)

1. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set Environment Variables:**
```bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/fastapi_db"
export PYROSCOPE_APP_NAME="fastapi-app"
export PYROSCOPE_SERVER="http://localhost:4040"
```

3. **Start PostgreSQL and Pyroscope:**
```bash
docker-compose up -d postgres pyroscope
```

4. **Run FastAPI:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f fastapi-app
docker-compose logs -f postgres
docker-compose logs -f pyroscope
```

### Rebuilding Containers

```bash
# Rebuild and restart
docker-compose up -d --build

# Force rebuild without cache
docker-compose build --no-cache
```

### Accessing the Database

```bash
# Using Docker
docker-compose exec postgres psql -U postgres -d fastapi_db

# Or connect from local machine (if ports are exposed)
psql -h localhost -U postgres -d fastapi_db
```

## 📦 Docker Commands

### Start Services
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose stop
```

### Stop and Remove Containers
```bash
docker-compose down
```

### Stop and Remove Everything (including volumes)
```bash
docker-compose down -v
```

### View Service Status
```bash
docker-compose ps
```

### Restart a Specific Service
```bash
docker-compose restart fastapi-app
```

## 🔒 Security Notes

⚠️ **This is a demo project. For production use:**

1. Change default database passwords
2. Use environment variables for sensitive data
3. Implement proper authentication/authorization
4. Use secrets management
5. Enable HTTPS/TLS
6. Configure proper firewall rules
7. Regular security updates

## 🐛 Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose logs

# Check if ports are already in use
lsof -i :8000  # FastAPI
lsof -i :5432  # PostgreSQL
lsof -i :4040  # Pyroscope
```

### Database Connection Errors

- Ensure PostgreSQL container is healthy: `docker-compose ps`
- Check database logs: `docker-compose logs postgres`
- Verify network connectivity: Containers should be on the same network

### Pyroscope Not Receiving Data

- Check FastAPI logs for Pyroscope connection errors
- Verify `PYROSCOPE_SERVER` environment variable is correct
- Ensure Pyroscope container is accessible: `curl http://localhost:4040/health`

### Pyroscope Package Installation Issues

If you get errors like "No matching distribution found for pyroscope":

- The Python package is `pyroscope-io` (not `pyroscope`)
- Make sure you have internet connectivity
- Try: `pip install pyroscope-io --upgrade`

### Performance Issues

- Check Docker resource limits
- Increase Docker memory allocation if needed
- Monitor container resource usage: `docker stats`

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pyroscope Documentation](https://pyroscope.io/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available for educational purposes.

## 🎯 Next Steps

1. **Explore Pyroscope UI** - Analyze the profiling data
2. **Modify Endpoints** - Add your own endpoints and see them profiled
3. **Experiment with Tags** - Add custom tags to filter profiling data
4. **Production Setup** - Adapt this setup for production use
5. **Advanced Profiling** - Explore Pyroscope's advanced features like diff profiles

---

**Happy Profiling! 🔥**
