# 🚀 Deployment & Startup Instructions

## Project: Student Management System (Full-Stack)
**Version:** 2.0.0  
**Status:** ✅ Production Ready

---

## System Requirements

### Minimum Requirements
- **OS:** Windows 10+, Linux, macOS
- **Python:** 3.8 or higher
- **RAM:** 2GB minimum (4GB recommended)
- **Storage:** 500MB free space
- **Database:** MySQL 8.0+
- **Port:** 8000 (or custom)

### Recommended Setup
- **OS:** Windows Server 2019+ or Ubuntu 20.04+
- **Python:** 3.11 (latest stable)
- **RAM:** 4GB or more
- **MySQL:** 8.0.33+
- **Network:** Stable internet connection

---

## Pre-Installation Checklist

### ☐ Database Setup
- [ ] MySQL Server installed and running
- [ ] MySQL service started
- [ ] Root user accessible: `root`
- [ ] Default port 3306 available
- [ ] Can connect: `mysql -u root -p`

### ☐ Python Environment
- [ ] Python 3.8+ installed
- [ ] Python added to PATH
- [ ] `python --version` shows version
- [ ] pip is available: `pip --version`

### ☐ Project Files
- [ ] Project extracted to: `c:\Student Management System`
- [ ] All directories present (app, alembic, etc.)
- [ ] `.env` file exists with credentials
- [ ] `requirements.txt` found

---

## Installation Steps

### Step 1: Navigate to Project Directory

**Windows PowerShell:**
```powershell
cd "c:\Student Management System"
```

**Linux/macOS:**
```bash
cd ~/path/to/student-management-system
```

### Step 2: Create Python Virtual Environment

**Windows PowerShell:**
```powershell
python -m venv venv
```

**Linux/macOS:**
```bash
python3 -m venv venv
```

### Step 3: Activate Virtual Environment

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**
```cmd
venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Verification:**
Your terminal should show `(venv)` prefix

### Step 4: Upgrade pip

**All platforms:**
```bash
pip install --upgrade pip
```

### Step 5: Install Dependencies

**All platforms:**
```bash
pip install -r requirements.txt
```

**Expected output:** All packages installed successfully

**Verification:**
```bash
pip list
```

Should show all packages from requirements.txt

### Step 6: Verify Database Connection

**Check MySQL is running:**
```bash
mysql -u root -p
# Enter password when prompted (default: root)
# Should connect successfully
# Type: exit
```

### Step 7: Initialize Database

**Windows PowerShell:**
```powershell
python app/main.py
```

**This will:**
- Create database tables automatically
- Verify Jinja2 templates
- Check static files
- Display startup status

**Press Ctrl+C to stop after verification**

---

## Running the Application

### Standard Startup

**Windows PowerShell:**
```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Linux/macOS:**
```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Expected Startup Output

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
INFO:     Database tables created successfully
```

### Access Application

Open browser and navigate to:
- **Main App:** http://127.0.0.1:8000
- **API Docs:** http://127.0.0.1:8000/api/docs
- **ReDoc:** http://127.0.0.1:8000/api/redoc
- **Health Check:** http://127.0.0.1:8000/health

### Stop Application

Press: **Ctrl + C** in the terminal

---

## Production Deployment

### Using Gunicorn (Recommended for Production)

#### 1. Install Gunicorn
```bash
pip install gunicorn
```

#### 2. Run with Gunicorn
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

**Parameters:**
- `-w 4` - Number of worker processes
- `-k uvicorn.workers.UvicornWorker` - Worker class
- `--bind 0.0.0.0:8000` - Listen on all interfaces, port 8000

### Using Docker (Advanced)

#### 1. Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 2. Build Image
```bash
docker build -t student-management-system:latest .
```

#### 3. Run Container
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL="mysql+mysqlconnector://root:root@host.docker.internal:3306/student_management" \
  student-management-system:latest
```

### Using Systemd (Linux)

#### 1. Create Service File
```ini
[Unit]
Description=Student Management System
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/app
Environment=PATH=/path/to/app/venv/bin
ExecStart=/path/to/app/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

