from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OnboardingPage:
    def __init__(self, driver):
        self.driver = driver
        # Sandbox registration and calculator URL
        self.url = "https://www.saucedemo.com/checkout-step-one.html" 
        
        # --- Web Locators for TC-001, TC-002, & TC-003 ---
        self.first_name = (By.ID, "first-name")
        self.last_name = (By.ID, "last-name")
        self.postal_code = (By.ID, "postal-code")
        self.continue_button = (By.ID, "continue")
        
        # Locators mapped to simulate our advanced financial edge cases
        self.error_container = (By.XPATH, "//h3[@data-test='error']")

    def load(self):
        """Navigates directly to the onboarding stage."""
        self.driver.get(self.url)

    def fill_personal_details(self, first, last, zip_code):
        """Fills out the core profile registration fields."""
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.first_name))
        self.driver.find_element(*self.first_name).send_keys(first)
        self.driver.find_element(*self.last_name).send_keys(last)
        self.driver.find_element(*self.postal_code).send_keys(zip_code)

    def click_continue(self):
        """Submits the current onboarding screen data."""
        self.driver.find_element(*self.continue_button).click()

    def get_validation_error(self):
        """Captures registration or age verification constraint errors."""
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.error_container))
        return self.driver.find_element(*self.error_container).text

        
        
    def get_calculated_total(self):
        """
        Extracts the dynamic final calculation total from the interface.
        Cleans the string data so it can be verified mathematically.
        """
        total_locator = (By.CLASS_NAME, "summary_total_label")
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(total_locator))
        
        # Retrieves text like "Total: $32.39"
        raw_total_text = self.driver.find_element(*total_locator).text
        
        # Cleans out the text to isolate just the numeric value
        numeric_value = raw_total_text.replace("Total: $", "").strip()
        return float(numeric_value)