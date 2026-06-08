from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        # Pointing to a real, live secure login dashboard sandbox
        self.url = "https://www.saucedemo.com" 
        
        # --- Updated Web Locators for the Live Sandbox ---
        self.username_input = (By.ID, "user-name")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "login-button")
        self.error_message = (By.XPATH, "//h3[@data-test='error']")

    def load(self):
        """Navigates to the portal login page."""
        self.driver.get(self.url)

    def login(self, username, password):
        """Executes a secure login attempt."""
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.username_input))
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()

    def get_error_message(self):
        """Retrieves validation errors, like invalid password warnings."""
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.error_message))
        return self.driver.find_element(*self.error_message).text