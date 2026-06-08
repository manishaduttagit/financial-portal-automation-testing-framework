import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def driver():
    """
    Pytest fixture to initialize and tear down the Selenium WebDriver asset.
    Using scope='function' ensures a clean, fresh browser window for every single test case.
    """
    # 1. Setup Chrome options (e.g., maximizing the window for consistent UI element tracking)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    # 2. Automatically manage and initialize the Chrome driver binaries
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # 3. Yield control to the test case execution loop
    yield driver
    
    # 4. Teardown: Safely quit the browser session after the test finishes to free up MacBook memory
    driver.quit()