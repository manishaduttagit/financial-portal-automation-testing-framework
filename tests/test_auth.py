import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestUserAuthentication:
    def test_invalid_login_lockout(self, driver):
        """Scenario: Verify system lockout rules for flagged users."""
        driver.get("https://www.saucedemo.com")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "user-name"))).send_keys("locked_out_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        error_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h3[@data-test='error']"))
        )
        assert "Sorry, this user has been locked out" in error_box.text

class TestAccountOnboarding:
    def test_new_premium_account_registration(self, driver):
        """TC-001: New Premium Account Registration"""
        driver.get("https://www.saucedemo.com")
        
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "user-name"))).send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "checkout"))).click()
        
        # Verify arrival at Onboarding Profile form
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "first-name")))
        assert "checkout-step-one.html" in driver.current_url

class TestInvestmentCalculator:
    def test_dynamic_investment_calculator(self, driver):
        """TC-002: Dynamic Investment Calculator Verification"""
        driver.get("https://www.saucedemo.com")
        
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "user-name"))).send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "checkout"))).click()
        
        # Process calculation wizard fields
        driver.find_element(By.ID, "first-name").send_keys("Manisha")
        driver.find_element(By.ID, "last-name").send_keys("Chandra")
        driver.find_element(By.ID, "postal-code").send_keys("55441")
        driver.find_element(By.ID, "continue").click()
        
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "summary_subtotal_label")))
        assert "checkout-step-two.html" in driver.current_url

class TestFormValidationConstraints:
    def test_missing_onboarding_fields_error(self, driver):
        """TC-003: Form Validation Constraints"""
        driver.get("https://www.saucedemo.com")
        
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "user-name"))).send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "checkout"))).click()
        
        # Click continue with intentionally blank name fields to trigger layout constraint logic
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "continue"))).click()
        
        error_banner = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h3[@data-test='error']"))
        )
        assert "Error: First Name is required" in error_banner.text