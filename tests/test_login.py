import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_ui_001_successful_login(driver):
    """Scenario 1: Verify a user can log in successfully with valid credentials."""
    driver.get("https://www.saucedemo.com")
    
    # Direct element manipulation to ensure no Page Object dependencies fail
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "user-name"))).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    
    WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))
    assert "inventory.html" in driver.current_url


def test_ui_002_invalid_login_error(driver):
    """Scenario 2: Verify an explicit error message appears for invalid passwords."""
    driver.get("https://www.saucedemo.com")
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "user-name"))).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("wrong_sauce")
    driver.find_element(By.ID, "login-button").click()
    
    error_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h3[@data-test='error']"))
    )
    assert "Username and password do not match" in error_element.text