# SentinelAI V2

Multi-user AI-powered Cyber Threat Intelligence Platform.

## What's New in V2

- Multi-user support with JWT authentication
- Per-user dashboard built with Streamlit
- Per-user digest scheduling
- Admin dashboard
- FastAPI backend
- Oracle Cloud deployment (24/7 uptime)

## Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI |
| Frontend | Streamlit |
| Database | SQLite → PostgreSQL |
| Auth | JWT |
| Deployment | Oracle Cloud Free Tier |

## Structure

v2/
├── backend/         # FastAPI backend
│   ├── routers/     # API route handlers
│   ├── models/      # Database models
│   ├── core/        # Auth, config, security
│   └── main.py      # Entry point
└── frontend/        # Streamlit dashboard
    ├── pages/       # Multi-page app
    ├── components/  # Reusable UI components
    └── app.py       # Entry point

## Status

🔨 Under active development