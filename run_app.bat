@echo off
echo 🚀 Starting Me-API Playground...
echo ================================

echo.
echo 📊 Checking database...
if not exist "meapi_playground.db" (
    echo Database not found. Creating and seeding...
    python seed_database.py
    if errorlevel 1 (
        echo ❌ Error creating database
        pause
        exit /b 1
    )
    echo ✅ Database created successfully!
) else (
    echo ✅ Database already exists
)

echo.
echo 🌐 Starting FastAPI server...
echo 📍 Server will be available at: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/docs
echo 🛑 Press Ctrl+C to stop the server
echo ================================

uvicorn main_profile:app --host 0.0.0.0 --port 8000 --reload

pause