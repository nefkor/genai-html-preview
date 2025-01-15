import pytest
from flask import jsonify

# Import your app (assuming main.py is in the same directory)
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True  # Important: enable testing mode
    with app.test_client() as client:
        yield client


def test_convert_text_success(client, mocker):
    mock_predict = mocker.patch('google.cloud.aiplatform.Model.predict')
    mock_predict.return_value = MockResponse(predictions=[{'content': '<p>Test HTML</p>'}])

    data = {'text': 'some example text'}
    response = client.post('/convert', json=data)

    assert response.status_code == 200
    assert response.get_json() == {'html': '<p>Test HTML</p>'}

def test_convert_text_no_text(client):
    response = client.post('/convert', json={}) # No "text" key provided
    assert response.status_code == 400
    assert response.get_json() == {'error': 'No text provided'}


# Mock Response class
class MockResponse:
    def __init__(self, predictions):
        self.predictions = predictions
