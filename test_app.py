

import pytest
# Import the Flask application instance from your main app.py file
from app import app 


# This client simulates requests to your app without running the actual server.
@pytest.fixture
def client():
    # Set the TESTING config flag to True for error handling
    app.config['TESTING'] = True
    
    # Use the test_client to set up the environment
    with app.test_client() as client:
        # 'yield' makes this code run before and after the test function
        yield client 

# --- Test Functions ---

def test_root_status(client):
    """Verify the root endpoint ('/') returns a 200 OK status."""
    response = client.get('/')
    assert response.status_code == 200

def test_stress_endpoint_status(client):
    """Verify the /stress endpoint returns a 200 OK status."""
    response = client.get('/stress')
    assert response.status_code == 200
    
