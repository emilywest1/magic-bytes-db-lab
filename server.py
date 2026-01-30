from flask import Flask, request, redirect, send_file
import sqlite3
import io
import os

app = Flask(__name__)
DB = "uploads.db"

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

JPEG_MAGIC = b"\xff\xd8\xff"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                filedata BLOB
            )
        """)

def allowed_extension(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

def valid_magic_bytes(data):
    if data.startswith(JPEG_MAGIC):
        return True
    if data.startswith(PNG_MAGIC):
        return True
    return False

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            return "No file uploaded", 400

        if not allowed_extension(file.filename):
            return "Invalid file extension", 400

        data = file.read()

        # ✅ Magic byte check (still insufficient)
        if not valid_magic_bytes(data):
            return "Invalid file signature", 400

        with sqlite3.connect(DB) as conn:
            conn.execute(
                "INSERT INTO uploads (filename, filedata) VALUES (?, ?)",
                (file.filename, data),
            )

        return redirect("/files")

    return """
        <h2>Upload Image</h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit">
        </form>
    """

@app.route("/files")
def list_files():
    with sqlite3.connect(DB) as conn:
        rows = conn.execute(
            "SELECT id, filename, length(filedata) FROM uploads"
        ).fetchall()

    out = "<h2>Stored Files</h2><ul>"
    for r in rows:
        out += f'<li>{r[1]} ({r[2]} bytes) - <a href="/file/{r[0]}">view</a></li>'
    out += "</ul>"
    return out

@app.route("/file/<int:file_id>")
def get_file(file_id):
    with sqlite3.connect(DB) as conn:
        row = conn.execute(
            "SELECT filename, filedata FROM uploads WHERE id = ?",
            (file_id,),
        ).fetchone()

    if not row:
        return "Not found", 404

    filename, data = row
    return send_file(
        io.BytesIO(data),
        download_name=filename,
        mimetype="image/jpeg"
    )

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
