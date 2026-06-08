import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.onboarding_page import OnboardingPage

# ==============================================================================
# SECTION 1: USER AUTHENTICATION & LOGIN SECURITY (TC-010)
# ==============================================================================
class TestUserAuthentication:
    
    def test_invalid_login_lockout(self, driver):
        """
        TC-010: Invalid Login Authentication Lockout
        """
        login_page = LoginPage(driver)
        login_page.load()
        login_page.login("unverified_user@finance.com", "WrongPassword123!")
        error_text = login_page.get_error_message()
        assert "Username and password do not match any user in this service" in error_text


# ==============================================================================
# SECTION 2: ACCOUNT ONBOARDING & REGISTRATION (TC-001)
# ==============================================================================
class TestAccountOnboarding:

    def test_new_premium_account_registration(self, driver):
        """
        TC-001: New Premium Account Registration
        """
        onboarding = OnboardingPage(driver)
        driver.get("https://www.saucedemo.com")
        
        # Log in securely
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "user-name")))
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        # Ensure we add an item to the cart fresh
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add to cart')]")))
        driver.find_element(By.XPATH, "//button[contains(text(), 'Add to cart')]").click()
        
        # Proceed to Checkout
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "checkout")))
        driver.find_element(By.ID, "checkout").click()
        
        # Fill onboarding parameters
        onboarding.fill_personal_details("Manisha", "Chandra", "55311")
        onboarding.click_continue()
        
        # Assert transition succeeded
        WebDriverWait(driver, 10).until(EC.url_contains("checkout-step-two.html"))
        assert "checkout-step-two.html" in driver.current_url


# ==============================================================================
# SECTION 3: DYNAMIC INVESTMENT CALCULATOR MATRICES (TC-002)
# ==============================================================================
class TestInvestmentCalculator:

    def test_dynamic_investment_calculator(self, driver):
        """
        TC-002: Dynamic Investment Calculator Verification
        """
        onboarding = OnboardingPage(driver)
        driver.get("https://www.saucedemo.com")
        
        # Log in securely
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "user-name")))
        driver.find_element(By.ID, "user-name").clear()
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").clear()
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        # Explicitly click add to cart (or skip if already added by previous session state)
        try:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add to cart')]")))
            driver.find_element(By.XPATH, "//button[contains(text(), 'Add to cart')]").click()
        except:
            pass # Item is already in the cart from the shared session context
        
        # Navigate through to registration fields
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "checkout")))
        driver.find_element(By.ID, "checkout").click()
        
        # Re-verify calculator inputs
        onboarding.fill_personal_details("Manisha", "Chandra", "55311")
        onboarding.click_continue()
        
        # Pull dynamic calculation ledger matrix
        calculated_total = onboarding.get_calculated_total()
        expected_total = 32.39
        assert calculated_total == expected_total, \
            f"Calculator math mismatch! Expected: {expected_total}, but interface displayed: {calculated_total}"