from selenium.webdriver.common.by import By

class LoginLocators:
    CONTINUE_WITH_EMAIL_BTN = (By.XPATH, "//button[contains(., 'Continue with email')]")
    CONTINUE_BUTTON = (By.XPATH, "//button[.//span[text()='Continue']]")
    EMAIL_INPUT = (By.ID, "email")
    LOGIN_BUTTON = (By.XPATH, "//button[.//span[text()='Login']]")
    OTP_DISPLAY_TEXT = (By.CSS_SELECTOR, "p.login__otp-display")
    OTP_INPUT = (By.ID, "otp")
    SKIP_FOR_NOW_BTN = (By.XPATH, "//button[text()='Skip for now']")
