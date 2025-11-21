import sys
import os
import pytest
from app import app
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

@pytest.fixture(scope="session", autouse=True)
def start_flask_server():
    import threading, time

    def run_app():
        app.run(port=5000, debug=False, use_reloader=False)

    thread = threading.Thread(target=run_app)
    thread.daemon = True
    thread.start()
    time.sleep(1)
    yield

# Test ID: test_accept_1
#
# Acceptance Criteria:
# Given a user wants to import an image to the website, when they import a valid image, the system must display the image as a preview for the user before submission.
#
# Test Steps:
# 1. Click on the choose file button
# 2. Navigate to the image file
# 3. Select the file and import it
#
# Expected Result:
# The image file is valid and is displayed in a preview box below the choose file button.
def test_import_valid_image_shows_preview():
	# Setup
    driver = webdriver.Chrome()

    # Arrange
    preview_image = None
    driver.get("http://127.0.0.1:5000")

    # Act
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(os.path.abspath("test_images/0/Sign 0 (21).jpeg"))

    preview_image = driver.find_element(By.ID, "imageResult")

    # Assert
    assert preview_image

    # Cleanup
    driver.quit()

# Test ID: test_accept_2
#
# Acceptance Criteria:
# Given a user wants to import an image to the website, when they import an invalid image and submit, the system displays an error message indicating the file cannot be processed.
#
# Test Steps:
# 1. Click on the choose file button
# 2. Navigate to a any file that is not an image
# 3. Select the file and import it
# 4. Click the submit button
#
# Expected Result:
# The website takes the user to the prediction page and informs them that the file could not be processed.
def test_import_invalid_image_and_submit_shows_error():
	# Setup
    driver = webdriver.Chrome()

    # Arrange
    error_message = None
    driver.get("http://127.0.0.1:5000")

    # Act
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(os.path.abspath("Readme.md"))

    submit_button = driver.find_element(By.CLASS_NAME, "btn.btn-primary.my-3")
    submit_button.submit()

    error_message = driver.find_element(By.XPATH, "//h2[text()='File cannot be processed.']")

    # Assert
    assert error_message

    # Cleanup
    driver.quit()
