from flask import Flask, request, render_template, redirect, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

# Create database
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS comments (user TEXT, text TEXT, time TEXT)")
    conn.commit()
    conn.close()

init_db()

secure_mode = False

@app.route("/", methods=["GET", "POST"])
def home():
    global secure_mode

    # 🔐 FORCE LOGIN FIRST
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    if request.method == "POST":

        if "toggle" in request.form:
            secure_mode = not secure_mode

        elif "clear" in request.form:
            c.execute("DELETE FROM comments")

        else:
            user = session["user"]
            text = request.form.get("comment")
            time = datetime.now().strftime("%H:%M:%S")

            c.execute("INSERT INTO comments VALUES (?, ?, ?)", (user, text, time))

        conn.commit()

    c.execute("SELECT * FROM comments")
    data = c.fetchall()
    conn.close()

    return render_template("index.html", comments=data, secure=secure_mode, user=session["user"])


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = request.form.get("username")
        return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()   # user remove
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)