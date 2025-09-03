from flask import Flask, jsonify, render_template
import pymysql
import os

app = Flask(__name__, template_folder='templates')

# Read DB connection details from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "testdb")

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flask & MySQL DB Connection</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f0f2f5;
                color: #333;
            }
            .container {
                text-align: center;
                background: #fff;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #4CAF50;
                font-size: 2.5em;
                margin-bottom: 0.5em;
            }
            .status {
                font-size: 1.2em;
                color: #555;
                margin-bottom: 20px;
            }
            .status strong {
                color: #2e7d32;
            }
            .info {
                font-size: 1em;
                color: #777;
                margin-bottom: 30px;
                line-height: 1.5;
            }
            .button-link {
                display: inline-block;
                padding: 12px 24px;
                background-color: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                transition: background-color 0.3s ease, transform 0.2s ease;
                font-weight: bold;
            }
            .button-link:hover {
                background-color: #0056b3;
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>

        <div class="container">
            <h1>✅ Flask App Connected!</h1>
            <p class="status">Your application is <strong>successfully connected</strong> to the MySQL (RDS) database.</p>
            <p class="info">
                This is a simple front page to confirm the status of your app. 
                The backend is set up to read database credentials from environment variables 
                and retrieve user data.
            </p>
            <a href="/users" class="button-link">View User Data</a>
        </div>

    </body>
    </html>
    """

@app.route("/users")
def get_users():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM users;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
