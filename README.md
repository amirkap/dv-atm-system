# DV ATM System

A thread-safe ATM system built with FastAPI, featuring containerization and cloud deployment.

## 🏗️ Architecture Overview

The system consists of:
- **FastAPI Backend**: Thread-safe ATM operations with in-memory storage
- **Cloud-Native Design**: Optimized for single-service deployment
- **Production Ready**: Containerized and ready for cloud deployment
- **Thread Safety**: Advanced per-account locking for optimal concurrency

## 🏗️ Project Structure

```
dv-atm-system/
├── app/
│   ├── config/           # Configuration and settings
│   │   └── settings.py   # Environment and app configuration
│   ├── routers/          # API route handlers
│   │   ├── accounts.py   # All account operations (CRUD + transactions)
│   │   └── health.py     # Health check endpoints
│   ├── schemas/          # Pydantic models for validation
│   │   ├── account.py    # Account-related schemas
│   │   └── transaction.py # Transaction-related schemas
│   ├── services/         # Business logic
│   │   └── account_service.py # Unified account service with thread safety
│   ├── utils/            # Utility functions
│   │   └── logger.py     # Logging configuration
│   └── main.py           # FastAPI application entry point
├── Dockerfile           # Production container configuration
├── requirements.txt     # Python dependencies
├── tests/               # Test suite
│   ├── __init__.py      # Test package initialization
│   ├── run_tests.py     # Unified test runner
│   ├── test_api.py      # Comprehensive API tests
│   ├── test_advanced_threading.py # Thread safety and concurrency tests
│   └── test_deployment.py # Production deployment tests
├── run_tests.py         # Root test runner (convenience)
└── README.md           # This file
```

## 🚀 Features

### Core ATM Operations
- ✅ **Get Balance**: Retrieve account balance (`GET /accounts/{account_number}/balance`)
- ✅ **Withdraw Money**: Withdraw funds with insufficient funds protection (`POST /accounts/{account_number}/withdraw`)
- ✅ **Deposit Money**: Add funds to account (`POST /accounts/{account_number}/deposit`)

### Bonus Features
- ✅ **Account Creation**: Create new accounts (`POST /accounts`)
- ✅ **Account Deletion**: Remove accounts (`DELETE /accounts/{account_number}`)
- ✅ **Account Listing**: View all accounts (`GET /accounts`)
- ✅ **Health Check**: System status monitoring (`GET /health`)

### Technical Features
- 🔒 **Advanced Thread Safety**: Per-account locking for optimal concurrency
- 💾 **Memory Management**: Configurable account limits (default: 1000 accounts)
- 🐳 **Containerization**: Docker ready for cloud deployment
- 📊 **Monitoring**: Health checks and comprehensive logging
- ⚡ **High Performance**: Different accounts process concurrently
- 🏗️ **Clean Architecture**: Organized with services, routers, schemas, and config
- ☁️ **Cloud Native**: Single-service architecture optimized for modern platforms

## 🛠️ Technical Implementation

### Thread Safety
- Uses **per-account locking** for optimal concurrency
- Global lock only for account management operations
- **Same-account operations**: Properly serialized to prevent race conditions
- **Different-account operations**: Run concurrently for maximum performance
- All transactions are atomic and thread-safe

### Memory Management
- Maximum account limit: 1000 (configurable)
- HTTP 507 response when limit exceeded
- Efficient in-memory storage with UUID account numbers

### Error Handling
- **Insufficient Funds**: Proper validation with detailed error messages
- **Invalid Accounts**: 404 responses for non-existent accounts
- **Input Validation**: Pydantic schemas ensure data integrity
- **Graceful Failures**: No system crashes on invalid operations

## 📦 Installation & Setup

### Prerequisites
- Docker (for containerized deployment)
- Python 3.11+ (for local development)

### Option 1: Local Development (Recommended)

1. **Clone and navigate to the project**:
   ```bash
   git clone <repository-url>
   cd dv-atm-system
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the FastAPI server**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Verify the system is running**:
   ```bash
   curl http://localhost:8000/health
   ```

### Option 2: Docker Deployment

1. **Build Docker image**:
   ```bash
   docker build -t dv-atm-system .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8000:8000 dv-atm-system
   ```

3. **Access the API**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## 🧪 Testing

### Comprehensive Test Suite
Run all tests with the unified test runner:
```bash
# Run complete test suite (from project root)
python run_tests.py

# Or run from tests directory
python tests/run_tests.py
```

### Individual Test Scripts
```bash
# Basic API functionality tests
python tests/test_api.py

# Advanced thread safety and concurrency tests
python tests/test_advanced_threading.py

# Test deployed service
python tests/test_deployment.py https://your-deployed-url.com

# Run against deployed service with API tests
python tests/test_api.py https://your-deployed-url.com
```

### Test Coverage
- ✅ **Functional Tests**: All API endpoints and error scenarios
- ✅ **Thread Safety Tests**: Same-account serialization verification
- ✅ **Concurrency Tests**: Multi-account parallel operations
- ✅ **Performance Tests**: Timing analysis and bottleneck identification
- ✅ **Integrity Tests**: Balance consistency under concurrent load

### Manual Testing Examples

#### 1. Create an Account
```bash
curl -X POST "http://localhost:8000/accounts" \
  -H "Content-Type: application/json" \
  -d '{"initial_balance": 1000.0}'
