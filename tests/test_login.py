import time
import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import sys
import os

# Add the parent directory to the path so we can import locators
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from locators.login_locators import LoginLocators

class TestLogin:
    
    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("https://121.eazypetition.org/?step=part2")
        self.wait = WebDriverWait(self.driver, 10)
        yield
        self.driver.quit()

    def test_login_flow(self):
        # 1. Click Main Login Button on the page
        login_btn = self.wait.until(EC.presence_of_element_located(LoginLocators.LOGIN_BUTTON))
        try:
            self.driver.execute_script("arguments[0].click();", login_btn)
        except Exception as e:
            print("Force click failed:", e)
        time.sleep(2)

        # 2. Click Continue with Email
        continue_btn = self.wait.until(EC.element_to_be_clickable(LoginLocators.CONTINUE_WITH_EMAIL_BTN))
        continue_btn.click()
        time.sleep(2)

        # 3. Enter email
        email_input = self.wait.until(EC.visibility_of_element_located(LoginLocators.EMAIL_INPUT))
        email_input.send_keys("manvendrasinghkhangarot062@gmail.com") 
        time.sleep(1)
        
        # 3.5 Click Continue to submit email
        email_continue_btn = self.wait.until(EC.element_to_be_clickable(LoginLocators.CONTINUE_BUTTON))
        email_continue_btn.click()
        time.sleep(2)
        
        # 4. Wait for OTP to be displayed on screen and extract it
        otp_display_element = self.wait.until(EC.visibility_of_element_located(LoginLocators.OTP_DISPLAY_TEXT))
        otp_text = otp_display_element.text
        
        import re
        otp_code = re.search(r'\d+', otp_text).group()
        print(f"Extracted OTP: {otp_code}")
        time.sleep(1)
        
        # 5. Enter the extracted OTP
        otp_input = self.wait.until(EC.visibility_of_element_located(LoginLocators.OTP_INPUT))
        otp_input.send_keys(otp_code)
        time.sleep(1)
        
        # 6. Click Login to verify OTP
        try:
            login_btn2 = self.wait.until(EC.element_to_be_clickable(LoginLocators.LOGIN_BUTTON))
            login_btn2.click()
        except:
            pass # Ignore if it auto-submits OTP
            
        time.sleep(5)
        
        # 7. Click Skip for now
        skip_btn = self.wait.until(EC.element_to_be_clickable(LoginLocators.SKIP_FOR_NOW_BTN))
        skip_btn.click()
        time.sleep(5)
        
        print("Login flow completed successfully!")
