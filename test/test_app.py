import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import app

def test_index():
    client = app.app.test_client()
    response = client.get('/')
    assert response.status_code == 200
