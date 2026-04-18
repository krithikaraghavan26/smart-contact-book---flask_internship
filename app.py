from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
app = Flask(__name__)
app.secret_key = "mini_project_key"
def get_db_connection():
    conn = sqlite3.connect("contacts.db")

#    conn.execute("""
#        CREATE TABLE IF NOT EXISTS contacts (
#        id INTEGER PRIMARY KEY AUTOINCREMENT,
#        name TEXT NOT NULL,
#        phone TEXT NOT NULL,
#        email TEXT NOT NULL
#       )
#   """)
#    conn.commit()

    conn.row_factory = sqlite3.Row
    return conn
@app.route("/")
def home():
    conn = get_db_connection()
    count = conn.execute("SELECT COUNT(*) FROM contacts").fetchone()[0]
    conn.close()
    return render_template("home.html", total=count)
@app.route("/add-contact", methods=["GET", "POST"])
def add_contact():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        if not name or not phone or not email:
            flash("All fields are required!")
            return redirect(url_for("add_contact"))
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
            (name, phone, email)
        )
        conn.commit()
        conn.close()
        flash("Contact added successfully!")
        return redirect(url_for("view_contacts"))
    return render_template("add_contact.html")
@app.route("/contacts")
def view_contacts():
    conn = get_db_connection()
    contacts = conn.execute("SELECT * FROM contacts").fetchall()
    conn.close()
    return render_template("view_contacts.html", contacts=contacts)
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        flash("Thank you for your feedback!")
        return redirect(url_for("home"))
    return render_template("feedback.html")
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
