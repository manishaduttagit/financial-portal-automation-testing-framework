import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def driver(request):
    options = webdriver.ChromeOptions()
    
    # Disable Chrome's built-in password manager and popups
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False
    }
    options.add_experimental_option("prefs", prefs)
    
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    
    # Initialize the automated driver instance
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    yield driver
    
    # --- AUTOMATED SCREENSHOT ENGINE ---
    # Create a screenshots directory in the root folder if it doesn't exist
    screenshot_dir = os.path.join(os.getcwd(), "screenshots")
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
        
    # Extract the name of the executing test case
    test_name = request.node.name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.join(screenshot_dir, f"{test_name}_{timestamp}.png")
    
    # Save the visual state of the browser automatically before quitting
    try:
        driver.save_screenshot(screenshot_path)
        print(f"\n--> Automated Documentation captured: screenshots/{test_name}_{timestamp}.png")
    except Exception as e:
        print(f"\n--> Failed to capture screenshot for {test_name}: {e}")
    # -----------------------------------
    
    # Secure teardown window destruction
    driver.quit()