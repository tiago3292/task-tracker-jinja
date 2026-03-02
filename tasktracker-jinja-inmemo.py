from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
tasks = [
	{"id":1, "title":"Learn Flask", "status":"Complete"}
]

@app.route("/")
def dashboard():
	return render_template("dashboard.html", tasks = tasks)

@app.route("/addtask", methods=["GET", "POST"])
def add_task():

	if request.method == "POST":

		if not request.form["title"] or not request.form["status"]:
			return render_template("adderror.html")

		task = {
		"id": len(tasks) + 1,
		"title": request.form["title"],
		"status": request.form["status"]
		}

		tasks.append(task)
		return redirect(url_for("dashboard"))

	return render_template("addtask.html", tasks = tasks)

@app.route("/edittask/<int:id>", methods = ["GET", "POST"])
def edit_task(id):

	task = next((t for t in tasks if t["id"] == id), None)

	if request.method == "POST":
		method = request.form.get("_method", "POST").upper()
		if method == "PUT":

			if not request.form["title"] or not request.form["status"]:
				return render_template("editerror.html", task=task)

			task["title"] = request.form["title"]
			task["status"] = request.form["status"]

			return redirect(url_for("dashboard"))

	return render_template("edittask.html", task = task)


@app.route("/deltask/<int:id>", methods = {"GET", "POST"})
def del_task(id):

	task = next((t for t in tasks if t["id"] == id), None)

	if request.method == "POST":
		method = request.form.get("_method", "POST").upper()
		if method == "DELETE":
			tasks.remove(task)
			return redirect(url_for("dashboard"))

	return render_template("deltask.html", task = task)