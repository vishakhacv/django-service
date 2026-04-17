# Task & Project Management System

A full-stack application with **Laravel** (API), **Django** (microservice), and **React** (frontend).

## Prerequisites
- PHP 8.1+ & Composer
- Python 3.10+ (installed ✅)
- Node.js 18+ (installed ✅)

## 1. Install PHP & Composer (if not installed)

### Option A — Using scoop (recommended)
```bash
scoop install php composer
```

### Option B — Manual
1. Download PHP 8.2 from https://windows.php.net/download (VS16 x64 Thread Safe)
2. Extract to `C:\php`, add to PATH
3. In `C:\php\php.ini`, enable: `extension=pdo_sqlite`, `extension=sqlite3`, `extension=openssl`, `extension=mbstring`, `extension=tokenizer`, `extension=fileinfo`
4. Download Composer from https://getcomposer.org/download/

## 2. Laravel Backend (port 8000)

```bash
cd E:\Vishakha\abspanel\proj_v\laravel-backend

# Install PHP dependencies
composer install

# Generate app key
php artisan key:generate

# Run migrations & seed
php artisan migrate --seed

# Start server
php artisan serve
```

## 3. Django Microservice (port 8001)

```bash
cd E:\Vishakha\abspanel\proj_v\django-service

# Dependencies already installed via pip
# Start server
python manage.py runserver 8001
```

### Endpoints
- `POST /api/check-overdue/` — scan & mark overdue tasks
- `POST /api/tasks/{id}/close/` — close overdue task (admin auth required)
- `GET /api/overdue-tasks/` — list all overdue tasks

## 4. React Frontend (port 5173)

```bash
cd E:\Vishakha\abspanel\proj_v\react-frontend

# Dependencies already installed
npm run dev
```

Open http://localhost:5173 in browser.


For frontend live testing either go to (http://localhost:5173) else run via ngrok;
# Install ngrok (one time)
npm install -g ngrok

# Start your frontend normally, then in another terminal:
ngrok http 5173
