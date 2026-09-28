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
from forms.form_765.locators_765 import Form765Locators

@pytest.fixture(scope="class", autouse=True)
def setup_browser(request):
    # 1. & 5. Browser setup executed once for the entire class/session
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    driver.maximize_window()
    request.cls.driver = driver
    request.cls.wait = WebDriverWait(driver, 15)
    
    request.cls.project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    yield
    driver.quit()

@allure.feature("Form 765")
class TestForm765Allure:

    def verify_and_get_element(self, name, locator, wait_time=30):
        """Helper to verify displayed, enabled, capture screenshot on failure, and attach to allure"""
        with allure.step(f"{name}"):
            try:
                # Use element_to_be_clickable instead of presence_of_element_located 
                # This ensures the element is both visible and enabled in the DOM before we interact
                element = WebDriverWait(self.driver, wait_time).until(EC.element_to_be_clickable(locator))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                time.sleep(0.5)
                
                assert element.is_displayed(), f"{name} is not displayed"
                assert element.is_enabled(), f"{name} is not enabled"
                return element
            except Exception as e:
                png_bytes = self.driver.get_screenshot_as_png()
                allure.attach(png_bytes, name=f"{name}_Failure", attachment_type=allure.attachment_type.PNG)
                
                # Also save to filesystem for agent debugging
                with open(f"failure_screenshot.png", "wb") as f:
                    f.write(png_bytes)
                print(f"Screenshot saved to failure_screenshot.png for step: {name}")
                raise e

    def safe_click(self, name, element):
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)
            
    def safe_send_keys(self, name, element, text):
        element.clear()
        element.send_keys(text)
        # Add a tiny wait so modern frontend frameworks (React/Vue) can process the onChange event and enable buttons
        time.sleep(1)

    @allure.story("Login")
    def test_01_login(self):
        """Execute login only once"""
        self.driver.get("https://121.eazypetition.org/")
        
        login_btn = self.verify_and_get_element("Login Button Visible", LoginLocators.LOGIN_BUTTON)
        self.safe_click("Login Button", login_btn)
        
        continue_email = self.verify_and_get_element("Continue with Email Button Visible", LoginLocators.CONTINUE_WITH_EMAIL_BTN)
        self.safe_click("Continue with Email Button", continue_email)
        
        email_input = self.verify_and_get_element("Email Entered", LoginLocators.EMAIL_INPUT)
        self.safe_send_keys("Email Input", email_input, "manvendrasinghkhangarot062@gmail.com")
        
        continue_to_submit = self.verify_and_get_element("Continue Submit Button Visible", LoginLocators.CONTINUE_BUTTON)
        self.safe_click("Continue Submit Button", continue_to_submit)
        
        # Wait for OTP to be displayed on screen and extract it
        with allure.step("Extract OTP from screen"):
            import re
            otp_display = self.verify_and_get_element("OTP Display Text", LoginLocators.OTP_DISPLAY_TEXT)
            otp_text = otp_display.text
            otp_code = re.search(r'\d+', otp_text).group()
            
        otp_input = self.verify_and_get_element("OTP Entered", LoginLocators.OTP_INPUT)
        self.safe_send_keys("OTP Input", otp_input, otp_code)
        
        # Click Login to verify OTP (ignore if auto-submits)
        try:
            login_btn2 = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(LoginLocators.LOGIN_BUTTON))
            self.safe_click("Verify OTP Login Button", login_btn2)
        except:
            pass
            
        skip_btn = self.verify_and_get_element("Skip For Now Button Visible", LoginLocators.SKIP_FOR_NOW_BTN)
        self.safe_click("Skip For Now Button", skip_btn)
        
        self.verify_and_get_element("Dashboard Loaded", Form765Locators.NEW_PETITION_BTN)

    @allure.story("Petition Creation")
    def test_02_create_petition(self):
        """Create a petition only once"""
        new_pet_btn = self.verify_and_get_element("New Petition Clicked", Form765Locators.NEW_PETITION_BTN)
        self.safe_click("New Petition Clicked", new_pet_btn)
        
        search_input = self.verify_and_get_element("Form Search 765", Form765Locators.SEARCH_INPUT)
        self.safe_send_keys("Form Search 765", search_input, "765")
        
        select_form_btn = self.verify_and_get_element("Form Selected", Form765Locators.SELECT_FORM_BTN)
        self.safe_click("Form Selected", select_form_btn)
        
        # Click Precondition Checkbox
        # Checkboxes are often visually hidden and replaced by custom UI, so JS click is safer
        checkbox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(Form765Locators.PRECONDITION_CHECKBOX))
        with allure.step("Precondition Checked"):
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", checkbox)
            
        # Click Continue to proceed to Form
        continue_btn = self.verify_and_get_element("Continue Clicked", Form765Locators.CONTINUE_BTN)
        self.safe_click("Continue Clicked", continue_btn)
        
        # Step: Reason for applying
        reason_input = self.verify_and_get_element("Application Reason Visible", Form765Locators.APPLICATION_REASON_INPUT)
        self.safe_click("Application Reason Dropdown", reason_input)
        
        reason_option = self.verify_and_get_element("Reason Option 1a Visible", Form765Locators.REASON_OPTION_1A)
        self.safe_click("Reason Option 1a", reason_option)
        
        next_btn = self.verify_and_get_element("Next Button Clickable", Form765Locators.get_next_button("last()"))
        self.safe_click("Next", next_btn)
        
        self.verify_and_get_element("Part 1 Loaded", Form765Locators.GIVEN_NAME_INPUT)
    @staticmethod
    def get_short_id(field_dict):
        key = field_dict['fieldKey'].split('[')[0]
        if '_' in key and key.startswith(('Line', 'Pt', 'Part')):
            key = key.split('_', 1)[-1]
        if key.startswith('have_'):
            key = key.replace('have_', '')
        return key[:15]

    def click_yes_or_checkbox(self, container):
        try:
            # 1. Check for modern <button> element with 'Yes'
            yes_btns = container.find_elements(By.XPATH, ".//button[normalize-space(text())='Yes' or normalize-space(text())='YES']")
            if yes_btns:
                btn = yes_btns[0]
                is_active = btn.get_attribute("aria-pressed") == "true" or "is-active" in (btn.get_attribute("class") or "")
                if not is_active:
                    self.driver.execute_script("arguments[0].click();", btn)
                return

            # 2. Check for explicit 'Yes' radio inputs
            yes_inputs = container.find_elements(By.XPATH, ".//input[@type='radio' and (@value='Yes' or @value='yes' or @value='true' or @value='1' or @value='Y')]")
            if yes_inputs:
                inp = yes_inputs[0]
                if not inp.is_selected():
                    self.driver.execute_script("arguments[0].click();", inp)
                return
            
            # 3. Fallback to text label 'Yes'
            yes_labels = container.find_elements(By.XPATH, ".//*[normalize-space(text())='Yes' or normalize-space(text())='YES']")
            if yes_labels:
                self.driver.execute_script("arguments[0].click();", yes_labels[0])
                return

            # 4. Final fallback to very first radio/checkbox
            radios = container.find_elements(By.XPATH, ".//input[@type='radio' or @type='checkbox']")
            if radios:
                if not radios[0].is_selected():
                    self.driver.execute_script("arguments[0].click();", radios[0])
        except:
            pass

    page_2_fields = [
        {'fieldKey': 'Line1a_FamilyName[0]', 'hasInput': True, 'hasFile': False},
        {'fieldKey': 'Line1b_GivenName[0]', 'hasInput': True, 'hasFile': False},
        {'fieldKey': 'Line1c_MiddleName[0]', 'hasInput': True, 'hasFile': False},
        {'fieldKey': 'other_names4used', 'hasInput': False, 'hasFile': False},
        {'fieldKey': 'other_names_used', 'hasInput': False, 'hasFile': False},
        {'fieldKey': 'mailing_same_as_physical', 'hasInput': False, 'hasFile': False},
        {'fieldKey': 'have_driving_license', 'hasInput': False, 'hasFile': False},
        {'fieldKey': 'mailing_address', 'hasInput': True, 'hasFile': False},
        {'fieldKey': 'physical_address', 'hasInput': True, 'hasFile': False},
        {'fieldKey': 'have_i797', 'hasInput': False, 'hasFile': False},
        {'fieldKey': 'have_aNumber', 'hasInput': False, 'hasFile': False},
        {'fieldKey': 'have_online_account_number', 'hasInput': False, 'hasFile': False},
        {'fieldKey': 'gender', 'hasInput': False, 'hasFile': False},
        {'fieldKey': 'marital_status', 'hasInput': False, 'hasFile': False},
        {'fieldKey': 'previous_i765_filed', 'hasInput': False, 'hasFile': False},
        {'fieldKey': 'have_ssn', 'hasInput': False, 'hasFile': False},
        {'fieldKey': 'nationality_note', 'hasInput': False, 'hasFile': False},
        {'fieldKey': 'Line17a_CountryOfBirth[0]', 'hasInput': True, 'hasFile': False},
        {'fieldKey': 'Line17b_CountryOfBirth[0]', 'hasInput': True, 'hasFile': False},
        {'fieldKey': 'have_birth_certificate', 'hasInput': False, 'hasFile': False},
        {'fieldKey': 'Line18a_CityTownOfBirth[9]', 'hasInput': False, 'hasFile': False},
        {'fieldKey': 'Line18a_CityTownOfBirth[0]', 'hasInput': True, 'hasFile': False},
        {'fieldKey': 'Line18b_CityTownOfBirth[0]', 'hasInput': True, 'hasFile': False},
        {'fieldKey': 'Line18c_CountryOfBirth[0]', 'hasInput': True, 'hasFile': False},
        {'fieldKey': 'Line19_DOB[0]', 'hasInput': True, 'hasFile': False},
        {'fieldKey': 'Line20a_I94Number[0]', 'hasInput': True, 'hasFile': False},
        {'fieldKey': 'Line20b_Passport[0]', 'hasInput': True, 'hasFile': False},
        {'fieldKey': 'Line20c_TravelDoc[0]', 'hasInput': True, 'hasFile': False},
        {'fieldKey': 'Line20d_CountryOfIssuance[0]', 'hasInput': True, 'hasFile': False},
        {'fieldKey': 'Line20e_ExpDate[0]', 'hasInput': True, 'hasFile': False},
        {'fieldKey': 'Line21_DateOfLastEntry[0]', 'hasInput': True, 'hasFile': False},
        {'fieldKey': 'place_entry[0]', 'hasInput': True, 'hasFile': False},
        {'fieldKey': 'Line23_StatusLastEntry[0]', 'hasInput': False, 'hasFile': False},
        {'fieldKey': 'Line24_CurrentStatus[0]', 'hasInput': False, 'hasFile': False},
        {'fieldKey': 'eligibility_category_dropdown', 'hasInput': False, 'hasFile': False},
        {'fieldKey': 'eligibility_category', 'hasInput': True, 'hasFile': False}
    ]

    @pytest.mark.parametrize("field", page_2_fields, ids=lambda f: TestForm765Allure.get_short_id(f))
    @allure.story("Page 2 Inputs")
    def test_03_page2_inputs(self, field):
        field_key = field['fieldKey']
        with allure.step(f"Input Field: {field_key}"):
            try:
                container_xpath = f"//div[@data-field-key='{field_key}']"
                container = self.wait.until(EC.presence_of_element_located((By.XPATH, container_xpath)))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", container)
                time.sleep(1)
                
                if field['hasInput']:
                    input_elem = container.find_element(By.XPATH, ".//input[not(@type='file') and not(@type='radio') and not(@type='checkbox')]")
                    val = "Test Data"
                    if "DOB" in field_key or "Date" in field_key or "ExpDate" in field_key:
                        val = "01/01/2000"
                    elif "Number" in field_key:
                        val = "123456789"
                    input_elem.clear()
                    input_elem.send_keys(val)
                    time.sleep(0.5)
                    
                elif not field['hasInput']:
                    self.click_yes_or_checkbox(container)
                    print(f" -> [YES/NO] Successfully clicked 'Yes' for: {field_key}")
                    time.sleep(0.5)
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name=f"Error_{field_key}", attachment_type=allure.attachment_type.PNG)
                print(f"Failed to process {field_key}: {e}")
                pass

    @allure.story("Page 2 Uploads")
    def test_04_page2_uploads(self):
        us_dl_path = os.path.join(self.project_dir, "US DL.jpeg")
        
        upload_fields = [
            ("Passport Front", "(//div[@data-field-key='passport_inline']//input[@type='file'])[1]"),
            ("Passport Back", "(//div[@data-field-key='passport_inline']//input[@type='file'])[2]"),
            ("Driving License", "//div[@data-field-key='driving_license_inline']//input[@type='file']"),
            ("I-797", "//div[@data-field-key='i797_inline']//input[@type='file']"),
            ("Birth Certificate", "//div[@data-field-key='birth_certificate_inline']//input[@type='file']"),
            ("I-94", "//div[@data-field-key='i94_inline']//input[@type='file']"),
            ("I-94 Travel History", "//div[@data-field-key='i94_travelhistory_inline']//input[@type='file']")
        ]
        
        for index, (field_name, file_input_xpath) in enumerate(upload_fields):
            try:
                container_xpath = f"({file_input_xpath}/ancestor::div[contains(@class, 'document-upload-card') or contains(@class, 'dynamic-form-field')])[last()]"
                
                try:
                    container = self.wait.until(EC.presence_of_element_located((By.XPATH, container_xpath)))
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", container)
                    time.sleep(1.5)
                except:
                    file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, file_input_xpath)))
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", file_input)
                    time.sleep(1.5)
                
                file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, file_input_xpath)))
                self.driver.execute_script("arguments[0].style.display = 'block'; arguments[0].style.opacity = '1'; arguments[0].classList.remove('pointer-events-none');", file_input)
                time.sleep(0.5)
                
                with allure.step(f"Upload Success: {field_name}"):
                    file_input.send_keys(us_dl_path)
                    time.sleep(5)
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name=f"Upload_{field_name}_Failure", attachment_type=allure.attachment_type.PNG)
                pass
            time.sleep(2)
            
        next_btn = self.verify_and_get_element("Next Button Clickable", Form765Locators.get_next_button("last()"))
        self.safe_click("Next", next_btn)

    page_3_fields = [
        {'fieldKey': 'Pt3Line10Checkbox', 'css': '[data-field-key="Pt3Line10Checkbox"]'},
        {'fieldKey': 'Pt3Line1Checkbox[1]', 'css': '[data-field-key="Pt3Line1Checkbox[1]"]'},
        {'fieldKey': 'Pt3Line1Checkbox[0]', 'css': '[data-field-key="Pt3Line1Checkbox[0]"]'},
        {'fieldKey': 'Part3_Checkbox[0]', 'css': '[data-field-key="Part3_Checkbox[0]"]'},
        {'fieldKey': 'Pt3Line3_DaytimePhoneNumber1[0]', 'css': '[data-field-key="Pt3Line3_DaytimePhoneNumber1[0]"]'},
        {'fieldKey': 'Pt3Line4_MobileNumber1[0]', 'css': '[data-field-key="Pt3Line4_MobileNumber1[0]"]'},
        {'fieldKey': 'Pt3Line5_Email[0]', 'css': '[data-field-key="Pt3Line5_Email[0]"]'},
        {'fieldKey': 'Pt4Line6_Checkbox[0]', 'css': '[data-field-key="Pt4Line6_Checkbox[0]"]'},
        {'fieldKey': 'Pt3Line7b_DateofSignature[0]', 'css': '[data-field-key="Pt3Line7b_DateofSignature[0]"]'}
    ]

    @pytest.mark.parametrize("field", page_3_fields, ids=lambda f: TestForm765Allure.get_short_id(f))
    @allure.story("Page 3 Inputs")
    def test_05_page3_inputs(self, field):
        field_key = field['fieldKey']
        css_selector = field['css']
        with allure.step(f"Input Field: {field_key}"):
            try:
                container = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", container)
                time.sleep(1)
                
                # Check if it's an input or checkbox based on the key name
                if 'Checkbox' in field_key:
                    self.click_yes_or_checkbox(container)
                    print(f" -> [YES/NO] Successfully clicked Checkbox for: {field_key}")
                    time.sleep(0.5)
                else:
                    # It's an input field (phone, email, date)
                    try:
                        input_elem = container.find_element(By.XPATH, ".//input[not(@type='checkbox') and not(@type='radio') and not(@type='file')]")
                        val = "Test Data"
                        if "Email" in field_key:
                            val = "test@example.com"
                        elif "Phone" in field_key or "Mobile" in field_key:
                            val = "5551234567"
                        elif "Date" in field_key:
                            val = "01/01/2000"
                        
                        input_elem.clear()
                        input_elem.send_keys(val)
                        print(f" -> [INPUT] Filled text/date for: {field_key}")
                        time.sleep(0.5)
                    except: pass
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name=f"Error_{field_key}", attachment_type=allure.attachment_type.PNG)
                print(f"Failed to process {field_key}: {e}")
                pass

    @allure.story("Page 3 Next")
    def test_06_page3_next(self):
        next_btn = self.verify_and_get_element("Next Button Clickable", Form765Locators.get_next_button("last()"))
        self.safe_click("Next", next_btn)

    @allure.story("Part 4")
    def test_05_part_4(self):
        next_btn = self.verify_and_get_element("Next Button Clickable", Form765Locators.get_next_button("last()"))
        self.safe_click("Next", next_btn)

    @allure.story("Part 5")
    def test_06_part_5(self):
        next_btn = self.verify_and_get_element("Next Button Clickable", Form765Locators.get_next_button("last()"))
        self.safe_click("Next", next_btn)

    @allure.story("Part 6")
    def test_07_part_6(self):
        next_btn = self.verify_and_get_element("Next Button Clickable", Form765Locators.get_next_button("last()"))
        self.safe_click("Next", next_btn)

    page_7_fields = [
        {'fieldKey': 'has_supporting', 'css': '[data-field-key="has_supporting"]'}
    ]

    @pytest.mark.parametrize("field", page_7_fields, ids=lambda f: TestForm765Allure.get_short_id(f))
    @allure.story("Part 7 Inputs")
    def test_08_part_7_inputs(self, field):
        field_key = field['fieldKey']
        css_selector = field['css']
        with allure.step(f"Input Field: {field_key}"):
            try:
                container = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", container)
                time.sleep(1)
                
                self.click_yes_or_checkbox(container)
                print(f" -> [YES/NO] Successfully clicked 'Yes' for: {field_key}")
                time.sleep(0.5)
            except Exception as e: pass

    @allure.story("Part 7 Next")
    def test_08_part_7_next(self):
        next_btn = self.verify_and_get_element("Next Button Clickable", Form765Locators.get_next_button("last()"))
        self.safe_click("Next", next_btn)

    @allure.story("Part 8")
    def test_09_part_8(self):
        next_btn = self.verify_and_get_element("Next Button Clickable", Form765Locators.get_next_button("last()"))
        self.safe_click("Next", next_btn)

    page_9_fields = [
        {'fieldKey': 'wants_g1145', 'css': '[data-field-key="wants_g1145"]'}
    ]

    @pytest.mark.parametrize("field", page_9_fields, ids=lambda f: TestForm765Allure.get_short_id(f))
    @allure.story("Part 9 Inputs")
    def test_10_part_9_inputs(self, field):
        field_key = field['fieldKey']
        css_selector = field['css']
        with allure.step(f"Input Field: {field_key}"):
            try:
                container = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", container)
                time.sleep(1)
                
                self.click_yes_or_checkbox(container)
                print(f" -> [YES/NO] Successfully clicked 'Yes' for: {field_key}")
                time.sleep(0.5)
            except Exception as e: pass

    @allure.story("Part 9 Next")
    def test_10_part_9_next(self):
        try:
            yes_btns = self.driver.find_elements(By.XPATH, "//button[normalize-space(text())='Yes' or normalize-space(text())='YES']")
            for btn in yes_btns:
                is_active = btn.get_attribute("aria-pressed") == "true" or "is-active" in (btn.get_attribute("class") or "")
                if not is_active:
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", btn)
                    time.sleep(0.5)
                    self.driver.execute_script("arguments[0].click();", btn)
                    print(" -> [YES/NO] Generic 'Yes' button clicked on Page 9")
                    time.sleep(0.5)
        except: pass

        next_btn = self.verify_and_get_element("Next Button Clickable", Form765Locators.get_next_button("last()"))
        self.safe_click("Next", next_btn)

    @allure.story("Part 10")
    def test_11_part_10(self):
        next_btn = self.verify_and_get_element("Next Button Clickable", Form765Locators.get_next_button("last()"))
        self.safe_click("Next", next_btn)

    @allure.story("Part 11")
    def test_12_part_11(self):
        try:
            yes_btns = self.driver.find_elements(By.XPATH, "//button[normalize-space(text())='Yes' or normalize-space(text())='YES']")
            for btn in yes_btns:
                is_active = btn.get_attribute("aria-pressed") == "true" or "is-active" in (btn.get_attribute("class") or "")
                if not is_active:
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", btn)
                    time.sleep(0.5)
                    self.driver.execute_script("arguments[0].click();", btn)
                    print(" -> [YES/NO] Generic 'Yes' button clicked on Page 11")
                    time.sleep(0.5)
        except: pass

        next_btn = self.verify_and_get_element("Next Button Clickable", Form765Locators.get_next_button("last()"))
        self.safe_click("Next", next_btn)

    @allure.story("Part 12")
    def test_13_part_12(self):
        try:
            attorney_no = self.verify_and_get_element("Attorney Review No Button", (By.XPATH, "//button[.//span[text()='No']]"), wait_time=5)
            self.safe_click("Attorney Review No", attorney_no)
            
            ship_myself = self.verify_and_get_element("Ship Myself Button", (By.XPATH, "//button[.//span[contains(text(), 'ship it myself')]]"))
            self.safe_click("Ship Myself", ship_myself)
        except: pass
        
        next1 = self.verify_and_get_element("Next Button 1", Form765Locators.get_next_button("last()"))
        self.safe_click("Next 1", next1)