#### 2. Enable and Start Service
```bash
sudo systemctl enable student-management-system
sudo systemctl start student-management-system
sudo systemctl status student-management-system
```

---

## Configuration for Production

### Update .env File

```env
# Database (Update credentials as needed)
DATABASE_URL=mysql+mysqlconnector://root:password@localhost:3306/student_management

# Security (IMPORTANT: Change these values!)
SECRET_KEY=your-very-secure-secret-key-generated-by-openssl
ALGORITHM=HS256

# Token Expiration (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Generate Secure Secret Key

```bash
# Windows PowerShell
[System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes(32) | ConvertTo-Hex

# Linux/macOS
openssl rand -hex 32
```

### Update CORS Settings

Edit `app/main.py`, find CORS configuration:

```python
# Before (Development)
allow_origins=["*"]

# After (Production)
allow_origins=["https://yourdomain.com", "https://www.yourdomain.com"]
```

---

## Post-Deployment Verification

### ✅ Step 1: Application Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "Student Management System is running"
}
```

### ✅ Step 2: API Documentation
Open: http://localhost:8000/api/docs

Should see interactive Swagger UI with all endpoints

### ✅ Step 3: Web Interface
Open: http://localhost:8000

Should see home page with login link

### ✅ Step 4: Create Test Admin
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@test.com",
    "password": "Test123!"
  }'
```

### ✅ Step 5: Test Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "Test123!"
  }'
```

Should return JWT token

### ✅ Step 6: Test Web Login
1. Open http://localhost:8000/login
2. Enter credentials (admin / Test123!)
3. Click Login
4. Should redirect to dashboard

---

## Monitoring & Logs

### View Application Logs

**Development (with reload):**
```bash
python -m uvicorn app.main:app --reload --log-level debug
```

### Log Levels

| Level | Purpose | Command |
|-------|---------|---------|
| `critical` | Critical errors only | `--log-level critical` |
| `error` | Errors and critical | `--log-level error` |
| `warning` | Warnings and above | `--log-level warning` |
| `info` | General info (default) | `--log-level info` |
| `debug` | Detailed debugging | `--log-level debug` |

### Database Query Logging

Enable in `app/core/database.py`:

```python
engine = create_engine(
    settings.database_url,
    echo=True  # Set to True for SQL logging
)
```

---

## Troubleshooting

### Application Won't Start

**Error:** `ModuleNotFoundError: No module named 'app'`

**Solution:**
1. Ensure you're in project root: `cd c:\Student Management System`
2. Check virtual environment is activated: `(venv)` visible in prompt
3. Reinstall packages: `pip install -r requirements.txt`

---

### Database Connection Error

**Error:** `Connection refused` or `Can't connect to MySQL`

**Solution:**
1. Check MySQL is running: `mysql -u root -p`
2. Verify .env credentials: `DATABASE_URL=...`
3. Check port 3306 is open: `netstat -an | findstr 3306`

---

### Port 8000 Already in Use

**Error:** `Address already in use`

**Solution (Option 1 - Stop other app):**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F
```

**Solution (Option 2 - Use different port):**
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

---

### Jinja2 Template Error

**Error:** `jinja2.exceptions.TemplateNotFound`

**Solution:**
1. Check template directory exists: `app/templates/`
2. Verify all HTML files present (9 files)
3. Check permissions (readable)
4. Verify main.py template configuration

---

### Static Files Not Loading

**Error:** CSS/JS files return 404

**Solution:**
1. Check static directory: `app/static/`
2. Verify CSS file: `app/static/css/style.css`
3. Verify JS file: `app/static/js/main.js`
4. Check main.py has `app.mount("/static", ...)`

---

### Authentication Token Expired

**Error:** `401 Unauthorized`

**Solution:**
1. Token expires after 30 minutes (configurable)
2. Login again to get new token
3. Check browser localStorage: `localStorage.getItem('token')`

---

## Performance Optimization

### Enable Caching

```python
# Add to main.py
from fastapi.middleware.gzip import GZIPMiddleware

