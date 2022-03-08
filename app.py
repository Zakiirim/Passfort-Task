"""Run the application."""

from flask import Flask

from src.documents.api import documents

app = Flask(__name__)
app.register_blueprint(documents)

if __name__ == "__main__":
    app.run(debug=True)
