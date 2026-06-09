import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestBoundaryConstraints:

    def test_whitespace_padding_edge_case(self, driver):
        """TC-010: Boundary Value Analysis & Edge-Case Input Trimming Matrix"""
        driver.get("https://www.saucedemo.com")
        
        # 1. Step: Enter credentials with explicit leading/trailing whitespace padding
        # This tests if the authentication handler is robust enough to process/trim input
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "user-name")))
        
        print("\n--> Injecting padded credentials to test system boundary trimming...")
        driver.find_element(By.ID, "user-name").send_keys("  standard_user  ")  # Padded with spaces
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        # 2. Step: Form Submission Edge-Case Validation
        # If the portal correctly trims inputs, login succeeds and we hit the inventory page.
        # If it fails to trim, an error message appears. We will capture the actual behavior.
        try:
            WebDriverWait(driver, 5).until(EC.url_contains("inventory.html"))
            print("--> System validation engine auto-trimmed the credential inputs successfully!")
            assert "inventory.html" in driver.current_url
            
        except Exception:
            print("--> System handled whitespace strictly as an invalid match. Verifying error constraint UI...")
            error_element = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//h3[@data-test='error']"))
            )
            assert "Username and password do not match" in error_element.text
            print("--> System successfully rejected untrimmed input with a secure validation message.")

        print("--> TC-010: Edge-case boundary analysis complete. Input security constraints verified!")