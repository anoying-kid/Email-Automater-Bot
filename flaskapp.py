from flask import Flask, render_template
import sqlite3

class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()

    def get_db_connection(self):
        conn = sqlite3.connect('mails.sqlite')
        conn.row_factory = sqlite3.Row
        return conn

    def setup_routes(self):
        @self.app.route('/')
        def index():
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users_emails')
            users = cursor.fetchall()
            conn.close()
            return render_template('index.html', users=users)

    def run(self, debug=True):
        self.app.run(debug=debug)

if __name__ == "__main__":
    flask_app = FlaskApp()
    flask_app.run()