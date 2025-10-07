# Me-API Playground 🚀

A comprehensive profile management API playground built with FastAPI, showcasing skills, projects, and professional experience. This application serves as a backend assessment demonstrating full-stack development capabilities.

## 🚀 Quick Start (TL;DR)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create database and seed data
python seed_database.py

# 3. Start the application (RECOMMENDED METHOD)
uvicorn main_profile:app --host 0.0.0.0 --port 8000 --reload

# 4. Open in browser
# Frontend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

**Note**: If you get Pydantic errors with `python main_profile.py`, use the uvicorn command above instead!

## 📖 How to Run the Application

### Method 1: Using Uvicorn (RECOMMENDED)
```bash
uvicorn main_profile:app --host 0.0.0.0 --port 8000 --reload
```

### Method 2: Using the Startup Script
```bash
python start_app.py
```

### Method 3: Direct Python (May have issues)
```bash
python main_profile.py
```

### What You'll See When It Works:
- ✅ Server starts without errors
- ✅ Database is created and seeded with sample data
- ✅ Frontend loads at http://localhost:8000
- ✅ API documentation at http://localhost:8000/docs
- ✅ All endpoints work (health, profiles, search, etc.)

### To Stop the Server:
Press `Ctrl+C` in the terminal where the server is running.

## 🏗️ Architecture

### Backend
- **Framework**: FastAPI (Python 3.8+)
- **Database**: SQLite (easily configurable for PostgreSQL/MySQL)
- **ORM**: SQLAlchemy 2.0
- **Validation**: Pydantic v2
- **API Documentation**: Auto-generated with Swagger UI

### Frontend
- **Technology**: Vanilla HTML/CSS/JavaScript
- **Features**: Responsive design, real-time search, interactive UI
- **Integration**: Direct API consumption with CORS support

### Database Schema
```sql
-- Core Profile Management
profiles (id, name, email, education, bio, location, created_at, updated_at)
skills (id, profile_id, name, level, category, created_at)
projects (id, profile_id, title, description, technologies, github_url, live_url, start_date, end_date, is_active)
work_experiences (id, profile_id, company, position, description, start_date, end_date, is_current, location)
profile_links (id, profile_id, platform, url, created_at)

-- Legacy Wallet Management (for backward compatibility)
users (id, name, email, phone, created_at)
wallets (id, user_id, balance, updated_at)
transactions (id, user_id, amount, transaction_type, description, created_at)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Fullstack
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**
   ```bash
   python seed_database.py
   ```

5. **Run the application**
   
   **Method 1: Using Uvicorn (Recommended)**
   ```bash
   uvicorn main_profile:app --host 0.0.0.0 --port 8000 --reload
   ```
   
   **Method 2: Using the startup script**
   ```bash
   python start_app.py
   ```
   
   **Method 3: Direct Python (if Method 1 doesn't work)**
   ```bash
   python main_profile.py
   ```

6. **Access the application**
   - Frontend: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Alternative API Docs: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/health

### Production Setup

1. **Environment Variables**
   ```bash
   export DATABASE_URL="postgresql://user:password@localhost/meapi_playground"
   export DEBUG=False
   ```

2. **Database Migration** (for PostgreSQL)
   ```bash
   # The application will automatically create tables on startup
   # For production, consider using Alembic for migrations
   ```

3. **Deploy with Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn main_profile:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

## 📚 API Endpoints

### Core Profile Management

#### Profiles
- `POST /profiles` - Create a new profile
- `GET /profiles` - List all profiles (with pagination)
- `GET /profiles/{profile_id}` - Get complete profile details
- `PUT /profiles/{profile_id}` - Update profile
- `DELETE /profiles/{profile_id}` - Delete profile

#### Skills
- `POST /profiles/{profile_id}/skills` - Add skill to profile
- `GET /profiles/{profile_id}/skills` - Get profile skills
- `GET /skills/top` - Get most common skills
- `GET /skills/search` - Search skills by name/level

#### Projects
- `POST /profiles/{profile_id}/projects` - Add project to profile
- `GET /profiles/{profile_id}/projects` - Get profile projects
- `GET /projects?skill={skill}` - Get projects by skill/technology

#### Work Experience
- `POST /profiles/{profile_id}/work` - Add work experience
- `GET /profiles/{profile_id}/work` - Get work experience

#### Profile Links
- `POST /profiles/{profile_id}/links` - Add profile link
- `GET /profiles/{profile_id}/links` - Get profile links

### Search & Query
- `GET /search?q={query}` - Global search across all content
- `GET /health` - Health check endpoint

## 🔍 Sample API Usage

### Create a Profile
```bash
curl -X POST "http://localhost:8000/profiles" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Developer",
    "email": "john@example.com",
    "education": "Computer Science Degree",
    "bio": "Passionate full-stack developer",
    "location": "San Francisco, CA"
  }'
