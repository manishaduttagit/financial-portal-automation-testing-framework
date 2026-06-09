import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestDashboardContent:

    def test_async_dynamic_content_rendering(self, driver):
        """TC-008: Fault-Tolerant Dynamic Content & Asynchronous Element Loading"""
        driver.get("https://www.saucedemo.com")
        
        # Access portal core via standardized authentication
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "user-name"))).send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        # Click on item header text to open details page
        item_link_locator = (By.ID, "item_4_title_link")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(item_link_locator)).click()
        
        # Explicit wait for details rendering
        detail_name_locator = (By.CLASS_NAME, "inventory_details_name")
        WebDriverWait(driver, 12).until(EC.visibility_of_element_located(detail_name_locator))
        
        extracted_title = driver.find_element(*detail_name_locator).text
        extracted_price = driver.find_element(By.CLASS_NAME, "inventory_details_price").text
        
        assert len(extracted_title) > 0, "Data Integrity Failure: Asset Title loaded empty!"
        assert "Backpack" in extracted_title, f"Content Mismatch! Expected Backpack, got: {extracted_title}"
        assert "$" in extracted_price, "Format Error: Currency descriptor missing from element price block."


    def test_broken_assets_and_dead_links(self, driver):
        """TC-009: Broken Link & Dead Asset Matrix (Hybrid UI/API Validation)"""
        driver.get("https://www.saucedemo.com")
        
        # 1. Step: Login to Dashboard
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "user-name"))).send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        # 2. Step: Scrape all image tags present on the inventory page
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item_img")))
        images = driver.find_elements(By.TAG_NAME, "img")
        
        print(f"\n--> Discovered {len(images)} active visual components in UI tree. Initiating network scans...")
        
        # 3. Step: Loop through each image component and verify the source link via HTTP requests
        for img in images:
            img_src = img.get_attribute("src")
            
            if not img_src:
                continue
                
            # Clean any leading/trailing whitespace and make it lowercase for validation
            clean_src = img_src.strip().lower()
            
            # STRICT HTTP FILTER: Only process actual web URLs. Ignore all base64 data strings.
            if not (clean_src.startswith("http://") or clean_src.startswith("https://")):
                print(f"--> Skipping non-HTTP asset string: {clean_src[:30]}...")
                continue
                
            try:
                # Fire an optimized network request to check the asset status code
                response = requests.head(img_src, timeout=5)
                
                # Check for 404 (Not Found) or 500 errors
                assert response.status_code < 400, \
                    f"Dead Asset Discovered! Link: {img_src} returned broken HTTP code: {response.status_code}"
                    
            except requests.RequestException as net_error:
                pytest.fail(f"Network handshake failure reaching asset: {img_src}. Error: {net_error}")
                
        print("--> TC-009: Asset parsing matrix complete. Zero broken resources detected!")