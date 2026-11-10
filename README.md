# Student Leave Hub

A full-stack **Leave Management System** built with **Django** for managing student leave requests in an academic environment. Students can register, manage their academic profile, submit leave applications with supporting documents, and monitor request statuses on an interactive calendar and dashboard, while administrators can review, approve, or reject requests and analyze leave trends.

---

## Live Website & Deployment Status

No live hosted URL is currently published in this repository. The application is deployment-ready and includes configuration files for **Render** (`render.yaml`, `render-build.sh`, `runtime.txt`) and **Procfile**-compatible platforms such as **Railway** (`Procfile`).

---

## Features

### Student Features
- **Account Registration & Authentication**: Self-service student registration (`/register/`), login, logout, and password reset flow (`/accounts/`).
- **Automatic Profile Creation**: Automatically creates a `StudentProfile` (`college_name`, `department`, `registration_number`) upon user registration via Django `post_save` signals.
- **Profile Management**: View and edit academic profile details (`/profile/`) with a read-only username field.
- **Leave Request Submission**: Apply for single-day or multi-day leave (`/new/`) with a reason and optional supporting attachment (e.g., medical certificate or proof).
- **Request Tracking & Management**: View personal leave history (`/my-requests/`), and edit or cancel requests while they are still `Pending`.

### Administrator Features
- **Role-Based Access Control**: Staff accounts (`is_staff`) have dedicated views and permissions separated from student accounts.
- **Request Review Workflow**: View all leave requests (`/all-requests/`), approve or reject pending applications with an optional `admin_response` comment, and delete rejected records.
- **Admin Analytics Dashboard**: Visualizes **Leave Status Distribution** (doughnut chart) and **Leaves by Department** (bar chart) at `/analytics/` using **Chart.js**.
- **Email Notifications**: Sends a notification via Django's `send_mail` when a new leave request is submitted (configured with Django's `console.EmailBackend` by default for development).

### UI & Experience
- **Interactive Dashboard & Calendar**: Displays summary counters (Total, Approved, Pending, Rejected) alongside an interactive **FullCalendar** schedule fed by the `/api/events/` JSON endpoint (color-coded by status).
- **Light & Dark Mode**: Persistent theme toggle stored in `localStorage` across both the main portal and authentication pages.
- **Responsive Design**: Desktop sidebar navigation and a mobile slide-out drawer with responsive layouts for cards, forms, calendars, and charts.
- **Interactive Touches**: Dynamic time-of-day greetings, animated toast notifications, animated canvas particles and rotating scientific quotes on auth pages, and an "On This Day" scientific fact card on the dashboard.

---

## Technology Stack

- **Backend**: Python (`3.11.9`), Django (`6.0.3`)
- **Frontend**: HTML5, Custom CSS3, Vanilla JavaScript (ES6+, HTML5 Canvas)
- **Frontend Libraries (CDN)**:
  - [Chart.js](https://www.chartjs.org/) (Admin analytics charts)
  - [FullCalendar](https://fullcalendar.io/) `6.1.10` (Interactive leave calendar)
  - [Font Awesome](https://fontawesome.com/) `6.4.0` (Icons)
  - [Google Fonts — Inter](https://fonts.google.com/specimen/Inter) (Typography)
- **Databases & Connectors**:
  - SQLite (`db.sqlite3`, default for local development)
  - PostgreSQL (`psycopg2-binary`, `psycopg[binary]`)
  - MySQL / MariaDB (`PyMySQL` with SSL configuration support)
  - `dj-database-url` for environment-based database configuration
- **Server & Deployment**:
  - Gunicorn (`21.2.0`)
  - WhiteNoise (`6.6.0`) for compressed static files
  - `python-dotenv` (`1.0.1`)
  - Render (`render.yaml`, `render-build.sh`) & Railway/WSGI (`Procfile`)

---

## Installation & Setup

Follow these steps to run the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/Abhilash-KK/leave-management.git
cd leave-management
```

### 2. Create and Activate a Virtual Environment
- **Windows (PowerShell / Command Prompt):**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

> **Note:** `runtime.txt` specifies Python `3.11.9`. Using Python 3.11 is recommended for smooth compatibility with the pinned packages in `requirements.txt`.

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables (Optional for Local SQLite)
By default, `leave_project/settings.py` runs with `DEBUG=True` and uses the local SQLite database (`db.sqlite3`), so no extra configuration is required to get started locally.

If you want to customize settings or connect a PostgreSQL/MySQL database, refer to `.env.example`:
```env
SECRET_KEY=django-insecure-local-key-change-me-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://user:password@host:port/dbname
```

### 5. Run Database Migrations
```bash
python manage.py migrate
```

### 6. Create an Admin Account
You can create a custom Django superuser:
```bash
python manage.py createsuperuser
```
Or run the included helper script (creates/updates an admin user with username `admin` and password `admin` — be sure to change these credentials in production):
```bash
python create_admin.py
```

### 7. Start the Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser. The Django Admin interface is available at `http://127.0.0.1:8000/admin/`.

---

## Project Structure

```text
leave-management/
├── leave_project/                # Django project settings and entry points
│   ├── __init__.py               # PyMySQL setup & MySQL/MariaDB compatibility patches
│   ├── asgi.py                   # ASGI configuration
│   ├── settings.py               # Core settings (DB, WhiteNoise static files, media, auth, email)
│   ├── urls.py                   # Root URL routing (/admin/, /accounts/, and leaves app)
│   └── wsgi.py                   # WSGI configuration for Gunicorn
├── leaves/                       # Main leave management Django app
│   ├── migrations/               # Database migration files
│   ├── static/images/            # Static image assets
│   ├── templates/
│   │   ├── leaves/               # Portal UI templates (base, dashboard, analytics, profile, requests)
│   │   └── registration/       # Login, registration, and password reset templates
│   ├── admin.py                  # Django admin module
│   ├── apps.py                   # App configuration
│   ├── forms.py                  # Registration, LeaveRequest, UserUpdate, and StudentProfile forms
│   ├── models.py                 # LeaveRequest & StudentProfile models + post_save signals
│   ├── tests.py                  # Test module
│   ├── urls.py                   # App routes and /api/events/ calendar JSON endpoint
│   └── views.py                  # Dashboard, CRUD, approval/rejection, analytics, and profile views
├── .env.example                  # Example environment variables
├── create_admin.py               # Script to create/reset the default superuser account
├── db.sqlite3                    # Local SQLite database
├── manage.py                     # Django management CLI utility
├── Procfile                      # Gunicorn web process definition
├── render-build.sh               # Render build script (pip install, collectstatic, migrate, create_admin)
├── render.yaml                   # Render service blueprint configuration
├── requirements.txt              # Python dependencies
├── runtime.txt                   # Python runtime version (3.11.9)
└── README.md                     # Project documentation
```

---

## Author

- **Abhilash**
- GitHub: [@Abhilash-KK](https://github.com/Abhilash-KK)
- Email: `kkabhilash30@gmail.com`
