import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

@pytest.fixture(scope="function")
def driver():
    """
    Fixture to initialize the WebDriver before a test 
    and tear it down completely after the test finishes.
    """
    print("\n--- Initializing Chrome Browser ---")
    
    # Starts the Chrome browser session
    driver = webdriver.Chrome()
    
    # Standard engineering practices: maximize window and wait up to 10 seconds for elements to load
    driver.maximize_window()
    driver.implicitly_wait(10)
    
    # This passes the browser over to our test scripts
    yield driver
    
    # Teardown phase: Closes the browser safely after the test runs
    print("\n--- Closing Chrome Browser ---")
    driver.quit()