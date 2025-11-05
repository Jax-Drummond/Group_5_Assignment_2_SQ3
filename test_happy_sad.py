import os
import pytest
import io
import sys
from PIL import Image

from app import app

@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def test_image_bytes():
    
    image = Image.new("RGB", (300, 300), color="red")
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="JPEG")
    image_bytes.seek(0)
    return image_bytes
        
# Happy Path Test
def test_happy_path_valid_image_prediction(client, test_image_bytes):
    
    image_data = {
        "file": (test_image_bytes, "valid_image.jpg")
    }
    
    response = client.post(
        "/prediction",
        data=image_data,
        content_type="multipart/form-data"
    )
    
    # Assert that the system returns a prediction
    assert response.status_code == 200
    assert b"Prediction" in response.data
    assert b"5" in response.data

# Sad Path Test   

def test_sad_path_invalid_image_file(client):
    invalid_image_data = {
        "file": (io.BytesIO(b"not an image"), "invalid_image.txt")
    }

    response = client.post(
        "/prediction",
        data=invalid_image_data,
        content_type="multipart/form-data"
    )
    
    assert response.status_code == 200
    assert b"File cannot be processed" in response.data