```

### Add Skills to Profile
```bash
curl -X POST "http://localhost:8000/profiles/1/skills" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python",
    "level": "expert",
    "category": "programming"
  }'
```

### Search Projects by Skill
```bash
curl "http://localhost:8000/projects?skill=Python"
```

### Global Search
   ```bash
curl "http://localhost:8000/search?q=machine%20learning"
   ```

### Get Top Skills
   ```bash
curl "http://localhost:8000/skills/top?limit=10"
```

## 🎯 Features Implemented

### ✅ Backend & API Requirements
- [x] Profile CRUD operations (name, email, education, bio, location)
- [x] Skills management with levels and categories
- [x] Projects with technologies, links, and descriptions
- [x] Work experience tracking
- [x] Profile links (GitHub, LinkedIn, portfolio)
- [x] Query endpoints:
  - [x] `GET /projects?skill=python` - Projects by skill
  - [x] `GET /skills/top` - Most common skills
  - [x] `GET /search?q=...` - Global search
- [x] `GET /health` - Health check endpoint

### ✅ Database Requirements
- [x] SQLite database (easily configurable for PostgreSQL/MySQL)
- [x] Complete schema with relationships
- [x] Seeded with realistic sample data
- [x] Proper indexing for performance

### ✅ Frontend Requirements
- [x] Minimal but functional HTML/CSS/JavaScript UI
- [x] Search by skill functionality
- [x] Project listing and display
- [x] Profile viewing capabilities
- [x] CORS configured for API calls
- [x] Responsive design

### ✅ Additional Features
- [x] Comprehensive API documentation
- [x] Input validation and error handling
- [x] Pagination support
- [x] Real-time search
- [x] Statistics dashboard
- [x] Health monitoring

## 🛠️ Technology Stack

- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Database**: SQLite (production-ready for PostgreSQL)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Development**: Python 3.8+, pip, virtual environments
- **Documentation**: Swagger UI, ReDoc

## 📊 Database Schema Details

### Profile Management Tables

#### profiles
- Primary key: `id`
- Unique constraints: `email`
- Indexes: `email`, `created_at`

#### skills
- Foreign key: `profile_id` → `profiles.id`
- Indexes: `name`, `level`, `category`

#### projects
- Foreign key: `profile_id` → `profiles.id`
- JSON field: `technologies` (array of strings)
- Indexes: `title`, `is_active`, `start_date`

#### work_experiences
- Foreign key: `profile_id` → `profiles.id`
- Indexes: `company`, `start_date`, `is_current`

#### profile_links
- Foreign key: `profile_id` → `profiles.id`
- Indexes: `platform`, `url`

## 🚀 Deployment Options

### Heroku
1. Add `Procfile`: `web: gunicorn main_profile:app -w 4 -k uvicorn.workers.UvicornWorker`
2. Add PostgreSQL addon
3. Set environment variables
4. Deploy with Git

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main_profile.py"]
```

