import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from selenium.webdriver.common.by import By
from core.common_locators import CommonLocators

class Form765Locators(CommonLocators):

    NEW_PETITION_BTN = (By.XPATH, "//button[.//span[contains(., 'New Petition')]]")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.formselection__search-input")
    SELECT_FORM_BTN = (By.XPATH, "//button[contains(., 'Select this form')]")
    PRECONDITION_CHECKBOX = (By.CSS_SELECTOR, "input.precondition-checkbox")
    CONTINUE_BTN = (By.XPATH, "//button[.//span[text()='Continue']]")
    APPLICATION_REASON_INPUT = (By.ID, "application_reason")
    REASON_OPTION_1A = (By.XPATH, "//div[contains(text(), '1.a. Initial permission')]")
    @staticmethod
    def get_next_button(index):
        return (By.XPATH, f"(//button[.//span[text()='Next']])[{index}]")
    GENERIC_INPUTS = (By.CSS_SELECTOR, "input.input__field")
    
    # input boxes ko verify karne ke locators
    GIVEN_NAME_INPUT = (By.ID, "Line1b_GivenName[0]")
    FAMILY_NAME_INPUT = (By.ID, "Line1a_FamilyName[0]")
    MIDDLE_NAME_INPUT = (By.ID, "Line1c_MiddleName[0]")
    
    FAMILY_NAME_2A = (By.ID, "Line2a_FamilyName[0]")
    GIVEN_NAME_2B = (By.ID, "Line2b_GivenName[0]")
    MIDDLE_NAME_2C = (By.ID, "Line2c_MiddleName[0]")
    
    FAMILY_NAME_3A = (By.ID, "Line3a_FamilyName[1]")
    GIVEN_NAME_3B = (By.ID, "Line3b_GivenName[1]")
    MIDDLE_NAME_3C = (By.ID, "Line3c_MiddleName[1]")
    
    FAMILY_NAME_4A = (By.ID, "Line3a_FamilyName[0]")
    GIVEN_NAME_4B = (By.ID, "Line3b_GivenName[0]")
    MIDDLE_NAME_4C = (By.ID, "Line3c_MiddleName[0]")
    
    
    
    
    STATE_DROPDOWN_INPUT = (By.CSS_SELECTOR, "input[placeholder='Select state']")
    FLR_BUTTON = (By.XPATH, "//button[contains(@class, 'address-field__unit-btn') and text()='Flr']")
    FLR_NEXT_INPUT = (By.XPATH, "(//button[contains(@class, 'address-field__unit-btn') and text()='Flr']/following::input)[1]")
    ZIP_CODE_NEXT_INPUT = (By.XPATH, "(//button[contains(@class, 'address-field__unit-btn') and text()='Flr']/following::input)[2]")
    
    
    REGISTRATION_NUMBER_INPUT = (By.XPATH, "(//label[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'registration')]/following::input)[1]")
    
    MARITAL_STATUS_DROPDOWN = (By.ID, "marital_status")
    
    UPLOAD_ICON = (By.XPATH, "//img[@alt='Upload']")
    UPLOAD_FROM_DEVICE_BTN = (By.XPATH, "//button[.//div[text()='Upload from Your Device']]")
    HIDDEN_FILE_INPUT = (By.CSS_SELECTOR, "input[type='file']")
    
    # Part 3 Locators
    PT3_LANGUAGE_INPUT = (By.XPATH, "//input[@id='Pt3Line1b_Language[0]']")
    PT3_REPRESENTATIVE_NAME_INPUT = (By.XPATH, "//input[@id='Pt3Line2_RepresentativeName[0]']")
    PT3_DAYTIME_PHONE_INPUT = (By.XPATH, "//input[@id='Pt3Line3_DaytimePhoneNumber1[0]']")
    PT3_MOBILE_NUMBER_INPUT = (By.XPATH, "//input[@id='Pt3Line4_MobileNumber1[0]']")
    
    # Part 4 Locators
    PT4_INTERPRETER_FAMILY_NAME_INPUT = (By.XPATH, "//input[@id='Pt4Line1a_InterpreterFamilyName[0]']")
    PT4_INTERPRETER_GIVEN_NAME_INPUT = (By.XPATH, "//input[@id='Pt4Line1b_InterpreterGivenName[0]']")
    PT4_INTERPRETER_ORG_INPUT = (By.XPATH, "//input[@id='Pt4Line2_InterpreterBusinessorOrg[0]']")
    PT4_COUNTRY_DROPDOWN = (By.XPATH, "//input[@placeholder='Select country']")
    PT4_DAYTIME_TELEPHONE_INPUT = (By.XPATH, "//input[@id='Pt4Line4_InterpreterDaytimeTelephone[0]']")
    PT4_MOBILE_NUMBER_INPUT = (By.XPATH, "//input[@id='Pt4Line5_MobileNumber[0]']")
    PT4_LANGUAGE_INPUT = (By.XPATH, "//input[@id='Part4_NameofLanguage[0]']")
    
    # Part 5 Locators
    PT5_PREPARER_FAMILY_NAME_INPUT = (By.XPATH, "//input[@id='Pt5Line1a_PreparerFamilyName[0]']")
    PT5_PREPARER_GIVEN_NAME_INPUT = (By.XPATH, "//input[@id='Pt5Line1b_PreparerGivenName[0]']")
    PT5_BUSINESS_NAME_INPUT = (By.XPATH, "//input[@id='Pt5Line2_BusinessName[0]']")
    PT5_COUNTRY_DROPDOWN = (By.XPATH, "(//input[@placeholder='Select country'])[last()]")
    PT5_DAYTIME_TELEPHONE_INPUT = (By.XPATH, "//input[@id='Pt5Line4_DaytimePhoneNumber1[0]']")
    PT5_MOBILE_NUMBER_INPUT = (By.XPATH, "//input[@id='Pt5Line5_PreparerFaxNumber[0]']")
    
    # Part 7 Locators
    PT7_EDUCATION_LEVEL_DROPDOWN = (By.ID, "education_level")

    # Final Steps Locators
    ATTORNEY_REVIEW_NO_BTN = (By.XPATH, "//button[.//span[text()='No']]")
    SHIP_MYSELF_BTN = (By.XPATH, "//button[.//span[text()=\"No, I'll ship it myself\"]]")
