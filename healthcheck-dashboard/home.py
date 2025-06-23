from flask import Flask, render_template, jsonify
import requests
from concurrent.futures import ThreadPoolExecutor
import logging
from flask_restx import Api, Resource, fields
from datetime import datetime

app = Flask(__name__)
api = Api(app, version='1.0', title='Service Health API', description='API for checking service health')

# Configuration - This could be in a separate file or environment variables
services = {
    'srvA': 'xxxxx/health',
    'srvB': 'yyyyy/health',
    # Add more services here
}

# Setup logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# Define the model for the health check response
health_model = api.model('HealthStatus', {
    'status': fields.String(description='The health status of the service', required=True, example='HEALTHY'),
    'last_checked': fields.DateTime(description='The time when the service was last checked', required=True, example='2023-11-11T00:00:00Z')
})

def check_service_health(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200 and response.json().get('status') == 'UP':
            return {'status': 'HEALTHY', 'last_checked': datetime.utcnow().isoformat() + 'Z'}
        else:
            return {'status': 'UNHEALTHY', 'last_checked': datetime.utcnow().isoformat() + 'Z'}
    except requests.RequestException:
        return {'status': 'DOWN', 'last_checked': datetime.utcnow().isoformat() + 'Z'}

@api.route('/api/health')
class HealthCheck(Resource):
    @api.doc(description="Get the health status of all services")
    @api.marshal_list_with(health_model)
    def get(self):
        with ThreadPoolExecutor(max_workers=len(services)) as executor:
            results = {service: executor.submit(check_service_health, endpoint) 
                       for service, endpoint in services.items()}
            health_status = {service: future.result() for service, future in results.items()}
        return jsonify(health_status)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
