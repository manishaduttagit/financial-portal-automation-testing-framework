import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def driver(request):
    options = webdriver.ChromeOptions()
    
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    yield driver
    
    # --- ENTERPRISE AUTOMATED SCREENSHOT ENGINE ---
    screenshot_dir = os.path.join(os.getcwd(), "screenshots")
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
        
    # Extract the test name and create a clean, timestamp-free file path
    test_name = request.node.name
    screenshot_path = os.path.join(screenshot_dir, f"{test_name}.png")
    
    try:
        driver.save_screenshot(screenshot_path)
    except Exception as e:
        print(f"\n--> Failed to capture screenshot for {test_name}: {e}")
    # ----------------------------------------------
    
    driver.quit()