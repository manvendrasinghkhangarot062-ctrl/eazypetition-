import os
import time
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from locators.login_locators import LoginLocators
from forms.form_485.locators_485 import Form485Locators

@pytest.fixture(scope="class", autouse=True)
def setup_browser(request):
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    driver.maximize_window()
    request.cls.driver = driver
    request.cls.wait = WebDriverWait(driver, 15)
    request.cls.project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    yield
    driver.quit()

@allure.feature("Form 485")
class TestForm485Allure:

    def verify_and_get_element(self, name, locator, wait_time=30):
        with allure.step(f"{name}"):
            try:
                element = WebDriverWait(self.driver, wait_time).until(EC.element_to_be_clickable(locator))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                time.sleep(0.5)
                assert element.is_displayed(), f"{name} is not displayed"
                assert element.is_enabled(), f"{name} is not enabled"
                return element
            except Exception as e:
                png_bytes = self.driver.get_screenshot_as_png()
                allure.attach(png_bytes, name=f"{name}_Failure", attachment_type=allure.attachment_type.PNG)
                with open(f"failure_screenshot_{name.replace(' ', '_')}.png", "wb") as f:
                    f.write(png_bytes)
                raise e

    def safe_click(self, name, element):
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)
            
    def safe_send_keys(self, name, element, text):
        element.clear()
        element.send_keys(text)
        time.sleep(1)

    @allure.story("Login")
    def test_01_login(self):
        self.driver.get("https://121.eazypetition.org/")
        
        login_btn = self.verify_and_get_element("Login Button Visible", LoginLocators.LOGIN_BUTTON)
        self.safe_click("Login Button", login_btn)
        
        continue_email = self.verify_and_get_element("Continue with Email Button Visible", LoginLocators.CONTINUE_WITH_EMAIL_BTN)
        self.safe_click("Continue with Email Button", continue_email)
        
        email_input = self.verify_and_get_element("Email Entered", LoginLocators.EMAIL_INPUT)
        self.safe_send_keys("Email Input", email_input, "manvendrasinghkhangarot062@gmail.com")
        
        continue_to_submit = self.verify_and_get_element("Continue Submit Button Visible", LoginLocators.CONTINUE_BUTTON)
        self.safe_click("Continue Submit Button", continue_to_submit)
        
        with allure.step("Extract OTP from screen"):
            import re
            otp_display = self.verify_and_get_element("OTP Display Text", LoginLocators.OTP_DISPLAY_TEXT)
            otp_text = otp_display.text
            otp_code = re.search(r'\d+', otp_text).group()
            
        otp_input = self.verify_and_get_element("OTP Entered", LoginLocators.OTP_INPUT)
        self.safe_send_keys("OTP Input", otp_input, otp_code)
        
        try:
            login_btn2 = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(LoginLocators.LOGIN_BUTTON))
            self.safe_click("Verify OTP Login Button", login_btn2)
        except: pass
            
        skip_btn = self.verify_and_get_element("Skip For Now Button Visible", LoginLocators.SKIP_FOR_NOW_BTN)
        self.safe_click("Skip For Now Button", skip_btn)
        
        self.verify_and_get_element("Dashboard Loaded", Form485Locators.NEW_PETITION_BTN)

    @allure.story("Petition Creation")
    def test_02_create_petition(self):
        new_pet_btn = self.verify_and_get_element("New Petition Clicked", Form485Locators.NEW_PETITION_BTN)
        self.safe_click("New Petition Clicked", new_pet_btn)
        
        search_input = self.verify_and_get_element("Form Search 485", Form485Locators.SEARCH_INPUT)
        self.safe_send_keys("Form Search 485", search_input, "485")
        
        select_form_btn = self.verify_and_get_element("Form Selected", Form485Locators.SELECT_FORM_BTN)
        self.safe_click("Form Selected", select_form_btn)
        
        checkbox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(Form485Locators.PRECONDITION_CHECKBOX))
        with allure.step("Precondition Checked"):
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", checkbox)
            
        continue_btn = self.verify_and_get_element("Continue Clicked", Form485Locators.CONTINUE_BTN)
        self.safe_click("Continue Clicked", continue_btn)
        
        time.sleep(10) # Pause so we can see the form layout
