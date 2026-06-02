from pages.login_page import LoginPage

def test_ui_001_successful_login(driver):
    """Scenario 1: Verify a user can log in successfully with valid credentials."""
    login_page = LoginPage(driver)
    
    # Action steps
    login_page.navigate_to_login()
    login_page.login_to_application("standard_user", "secret_sauce")
    
    # Assert step: Verify the URL updates to show we reached the inventory dashboard
    assert "inventory.html" in driver.current_url, "Login failed: Dashboard URL not reached."

def test_ui_002_invalid_login_error(driver):
    """Scenario 2: Verify an explicit error message appears for invalid passwords."""
    login_page = LoginPage(driver)
    
    # Action steps
    login_page.navigate_to_login()
    login_page.login_to_application("standard_user", "wrong_password")
    
    # Assert step: Verify the system safely flags the bad login attempts
    error_text = login_page.get_error_message()
    expected_error = "Username and password do not match any user in this service"
    
    assert expected_error in error_text, f"Expected error message not found. Got: '{error_text}'"