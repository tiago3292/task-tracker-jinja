from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

def db_connect():
	conn = sqlite3.connect("tasks.db")
	conn.row_factory = sqlite3.Row
	return conn


@app.route("/")
def dashboard():
	conn = db_connect()
	tasks = conn.execute("SELECT * FROM tasks").fetchall()
	conn.close()
	return render_template("dashboard.html", tasks = tasks)


@app.route("/addtask", methods=["GET", "POST"])
def add_task():

	if request.method == "POST":
		conn = db_connect()
		cursor = conn.cursor()
		cursor.execute(
			"INSERT INTO tasks (title, status) VALUES (?, ?)",
			(request.form["title"], request.form["status"])
			)

		conn.commit()
		task_id = cursor.lastrowid
		conn.close()

		return redirect(url_for("dashboard"))

	return render_template("addtask.html", tasks = db_connect())


@app.route("/edittask/<int:id>", methods = ["GET", "POST"])
def edit_task(id):

	conn = db_connect()
	conn.row_factory = sqlite3.Row
	cursor = conn.cursor()

	if request.method == "POST":
		method = request.form.get("_method", "POST").upper()

		if method == "PUT":
			cursor.execute(
				"UPDATE tasks SET title = ?, status = ? WHERE id = ?",
				(request.form["title"], request.form["status"], id)
				)

			conn.commit()
			conn.close()

			return redirect(url_for("dashboard"))

	cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
	task = cursor.fetchone()
	conn.close()

	return render_template("edittask.html", task = task)


@app.route("/deltask/<int:id>", methods = {"GET", "POST"})
def del_task(id):

	conn = db_connect()
	cursor = conn.cursor()

	if request.method == "POST":
		method = request.form.get("_method", "POST").upper()

		if method == "DELETE":
			cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
			conn.commit()
			conn.close()

			return redirect(url_for("dashboard"))

	cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
	task = cursor.fetchone()
	conn.close()

	return render_template("deltask.html", task = task)