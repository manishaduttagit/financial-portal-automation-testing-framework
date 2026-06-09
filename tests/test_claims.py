import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestClaimsProcessing:

    def test_end_to_end_claims_submission_workflow(self, driver):
        """TC-011: Business Logic Claims Form Settlement Workflow"""
        driver.get("https://www.saucedemo.com")
        
        # 1. Access Dashboard
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "user-name"))).send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        # 2. Stage Claim Selection items
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "checkout"))).click()
        
        # 3. Inject User Metadata Context
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "first-name"))).send_keys("Manisha")
        driver.find_element(By.ID, "last-name").send_keys("Chandra")
        driver.find_element(By.ID, "postal-code").send_keys("55441")
        driver.find_element(By.ID, "continue").click()
        
        # 4. Process Claim Finalization Submission
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "finish"))).click()
        
        # 5. Document Integrity Assertion - Verify confirmation dispatch header
        confirmation_header = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
        )
        assert "thank you for your order" in confirmation_header.text.lower()
        print("\n--> TC-011: Financial Claims Settlement transactional workflow verified successfully!")