### AWS/GCP/Azure
- Use managed database services (RDS, Cloud SQL, etc.)
- Deploy with container services or serverless functions
- Configure load balancers and CDN for frontend

## 🔧 Configuration

### Environment Variables
```bash
DATABASE_URL=sqlite:///./meapi_playground.db  # Database connection string
DEBUG=True                                    # Debug mode
CORS_ORIGINS=*                               # CORS allowed origins
```

### Database Configuration
The application supports multiple database backends:
- SQLite (default, for development)
- PostgreSQL (recommended for production)
- MySQL (supported via SQLAlchemy)

## 📈 Performance Considerations

- Database queries are optimized with proper indexing
- Pagination implemented for large datasets
- Caching can be added with Redis for production
- API responses are compressed
- Frontend assets are minified

## 🧪 Testing

### Manual Testing
- Use the interactive API documentation at `/docs`
- Test the frontend interface at the root URL
- Verify all CRUD operations work correctly

### Automated Testing (Future Enhancement)
```bash
# Install testing dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue 1: Pydantic Import Errors
**Error**: `ImportError: email-validator is not installed`
**Solution**:
```bash
pip install pydantic[email]
```

#### Issue 2: Server Won't Start with `python main_profile.py`
**Error**: Long Pydantic model rebuild errors
**Solution**: Use uvicorn directly instead:
```bash
uvicorn main_profile:app --host 0.0.0.0 --port 8000 --reload
```

#### Issue 3: Database Tables Don't Exist
**Error**: `no such table: profile_links`
**Solution**: Create tables first:
```bash
python -c "from database import engine; import models; models.Base.metadata.create_all(bind=engine)"
python seed_database.py
```

#### Issue 4: Port Already in Use
**Error**: `Address already in use`
**Solution**: Kill existing processes and try again:
```bash
# Windows
taskkill /f /im python.exe
taskkill /f /im uvicorn.exe

# Then restart
uvicorn main_profile:app --host 0.0.0.0 --port 8000 --reload
```

#### Issue 5: Static Files Not Found
**Error**: `StaticFiles directory not found`
**Solution**: The app will work without static files, but create the directory:
```bash
mkdir static
```

### Quick Start Commands
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create database and seed data
python seed_database.py

# 3. Start the application
uvicorn main_profile:app --host 0.0.0.0 --port 8000 --reload

# 4. Open in browser
# Frontend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 🐛 Known Limitations

1. **Authentication**: No user authentication system (can be added)
2. **File Uploads**: No support for profile images or project screenshots
3. **Real-time Updates**: No WebSocket support for real-time updates
4. **Rate Limiting**: No API rate limiting (can be added with Redis)
5. **Caching**: No caching layer (can be added with Redis)
6. **Logging**: Basic logging (can be enhanced with structured logging)

## 🔮 Future Enhancements

- [ ] User authentication and authorization
- [ ] File upload for profile images and project screenshots
- [ ] Real-time notifications with WebSockets
- [ ] Advanced search with filters and sorting
- [ ] API rate limiting and caching
- [ ] Comprehensive test suite
- [ ] CI/CD pipeline
- [ ] Monitoring and analytics dashboard

## 📞 Contact & Resume

**Developer**: Gagan
**Email**: [Your Email]
**GitHub**: [Your GitHub Profile]
**LinkedIn**: [Your LinkedIn Profile]
**Portfolio**: [Your Portfolio Website]

**Resume**: [Link to your resume/CV]

## 📄 License

This project is created for assessment purposes. All rights reserved.

---

## 🎉 Getting Started

1. **Clone and setup** the repository
2. **Install dependencies** with `pip install -r requirements.txt`
3. **Seed the database** with `python seed_database.py`
4. **Run the application** with `python main_profile.py`
5. **Visit** http://localhost:8000 to explore the playground!

The application includes comprehensive sample data showcasing various profiles, skills, projects, and work experiences. Use the search functionality to explore the data and test the API endpoints through the interactive documentation.