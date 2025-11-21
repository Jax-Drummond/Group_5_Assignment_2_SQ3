import sys
import os
import io
import pytest
import numpy as np
from PIL import Image
from model import preprocess_img, predict_result
from app import app

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

@pytest.fixture()
def client():
	with app.test_client() as client:
		yield client

def test_home_page_gives_status_code_200(client):
	response = client.get('/')
	assert response.status_code == 200

def test_home_page_has_title(client):
	response = client.get('/')
	assert b"Hand Sign Digit Language Detection" in response.data

def test_home_page_has_description(client):
	response = client.get('/')
	assert b"Aaaaaaaaa webapp to detect a digit using hand sign language." in response.data

def test_prediction_with_valid_file_shows_prediction(client):
	image = Image.open("test_images/0/Sign 0 (21).jpeg")
	image_bytes = io.BytesIO()
	image.save(image_bytes, format="JPEG")

	image_data = {
			"file": (image_bytes.getvalue(), "test.png")
	}

	response = client.post("/prediction", content_type="multipart/form-data", data=image_data)
	assert b"Prediction" in response.data

def test_prediction_with_invalid_file_shows_error_messages(client):
	blank_file = io.BytesIO(b"")
	blank_data = {
			"file": (blank_file, "blank.txt")
	}

	response = client.post("/prediction", content_type="multipart/form-data", data=blank_data)
	assert response.status_code == 200
	assert b"File cannot be processed." in response.data

def test_prediction_with_no_file_shows_error_message(client):
	response = client.post("/prediction", content_type="multipart/form-data", data={})
	assert b"File cannot be processed." in response.data

def test_predict_with_valid_image_predicts_integer():
	image = preprocess_img("test_images/0/Sign 0 (21).jpeg")
	prediction = predict_result(image)
	assert isinstance(prediction, (int, np.integer))

def test_predict_result_invalid_path():
	exception_caught = False
	try:
		predict_result("Nonexistentimage.jpeg")
	except:
		exception_caught = True

	assert exception_caught
