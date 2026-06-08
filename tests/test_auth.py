import pytest
from pages.login_page import LoginPage  # Imports your financial login page object

def test_invalid_login_lockout(driver):
    """
    TC-010: Invalid Login Authentication Lockout
    Validates that the portal rejects incorrect credentials and displays a clear error warning.
    """
    login_page = LoginPage(driver)
    
    # 1. Navigate to the secure financial portal
    login_page.load()
    
    # 2. Attempt to log in with invalid/unverified credentials
    login_page.login("unverified_user@finance.com", "WrongPassword123!")
    
    # 3. Retrieve the resulting system validation error message
    error_text = login_page.get_error_message()
    
    # 4. Assert that the strict corporate security warning is displayed
    assert "Username and password do not match any user in this service" in error_text, \
        f"Expected security warning not found! Instead, got: '{error_text}'"