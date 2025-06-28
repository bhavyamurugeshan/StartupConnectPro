# StartupConnectPro
# 🚀 StartupConnectPro

**StartupConnectPro** is a lightweight web application built with Python and Flask. It enables founders and startups to connect seamlessly with investors, mentors, and peers through interactive forms, lists, and matchmaking logic.

---

## 🧩 Features

- **User Interaction**  
  Founder and investor profiles with contact details and preferences via web forms (`forms.py`).

- **Data Modeling & Storage**  
  Uses SQLAlchemy models (`models.py`) and `data_store.py` for database connectivity and data access.

- **Routing & Views**  
  Clean URL structure with Flask routes in `routes.py` and main logic in `app.py`.

- **HTML Templates & Static Assets**  
  Fully styled UI using Jinja2 templates (in `templates/`) and CSS/JavaScript in `static/`.

- **Replit-Friendly Setup**  
  Includes `replit.md` with instructions for deploying and running in Replit environments.

---

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/bhavyamurugeshan/StartupConnectPro.git
   cd StartupConnectPro

StartupConnectPro/
├── app.py            — App initialization
├── main.py           — Main entry point (if separated)
├── routes.py         — Flask routes for pages & forms
├── forms.py          — WTForms form definitions
├── models.py         — SQLAlchemy database models
├── data_store.py     — Database connection & session management
├── templates/        — Jinja2 HTML templates
├── static/           — CSS, JS, images, assets
├── pyproject.toml    — Poetry project config & dependencies
├── requirements.txt  — (Optional) pip dependencies
├── replit.md         — Replit-specific setup guide
└── LICENSE           — MIT license

