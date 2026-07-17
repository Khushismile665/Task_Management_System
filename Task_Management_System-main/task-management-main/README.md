# TaskFlow

A modern task management dashboard built with **Flask** and **MySQL** for assigning, tracking, and managing employee tasks.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Framework-black?logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-Database-blue?logo=mysql)

---

## Features

- Secure Admin Login
- Assign, Update & Delete Tasks
- Employee Task Tracking
- Search Tasks
- Dashboard Analytics
- Task Priority Management
- Due Date Tracking
- Responsive UI

---

## Tech Stack

- Python
- Flask
- MySQL
- HTML5
- CSS3
- Bootstrap Icons

---

## Getting Started

Clone the repository.

```bash
git clone https://github.com/Khushismile665/Task_Management_System.git
```

Install dependencies.

```bash
pip install flask flask-mysqldb
```

Import the provided **database.sql** into MySQL.

Update the database credentials in `app.py`.

```python
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "YOUR_PASSWORD"
app.config["MYSQL_DB"] = "task_management"
```

Run the project.

```bash
python app.py
```

Open

```
http://127.0.0.1:5000
```

---


## Project Structure

```
task-management/
│
├── app.py
├── database.sql
├── static/
├── templates/
└── README.md
```

---

## Author

**Rohan Decharwal**

GitHub → https://github.com/RohanDecharwal
