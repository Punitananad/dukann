@echo off
echo ============================================
echo   RackFinder — Shop Locator Setup
echo ============================================

echo.
echo [1] Installing dependencies...
pip install -r requirements.txt

echo.
echo [2] Running database migrations...
python manage.py migrate

echo.
echo [3] Loading sample data + creating admin user...
python setup.py

echo.
echo [4] Starting development server...
echo.
echo  Open your browser: http://127.0.0.1:8000/
echo  Login: admin / admin123
echo.
python manage.py runserver
pause