app.add_middleware(GZIPMiddleware, minimum_size=1000)
```

### Database Connection Pooling

Already configured in `app/core/database.py`:
```python
engine = create_engine(
    settings.database_url,
    pool_size=20,
    max_overflow=40,
    pool_recycle=3600,
)
```

### Enable Response Compression

Automatically enabled with GZIP middleware above

---

## Backup & Recovery

### Backup Database

**MySQL Dump:**
```bash
mysqldump -u root -p student_management > backup.sql
```

### Restore Database

```bash
mysql -u root -p student_management < backup.sql
```

### Backup Application Files

```bash
# Windows PowerShell
Compress-Archive -Path "c:\Student Management System" -DestinationPath backup.zip

# Linux/macOS
tar -czf backup.tar.gz /path/to/app
```

---

## Environment-Specific Configuration

### Development Setup
```env
DATABASE_URL=mysql+mysqlconnector://root:root@localhost:3306/student_management
SECRET_KEY=dev-key-not-secure
DEBUG=True
LOG_LEVEL=debug
```

### Staging Setup
```env
DATABASE_URL=mysql+mysqlconnector://user:password@staging-db:3306/student_management
SECRET_KEY=staging-key
DEBUG=False
LOG_LEVEL=info
```

### Production Setup
```env
DATABASE_URL=mysql+mysqlconnector://user:securepassword@prod-db.example.com:3306/student_management
SECRET_KEY=production-secure-key-from-openssl
DEBUG=False
LOG_LEVEL=warning
CORS_ORIGINS=["https://yourdomain.com"]
```

---

## Support & Debugging

### Enable Debug Mode

**Windows PowerShell:**
```powershell
$env:DEBUG='True'
python -m uvicorn app.main:app --reload --log-level debug
```

**Linux/macOS:**
```bash
DEBUG=True python -m uvicorn app.main:app --reload --log-level debug
```

### Test Database Connection

**Python CLI:**
```python
from app.core.database import SessionLocal
from app.models.admin import Admin

db = SessionLocal()
print(db.query(Admin).count(), "admins in database")
db.close()
```

### Common Port Numbers

| Service | Port | Alternative |
|---------|------|-------------|
| FastAPI App | 8000 | 8001, 8002, 8080 |
| MySQL | 3306 | 3307 |
| PostgreSQL | 5432 | 5433 |
| Redis | 6379 | 6380 |

---

## Performance Benchmarks

### Expected Response Times
- Page load: 500ms - 1.5s
- API call: 100 - 500ms
- Database query: 50 - 200ms
- Static file: <100ms

### Expected Load Capacity
- Concurrent users: 50-100 (single server)
- Requests per second: 100-200 (single server)
- Database connections: 20 (configured)

### Scaling Recommendations
- Horizontal: Add load balancer (nginx/HAProxy)
- Vertical: Increase server RAM/CPU
- Database: Use connection pool, read replicas
- Caching: Implement Redis for frequently accessed data

---

## Maintenance Tasks

### Regular Tasks (Weekly)
- [ ] Check application logs
- [ ] Monitor database size
- [ ] Test backup procedures

### Regular Tasks (Monthly)
- [ ] Review access logs
- [ ] Check for security updates
- [ ] Update dependencies: `pip install --upgrade -r requirements.txt`
- [ ] Database optimization: `OPTIMIZE TABLE`

### Regular Tasks (Quarterly)
- [ ] Security audit
- [ ] Performance analysis
- [ ] Disaster recovery drill

---

## Support Resources

### Documentation
- `SETUP_AND_RUN.md` - Quick start
- `WEB_UI_GUIDE.md` - UI features
- `VALIDATION_CHECKLIST.md` - Validation steps
- `COMPLETION_REPORT.md` - Project summary

### API Documentation
- Swagger UI: `/api/docs`
- ReDoc: `/api/redoc`

### Health Check
- Endpoint: `/health`
- Always accessible without authentication

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2023-12 | Initial backend API release |
| 2.0.0 | 2024-01 | Full-stack with web interface |

---

**Last Updated:** January 2024  
**Status:** Production Ready ✅

For issues or questions, refer to the documentation files or check application logs.
