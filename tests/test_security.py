import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestSessionSecurity:

    def test_sso_external_link_tab_handshake(self, driver):
        """TC-006: Secure Single-Sign-On (SSO) External Link Authentication & Tab Handshake"""
        driver.get("https://www.saucedemo.com")
        
        # 1. Step: Login to establish parent session view
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "user-name"))).send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        # Capture the original unique window ID handle for reference
        parent_window_handle = driver.current_window_handle
        
        # 2. Step: Click the external social portal link (this opens a brand new browser tab)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "social_twitter"))).click()
        
        # 3. Step: Dynamic Wait for the browser engine to register the new tab handle window count
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 2)
        
        # Extract all active tab ID handles
        all_window_handles = driver.window_handles
        
        # 4. Step: Context Switching Loop - Move Selenium's control focus onto the new tab
        new_tab_handle = [handle for handle in all_window_handles if handle != parent_window_handle][0]
        driver.switch_to.window(new_tab_handle)
        
        # 5. Step: Execute multi-tab URL parsing security validation on the external site
        WebDriverWait(driver, 15).until(EC.url_contains("x.com"))
        current_tab_url = driver.current_url
        
        print(f"\n--> Successfully switched context to external tab! URL: {current_tab_url}")
        assert "x.com" in current_tab_url or "twitter.com" in current_tab_url, \
            f"Security Handshake Mismatch! Tab routed to unverified destination: {current_tab_url}"
        
        # 6. Step: Clean up and teardown - Close the external tab and securely switch focus back to parent
        driver.close()
        driver.switch_to.window(parent_window_handle)
        
        # Confirm parent scope is active by checking dashboard visibility
        assert "inventory.html" in driver.current_url
        print("--> TC-006 (SSO / Tab Switch): Multi-window state matrix executed and validated flawlessly!")


    def test_responsive_ui_mobile_breakpoint(self, driver):
        """TC-007: Responsive UI Component Layout Validation"""
        driver.get("https://www.saucedemo.com")
        
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "user-name"))).send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        print("\n--> Compressing browser viewport to mobile dimensions (375x812)...")
        driver.set_window_size(375, 812)
        
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item")))
        cart_link = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        assert cart_link.is_displayed(), "Layout Mismatch! Shopping cart icon hidden or clipped on mobile viewpoint."
        
        driver.set_window_size(1920, 1080)
        print("--> TC-007: Responsive UI breakpoint validation completed successfully!")