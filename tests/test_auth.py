import pytest
from selenium.webdriver.common.by import By
# --- ADDED IMPORTS FOR SMART WAITS ---
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# -------------------------------------
from pages.login_page import LoginPage
from pages.onboarding_page import OnboardingPage

# ==============================================================================
# SECTION 1: USER AUTHENTICATION & LOGIN SECURITY (TC-010)
# ==============================================================================
class TestUserAuthentication:
    
    def test_invalid_login_lockout(self, driver):
        """
        TC-010: Invalid Login Authentication Lockout
        Validates that the portal rejects incorrect credentials and displays a warning.
        """
        login_page = LoginPage(driver)
        
        # 1. Navigate to secure portal
        login_page.load()
        
        # 2. Attempt login with bad credentials
        login_page.login("unverified_user@finance.com", "WrongPassword123!")
        
        # 3. Retrieve system error
        error_text = login_page.get_error_message()
        
        # 4. Assert the warning matches expectations
        assert "Username and password do not match any user in this service" in error_text


# ==============================================================================
# SECTION 2: ACCOUNT ONBOARDING & REGISTRATION (TC-001)
# ==============================================================================
class TestAccountOnboarding:

    def test_new_premium_account_registration(self, driver):
        """
        TC-001: New Premium Account Registration
        Validates that entering valid profile data submits the form cleanly.
        """
        onboarding = OnboardingPage(driver)
        
        # 1. Prerequisite: Quick login to get past the security gate
        driver.get("https://www.saucedemo.com")
        
        # Explicit wait to ensure login inputs are fully loaded
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "user-name")))
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        # 2. Add the first available item to the cart using a reliable button text match
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Add to cart']")))
        driver.find_element(By.XPATH, "//button[text()='Add to cart']").click()
        
        # 3. Click the shopping cart icon
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        
        # 4. Click the Checkout button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "checkout")))
        driver.find_element(By.ID, "checkout").click()
        
        # 5. Input profile details using our Page Object Model
        onboarding.fill_personal_details("Manisha", "Chandra", "55311")
        
        # 6. Submit parameters
        onboarding.click_continue()
        
        # 7. Assert browser redirected forward without validation flags
        assert "checkout-step-two.html" in driver.current_url, \
            f"Registration failed to advance! Stuck on: {driver.current_url}"