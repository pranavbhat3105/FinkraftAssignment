from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"health": "UP"})

@app.route('/stress')
def stress():
    start_time = time.time()
    # Simulate CPU work - adjust the range to control load
    for i in range(1, 200000):
        _ = i * i
    return f"Processed load in {time.time() - start_time:.4f} seconds"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)