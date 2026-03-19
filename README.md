# MyProductivity - Task Management System

A robust Full-stack Task Management application built with **Python 3.13** and **Django 5.2**.

## Project Overview
This project features a dynamic user interface with asynchronous updates and a secure backend architecture.

### Key Features:
- **Interactive UI**: Powered by **HTMX** and **Hyperscript** for seamless, no-reload interactions (adding, toggling, and deleting tasks/projects).
- **Drag-and-Drop Prioritization**: Interactive task reordering using **SortableJS**, with persistence in the PostgreSQL database.
- **Smart Sorting**: Tasks are organized by status (Active/Done) and custom user position.
- **Authentication**: Full user lifecycle (Login, Signup, Password Reset) via **django-allauth**.
- **Database Analysis**: Custom SQL reporting available in `SQL.md`.

---

## Note on Design and Architecture 
This repository contains two versions of the application:

### 1. Main Branch (`main`) 
As per the technical requirements (**"It should look like on screens"**), this branch features.
**Note**: Deadlines and manual priority levels are hidden in this branch to maintain visual identity with the original specification.

### 2. Development Branch (`dev`) - **With extended logic**
Please check the `dev` branch:
- Clean Bootstrap 5 interface with card-based layouts and better accessibility.
- Logic: Includes UI elements for **Deadlines** and **Priority Levels** (High/Medium/Low) which were not present in the original screenshots but are essential for a real-world Task Manager.
- **Alternative Sorting**: Logic that balances manual Drag-and-Drop with automated Priority/Deadline sorting.

---

## Tech Stack
- **Backend**: Python 3.13, Django 5.2
- **Database**: PostgreSQL
- **Frontend**: Bootstrap 5, HTMX, Hyperscript, SortableJS
- **DevOps**: Docker, Docker Compose

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <https://github.com/aculaxxl/MyProductivity>
2. Run with Docker:
    ```bash
    docker compose up --build
3. Initialize Database:
    ```bash
    docker compose exec web python manage.py migrate
4. Access the App:
    Open http://localhost:8000 in your browser.