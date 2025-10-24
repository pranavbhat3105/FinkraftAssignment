from flask import Flask, jsonify
import time

app = Flask(__name__)


@app.route('/')
def index():
    """Returns a simple success message for the root URL (/)"""
    # By default, returning a string will result in an HTTP 200 OK status.
    return "Welcome! The application is running." 
# ---------------------------------

@app.route('/health')
def health():
    return jsonify({"health": "UP"})

@app.route('/stress')
def stress():
    start_time = time.time()

    for i in range(1, 200000):
        _ = i * i
    return f"Processed load in {time.time() - start_time:.4f} seconds"

if __name__ == '__main__':
    # Note: Gunicorn usually handles running the app; this is for local testing.
    app.run(host='0.0.0.0', port=3000)