```

#### 2. Check Balance
```bash
curl "http://localhost:8000/accounts/{account_number}/balance"
```

#### 3. Deposit Money
```bash
curl -X POST "http://localhost:8000/accounts/{account_number}/deposit" \
  -H "Content-Type: application/json" \
  -d '{"amount": 500.0}'
```

#### 4. Withdraw Money
```bash
curl -X POST "http://localhost:8000/accounts/{account_number}/withdraw" \
  -H "Content-Type: application/json" \
  -d '{"amount": 200.0}'
```

#### 5. List All Accounts
```bash
curl "http://localhost:8000/accounts"
```

#### 6. Delete Account
```bash
curl -X DELETE "http://localhost:8000/accounts/{account_number}"
```

## 📊 API Documentation

### Response Formats

#### Success Responses
```json
// Account Creation
{
  "account_number": "uuid-string",
  "balance": 1000.0,
  "message": "Account created successfully"
}

// Balance Check
{
  "account_number": "uuid-string",
  "balance": 1000.0
}

// Transaction (Withdraw/Deposit)
{
  "account_number": "uuid-string",
  "new_balance": 1500.0,
  "transaction_amount": 500.0,
  "transaction_type": "deposit",
  "timestamp": "2023-12-07T10:30:00.123456"
}
```

#### Error Responses
```json
// Insufficient Funds
{
  "detail": "Insufficient funds"
}

// Account Not Found
{
  "detail": "Account not found"
}

// Invalid Input
{
  "detail": "Amount must be positive"
}

// Account Limit Reached
{
  "detail": "Maximum number of accounts (1000) reached"
}
```

## 🔧 Configuration

### Environment Variables
- `MAX_ACCOUNTS`: Maximum number of accounts (default: 1000)
- `MAX_TRANSACTION_AMOUNT`: Maximum transaction amount (default: 10000.0)

### Application Configuration
The application can be configured via environment variables:
- All settings defined in `app/config/settings.py`
- Production-ready defaults provided
- Easy customization for different environments

## 🚀 Cloud Deployment

### Render Deployment (Recommended)

The easiest way to deploy this ATM system is using Render:

#### Quick Deploy
1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Deploy to Render"
   git push origin main
   ```

2. **Deploy on Render**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - 🌍 **Region**: Frankfurt (optimal for Middle East/Europe)
   - Render will auto-detect `render.yaml` and deploy

3. **Access Your API**:
   - Get URL: `https://your-app-name.onrender.com`
   - Test: `curl https://your-app-name.onrender.com/health`

#### Manual Configuration
If you prefer manual setup:
```bash
# Service Type: Web Service
# Runtime: Docker
# Build Command: (automatic - Docker handles build)
# Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions.

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**:
   ```bash
   # Check for processes using port 8000
   lsof -i :8000
   
   # Kill any existing FastAPI processes
   pkill -f uvicorn
   ```

2. **Memory Issues**:
   - Monitor account count via `/health` endpoint
   - Adjust `MAX_ACCOUNTS` if needed
   - Use `/accounts` endpoint to view all accounts

3. **Performance Issues**:
   - Check memory usage via `/health` endpoint
   - Monitor account count and adjust `MAX_ACCOUNTS` if needed

4. **Connection Issues**:
   - Check if FastAPI is running: `curl http://localhost:8000/health`
   - Restart the service: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

## 📈 Performance Considerations

- **Advanced Concurrency**: Per-account locking allows different accounts to process simultaneously
- **Thread Safety**: Same-account operations properly serialized, no race conditions
- **Memory Efficiency**: In-memory storage with configurable limits and automatic cleanup
- **Input Validation**: Comprehensive validation prevents invalid operations
- **Health Checks**: Automatic container restart on failure
- **Comprehensive Logging**: Detailed transaction and performance logging

## 🔒 Security Features

- **Input Validation**: Pydantic models with strict validation
- **CORS Configuration**: Proper cross-origin resource sharing setup
- **Security Headers**: FastAPI built-in security features
- **Non-root User**: Docker containers run as non-root user
- **Error Handling**: No sensitive information in error responses

## 📝 Development Notes

### Design Decisions
1. **In-Memory Storage**: As per requirements, simple and fast
2. **Per-Account Threading**: Optimal concurrency with account-level locks
3. **Unified Service Architecture**: Single account service for all operations
4. **UUID Account Numbers**: Secure and collision-resistant
5. **Single Service Design**: Cloud-native architecture optimized for modern platforms
6. **FastAPI Framework**: Modern, fast, and auto-documented APIs

### Challenges Faced & Solutions
1. **Thread Safety**: Solved with per-account locking for optimal concurrency
2. **Architecture Organization**: Refactored from over-engineered to clean, logical structure
3. **Memory Management**: Implemented configurable limits with automatic cleanup
4. **Cloud Deployment**: Optimized for single-service cloud platforms
5. **Container Design**: Lightweight Docker image with proper health checks

### Future Improvements
- Database persistence (PostgreSQL/Redis)
- Authentication and authorization
- Transaction history and audit logs
- Metrics and monitoring (Prometheus/Grafana)
- Horizontal scaling with load balancer
- Circuit breaker patterns for resilience

## 📞 Support

For questions or issues:
- Check if service is running: `curl http://localhost:8000/health`
- Run the complete test suite: `python run_tests.py`
- Run individual tests: `python tests/test_api.py` or `python tests/test_advanced_threading.py`
- Test deployments: `python tests/test_deployment.py <URL>`
- Review the API documentation: http://localhost:8000/docs

---

**Assignment completed for DoubleVerify - Junior Software Engineer Position**
