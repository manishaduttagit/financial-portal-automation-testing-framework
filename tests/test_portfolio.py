import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class TestPortfolioDashboard:

    def test_multi_currency_balance_rendering(self, driver):
        """TC-004: Multi-Currency Account Balance Portfolio Verification"""
        driver.get("https://www.saucedemo.com")
        
        # Secure Login
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "user-name"))).send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        # Locate inventory prices
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item_price")))
        price_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        
        # Extract and validate currency format parsing accuracy
        for element in price_elements:
            raw_price_text = element.text
            assert raw_price_text.startswith("$"), f"Expected USD symbol ($), but found: {raw_price_text}"
            numeric_value = float(raw_price_text.replace("$", "").strip())
            assert numeric_value > 0.00, f"Invalid asset balance: {numeric_value}"


    def test_ledger_sorting_matrix(self, driver):
        """TC-005: Real-Time Transaction Ledger Sorting Matrix (Z to A)"""
        driver.get("https://www.saucedemo.com")
        
        # 1. Step: Access Dashboard
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "user-name"))).send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        # 2. Step: Target the Sorting Dropdown element using Select wrapper
        dropdown_locator = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "product_sort_container"))
        )
        sort_select = Select(dropdown_locator)
        
        # 3. Step: Switch filter to "Name (Z to A)" using its native HTML option value attribute
        sort_select.select_by_value("za")
        
        # 4. Step: Extract the newly arranged asset names from the interface
        asset_names = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        actual_titles = [element.text for element in asset_names]
        
        print(f"\n--> Extracted Current Sorted UI Order: {actual_titles}")
        
        # 5. Step: Programmatically sort the list in reverse order to verify UI behavior match
        expected_sorted_order = sorted(actual_titles, reverse=True)
        
        # Core Matrix Assertion
        assert actual_titles == expected_sorted_order, \
            f"Sorting Engine Discrepancy! Expected order: {expected_sorted_order}, but UI showed: {actual_titles}"
            
        print("--> TC-005: Ledger sorting matrix successfully validated via strict reverse-alphabetical assertion!")