# Deelflow Admin Backend

Deelflow Admin Backend is a Django REST API server for property analytics, AI-powered predictions, business metrics, and admin management. It supports user authentication, role-based permissions, campaign analytics, and integrates with external AI services.

## Features

- **User Authentication**: JWT-based login, registration, and organization management.
- **Role & Permission Management**: Custom roles, permissions, and admin controls.
- **Property Analytics**: AI-driven property analysis, repair estimates, neighborhood metrics.
- **Business Metrics**: Revenue, deals, user growth, compliance, and activity feeds.
- **Campaign Management**: Campaigns, leads, channel response rates, performance stats.
- **AI Metrics**: NLP, Vision, Voice AI, Blockchain transaction metrics.
- **Admin Dashboard**: Django admin for all models.
- **API Endpoints**: RESTful endpoints for all resources.
- **CORS Support**: Configured for local development and frontend integration.

## Project Structure

```
ai_prediction_worker.py
db.sqlite3
manage.py
requirements.txt
deelflow/
    __init__.py
    admin.py
    apps.py
    decorators.py
    models.py
    models_property_ai_analysis.py
    serializers.py
    tests.py
    urls.py
    views.py
    management/
    migrations/
deelflowAI/
    __init__.py
    asgi.py
    settings.py
    urls.py
    wsgi.py
```

## Setup

### Prerequisites

- Python 3.8+
- pip
- [virtualenv](https://virtualenv.pypa.io/en/latest/) (recommended)

### Installation

1. **Clone the repository**
    ```sh
    git clone <repo-url>
    cd Deelflow-Admin-Backend-main
    ```

2. **Create and activate a virtual environment**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4. **Apply migrations**
    ```sh
    python manage.py migrate
    ```

5. **Create a superuser (for Django admin)**
    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server**
    ```sh
    python manage.py runserver
    ```

## API Endpoints

See [`deelflow/urls.py`](deelflow/urls.py) and [`deelflow/views.py`](deelflow/views.py) for all endpoints.

### Authentication

- `POST /create-user/` — Register a new user
- `POST /login/` — Login and get JWT token

### Property Analytics

- `POST /property_analysis/` — Get property analysis by address
- `POST /repair_analysis/` — Get repair estimates
- `POST /neighborhood_analysis/` — Get neighborhood metrics

### Metrics & Business Data

- `GET /api/total-revenue/` — Latest revenue
- `GET /api/total-deals/` — Latest deals
- `GET /api/active-users/` — Active users
- `GET /api/voice-calls-count/` — Voice AI call metrics
- `GET /api/nlp-processing/` — NLP metrics
- `GET /api/blockchain-txns/` — Blockchain transaction metrics
- `GET /api/vision-analysis/` — Vision analysis metrics
- `GET /api/system-health-metrics/` — System health status

### Campaigns & Channels

- `GET /active_campaign_summary/` — Campaign summary
- `GET /lead_conversion_funnel/` — Lead funnel
- `GET /channel_status/` — Channel status
- `GET /channel_response_rates/` — Channel response rates

### Roles & Permissions

- `GET /get_roles/` — List roles
- `POST /create_role/` — Create role
- `POST /delete_role/` — Delete role
- `GET /get_permissions/` — List permissions
- `POST /update_role_permissions/` — Update role permissions

### Admin

- Django admin at `/admin/`

## Models

See [`deelflow/models.py`](deelflow/models.py) for all models, including:

- `User`, `Organization`
- `BusinessMetrics`, `HistoricalMetrics`, `ActivityFeed`, `ComplianceStatus`
- `Role`, `Permission`
- `PropertyAIAnalysis`, `NLPProcessingMetrics`, `BlockchainTxnMetrics`
- `Campaign`, `Lead`, `Channel`, `ChannelResponseRate`, `CampaignPerformance`, `CampaignPropertyStats`

## Development

- **Run tests:**  
    ```sh
    python manage.py test
    ```
- **Custom management commands:**  
    See [`deelflow/management/commands/run_ai_agent.py`](deelflow/management/commands/run_ai_agent.py)

## Configuration

- **CORS:**  
    Configured in [`deelflowAI/settings.py`](deelflowAI/settings.py)
- **Database:**  
    SQLite by default, see [`deelflowAI/settings.py`](deelflowAI/settings.py)

## License

MIT License (or specify your license)

## Contact

For support, contact [admin@example.com](mailto:admin@example.com)

---

**Note:**  
This backend is intended for development and demonstration. For production, review security, secret management, and deployment best