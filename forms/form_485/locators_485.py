import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from selenium.webdriver.common.by import By
from core.common_locators import CommonLocators

class Form485Locators(CommonLocators):
    NEW_PETITION_BTN = (By.XPATH, "//button[.//span[contains(., 'New Petition')]]")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.formselection__search-input")
    SELECT_FORM_BTN = (By.XPATH, "(//button[contains(., 'Select this form')])[1]")
    PRECONDITION_CHECKBOX = (By.CSS_SELECTOR, "input.precondition-checkbox")
    CONTINUE_BTN = (By.XPATH, "//button[.//span[text()='Continue']]")
    APPLICATION_REASON_INPUT = (By.ID, "application_reason")
    REASON_OPTION_1A = (By.XPATH, "//div[contains(text(), '1.a.')]")
    @staticmethod
    def get_next_button(index):
        return (By.XPATH, f"(//button[.//span[text()='Next']])[{index}]")

