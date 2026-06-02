from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Standard engineering practice: Define your locators cleanly at the top of the class
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_CONTAINER = (By.CSS_SELECTOR, "[data-test='error']")

    def navigate_to_login(self):
        """Opens the standard global e-commerce sandbox practice page."""
        self.open_url("https://www.saucedemo.com/")

    def login_to_application(self, username, password):
        """Executes a complete login flow using our base page engine methods."""
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)

    def get_error_message(self):
        """Retrieves validation text when a login fails."""
        return self.find_element(self.ERROR_CONTAINER).text