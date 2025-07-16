# 🌐 Odoo-FastAPI URL Monitoring Integration

This project integrates a FastAPI-based URL monitoring system with Odoo to enable seamless tracking of URL status, latency, incidents, and alerts from within the Odoo interface.

---

## 📌 Features

- ✅ Manage and sync URL monitors from FastAPI
- 📊 View real-time dashboard with uptime % and latency charts
- 🔁 Scheduled sync of monitor data and incidents (via cron jobs)
- ⚠️ Display and track historical incidents inside Odoo
- 🛠️ Manual “Sync Now” button support
- 🔔 Handle real-time alerts via webhook
- 👥 Role-based access control (Admin, Manager, User)

---

## 📦 Tech Stack

| Area        | Technology               |
|-------------|---------------------------|
| Backend     | Odoo (Python), FastAPI     |
| Frontend    | OWL (Odoo Web Library), QWeb |
| Scheduler   | Odoo Cron Jobs             |
| Webhooks    | Odoo Controllers           |
| Charts      | Chart.js (in Odoo Assets)  |
| Database    | PostgreSQL, SQLAlchemy     |

---

## 🧱 Module Structure

```

url\_monitor\_integration/
├── controllers/
│   └── dashboard\_controller.py
├── models/
│   ├── url\_monitor.py
│   └── url\_incident.py
├── views/
│   ├── url\_monitor\_views.xml
│   ├── url\_incident\_views.xml
│   ├── dashboard\_menu.xml
│   └── menu\_root.xml
├── static/
│   └── src/
│       ├── js/
│       │   └── monitor\_dashboard.js
│       └── xml/
│           └── monitor\_dashboard.xml
├── security/
│   └── ir.model.access.csv
├── data/
│   └── cron\_jobs.xml
├── **manifest**.py
└── README.md

````

---

## ⚙️ Setup Guide

### 1️⃣ Configuration

- Set system parameter:
  - Go to: `Settings → Technical → Parameters → System Parameters`
  - Add:  
    - Key: `fastapi_base_url`  
    - Value: `http://localhost:8000` (or your FastAPI server URL)

- Add your module path to the `addons_path` in `odoo.conf`

### 2️⃣ Install the Module

```bash
./odoo-bin -u url_monitor_integration -d your_db_name
````

Replace `your_db_name` with your actual database name.

---

## 🔁 Data Sync

### 🔹 Cron Jobs

| Job Name       | Interval | Function Called                 |
| -------------- | -------- | ------------------------------- |
| Sync Monitors  | 5 min    | `sync_monitors_from_fastapi()`  |
| Sync Incidents | 5 min    | `sync_incidents_from_fastapi()` |

Defined in: `data/cron_jobs.xml`

### 🔹 Manual Sync

* A “Sync Now” button is available on both monitor and incident forms.
* Calls the same backend sync functions.

---

## 📊 Dashboard

* Custom OWL Component (`monitor_dashboard.js`)
* Uses `/monitor/dashboard/data` HTTP route from `dashboard_controller.py`
* Renders:

  * Total Monitors
  * Down Monitors
  * Uptime % in last 24h
* Assets declared in `__manifest__.py`

---

## 🛡️ Access Control

Defined in: `security/ir.model.access.csv`

| Group                                               | Permissions (CRUD) |
| --------------------------------------------------- | ------------------ |
| base.group\_system                                  | All (1,1,1,1)      |
| You can extend it with Manager/User roles as needed |                    |

---


## 📷 Add Screenshots to README

Create a folder like:

```
assets/screenshots/
```

Then reference images like this in Markdown:

```markdown
### 💻 Dashboard Example
![URL_MONITOR Screenshot](assets/screenshots/url_monitors.png)
![URL_INCIDENT Screenshot](assets/screenshots/url_incident.png)


```

---

## 👨‍💻 Author

**Shaket Shubham**
Module: `url_monitor_integration`
Version: `1.0`
GitHub: [shaketshubham](https://github.com/shaketshubham)

---

## ✅ Future Improvements

* [ ] Add per-user dashboard filtering
* [ ] Slack/MS Teams webhook notification support
* [ ] Pagination on incident list
* [ ] Public uptime pages for each monitor

---

Let me know if you’d like me to generate screenshot placeholders or add links to your FastAPI repo. You can now drop this `README.md` file into your module root!

```
```
