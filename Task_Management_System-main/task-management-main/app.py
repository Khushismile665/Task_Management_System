from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "taskmanagement"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "1234"
app.config["MYSQL_DB"] = "task_management"

mysql = MySQL(app)


# ---------------- LOGIN ---------------- #

@app.route("/")
def index():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM admin WHERE username=%s AND password=%s",
        (username, password)
    )

    admin = cur.fetchone()
    cur.close()

    if admin:
        session["admin"] = username
        return redirect("/home")

    return render_template("login.html",
                           error="Invalid Username or Password")


# ---------------- HOME ---------------- #

@app.route("/home")
def home():

    if "admin" not in session:
        return redirect("/")

    search = request.args.get("search", "")

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM employees")
    employees = cur.fetchall()

    if search:

        cur.execute("""
        SELECT
        t.task_id,
        e.employee_name,
        t.task_title,
        t.priority,
        t.due_date,
        t.completed,
        t.employee_id

        FROM tasks t

        JOIN employees e
        ON e.employee_id=t.employee_id

        WHERE
        e.employee_name LIKE %s
        OR
        t.task_title LIKE %s

        ORDER BY t.task_id
        """,

        (f"%{search}%", f"%{search}%"))

    else:

        cur.execute("""
        SELECT
        t.task_id,
        e.employee_name,
        t.task_title,
        t.priority,
        t.due_date,
        t.completed,
        t.employee_id

        FROM tasks t

        JOIN employees e
        ON e.employee_id=t.employee_id

        ORDER BY t.task_id
        """)

    tasks = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM tasks")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM tasks WHERE completed=1")
    completed = cur.fetchone()[0]

    pending = total - completed

    edit_task = None

    if request.args.get("edit"):

        task_id = request.args.get("edit")

        cur.execute(
            "SELECT * FROM tasks WHERE task_id=%s",
            (task_id,)
        )

        edit_task = cur.fetchone()

    cur.close()

    return render_template(
        "home.html",
        employees=employees,
        tasks=tasks,
        total=total,
        completed=completed,
        pending=pending,
        edit_task=edit_task,
        search=search
    )


# ---------------- ADD ---------------- #

@app.route("/add_task", methods=["POST"])
def add_task():

    cur = mysql.connection.cursor()

    cur.execute("""
    INSERT INTO tasks
    (employee_id,task_title,completed,priority,due_date)

    VALUES(%s,%s,%s,%s,%s)
    """,

    (

        request.form["employee_id"],
        request.form["task_title"],
        request.form["completed"],
        request.form["priority"],
        request.form["due_date"]

    ))

    mysql.connection.commit()
    cur.close()

    return redirect("/home")


# ---------------- UPDATE ---------------- #

@app.route("/update_task", methods=["POST"])
def update_task():

    cur = mysql.connection.cursor()

    cur.execute("""

    UPDATE tasks

    SET

    employee_id=%s,

    task_title=%s,

    completed=%s,

    priority=%s,

    due_date=%s

    WHERE task_id=%s

    """,

    (

        request.form["employee_id"],
        request.form["task_title"],
        request.form["completed"],
        request.form["priority"],
        request.form["due_date"],
        request.form["task_id"]

    ))

    mysql.connection.commit()
    cur.close()

    return redirect("/home")


# ---------------- DELETE ---------------- #

@app.route("/delete_task/<int:id>")
def delete_task(id):

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM tasks WHERE task_id=%s",
        (id,)
    )

    mysql.connection.commit()
    cur.close()

    return redirect("/home")


# ---------------- LOGOUT ---------------- #

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)