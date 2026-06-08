# L&C Shopping 🛍️

A full-stack e-commerce web application for clothing and accessories, built with Python Django and deployed on AWS Elastic Beanstalk.

🔗 **Live Demo**: [http://lc-shopping-env.eba-bwiwmcjd.eu-west-2.elasticbeanstalk.com](http://lc-shopping-env.eba-bwiwmcjd.eu-west-2.elasticbeanstalk.com)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.13, Django 6.0 |
| Database | PostgreSQL (psycopg), SQLite (dev) |
| Storage | AWS S3 (django-storages, boto3) |
| Deployment | AWS Elastic Beanstalk (eu-west-2) |
| Web Server | Gunicorn + Nginx (via EB platform) |
| Frontend | HTML5, CSS3, Bootstrap 4 |
| Auth | Custom user model (email-based) |
| Security | django-ratelimit, CSRF protection, session timeout |

---

## ✨ Features

- **Product catalogue** — browse products by category with image galleries
- **Search** — keyword-based product search across name and description
- **User accounts** — register, login, email-based authentication with custom user model
- **Shopping cart** — add/remove items, quantity management, session-based cart
- **Checkout & orders** — order placement with order history dashboard
- **Product reviews** — authenticated users can submit and view ratings and reviews
- **Admin panel** — full product, category, and order management via Django admin
- **Security** — rate-limited login, session timeout, CSRF protection, OWASP-aware implementation

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│           AWS Elastic Beanstalk         │
│  ┌──────────────────────────────────┐   │
│  │   EC2 (t3.micro, eu-west-2)      │   │
│  │   Gunicorn → Django 6.0          │   │
│  │   Nginx (EB managed)             │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
         │                    │
         ▼                    ▼
┌──────────────┐    ┌──────────────────┐
│  PostgreSQL  │    │    AWS S3        │
│  (RDS)       │    │  Static & Media  │
└──────────────┘    └──────────────────┘
```

### Key design decisions

- **Custom user model** — uses email instead of username for authentication, implemented from project start to avoid migration issues later
- **Environment-based configuration** — all secrets and environment-specific settings managed via `python-decouple`, never hardcoded
- **Conditional S3/local storage** — `USE_S3_STATIC` and `USE_S3_MEDIA` flags allow seamless switching between local development and S3 production storage
- **Platform hooks** — migrations and `collectstatic` run automatically on every deploy via `.platform/hooks/postdeploy/`
- **Rate limiting** — login endpoint protected against brute force attacks using `django-ratelimit`

---

## 📁 Project Structure

```
L-C-Shopping/
├── accounts/          # Custom user model, auth views, registration
├── carts/             # Cart logic, session management
├── category/          # Category model, context processor
├── store/             # Product model, search, reviews
├── orders/            # Order model, checkout, order history
├── lcshop/            # Project config, settings, URLs, storage backends
├── templates/         # HTML templates
├── staticfiles/       # Collected static files
├── .ebextensions/     # AWS Elastic Beanstalk config
├── .platform/         # EB platform hooks (migrations, collectstatic)
├── Procfile           # Gunicorn startup command
└── requirements.txt   # Python dependencies
```

---

## 🚀 Running Locally

### Prerequisites
- Python 3.13
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/Chithranjaly/L-C-Shopping.git
cd L-C-Shopping

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your local settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_ENGINE=sqlite
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## ☁️ Deployment

The application is deployed on AWS Elastic Beanstalk using the EB CLI:

```bash
# Initialise EB (first time only)
eb init --profile your-profile

# Create environment
eb create your-env-name --single --instance-types t3.micro

# Deploy updates
eb deploy
```

Migrations and static file collection run automatically via `.platform/hooks/postdeploy/01_collectstatic.sh` on every deploy.

---

## 🔒 Security Considerations

- No hardcoded secrets — all sensitive values read from environment variables
- Rate-limited login endpoint to prevent brute force attacks
- Session timeout after 1 hour of inactivity
- CSRF protection enabled on all forms
- OWASP Top 10 awareness applied throughout development
- SQLite database excluded from version control via `.gitignore`

---

## 👩‍💻 Developer

**Chithranjaly** — MSc graduate building toward a software engineering career.

- GitHub: [@Chithranjaly](https://github.com/Chithranjaly)

---

## 📄 Licence

This project is for portfolio and educational purposes.
