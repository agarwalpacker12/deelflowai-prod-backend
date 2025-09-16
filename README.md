# DeelflowAI Backend

This is the backend for the DeelflowAI project, built with Django and Django REST Framework.

## Project Structure

```
db.sqlite3
manage.py
requirements.txt
deelflow/
    __init__.py
    admin.py
    apps.py
    decorators.py
    models.py
    serializers.py
    tests.py
    urls.py
    views.py
    migrations/
deelflowAI/
    __init__.py
    asgi.py
    settings.py
    urls.py
    wsgi.py
```

## Features

- **User Management:** Custom `User` model with organization relationship, JWT authentication, and registration endpoints.
- **Business Metrics:** Models and APIs for business metrics, historical data, compliance status, and activity feeds.
- **Admin Interface:** Django admin integration for managing users and organizations.
- **REST API:** Endpoints for metrics, compliance, activity feed, and user authentication.
- **CORS Support:** Configured for cross-origin requests.
- **Security:** Passwords are hashed, JWT tokens are used for authentication.

## Setup

1. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

2. **Apply migrations:**
    ```sh
    python manage.py migrate
    ```

3. **Run the development server:**
    ```sh
    python manage.py runserver
    ```

## API Endpoints

- `POST /create-user/` — Register a new user
- `POST /login/` — User login (returns JWT)
- `GET /api/total-revenue/` — Get latest total revenue
- `GET /api/active-users/` — Get latest active users
- `GET /api/properties-listed/` — Get latest properties listed
- `GET /api/ai-conversations/` — Get latest AI conversations
- `GET /api/total-deals/` — Get latest total deals
- `GET /api/monthly-profit/` — Get latest monthly profit
- `GET /api/voice-calls-count/` — Get latest voice calls count
- `GET /api/compliance-status/` — Get latest compliance status
- `GET /api/audit-trail-data/` — Get audit trail data
- `GET /api/system-health-metrics/` — Get system health metrics
- `GET /api/revenue-user-growth-chart-data/` — Get revenue and user growth chart data
- ...and more

## Main Files

- [deelflow/models.py](deelflow/models.py): Django models for users, organizations, metrics, etc.
- [deelflow/views.py](deelflow/views.py): API views for authentication and metrics.
- [deelflow/serializers.py](deelflow/serializers.py): Serializers for API data.
- [deelflow/urls.py](deelflow/urls.py): App URL routes.
- [deelflowAI/settings.py](deelflowAI/settings.py): Project settings.
- [requirements.txt](requirements.txt): Python dependencies.

## Requirements

- Python 3.8+
- Django 4.2.x
- djangorestframework
- djangorestframework-simplejwt
- django-cors-headers

## License

This project is for internal use. See LICENSE file