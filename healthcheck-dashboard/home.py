from flask import Flask, render_template, jsonify
import requests
from concurrent.futures import ThreadPoolExecutor
import logging

app = Flask(__name__)

# Configuration - This could be in a separate file or environment variables
services = {
    'srvA': 'xxxxx/health',
    'srvB': 'yyyyy/health',
    # Add more services here
}

# Setup logging
logging.basicConfig(filename='app.log', level=logging.INFO)

def check_service_health(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200 and response.json().get('status') == 'UP':
            return {'status': 'HEALTHY', 'color': 'green'}
        else:
            return {'status': 'UNHEALTHY', 'color': 'red'}
    except requests.RequestException:
        return {'status': 'DOWN', 'color': 'red'}

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/health')
def health_check():
    with ThreadPoolExecutor(max_workers=len(services)) as executor:
        results = {service: executor.submit(check_service_health, endpoint)
                   for service, endpoint in services.items()}
        health_status = {service: future.result() for service, future in results.items()}
    return jsonify(health_status)

if __name__ == '__main__':
    app.run(debug=True)
