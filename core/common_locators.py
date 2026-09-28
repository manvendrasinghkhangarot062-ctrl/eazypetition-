from selenium.webdriver.common.by import By

class CommonLocators:
    @staticmethod
    def get_yes_button(index):
        return (By.XPATH, f"(//button[text()='Yes'])[{index}]")

    @staticmethod
    def get_no_button(index):
        return (By.XPATH, f"(//button[text()='No'])[{index}]")

    @staticmethod
    def get_datepicker_input(is_last=False):
        if is_last:
            return (By.XPATH, "(//input[@data-test-id='dp-input'])[last()]")
        return (By.CSS_SELECTOR, "input[data-test-id='dp-input']")

    TODAY_DATE = (By.XPATH, "//div[contains(@class, 'dp__today')]")

    @staticmethod
    def get_email_input(is_last=False):
        if is_last:
            return (By.XPATH, "(//input[@type='email'])[last()]")
        return (By.XPATH, "//input[@type='email']")

    @staticmethod
    def get_next_button(index):
        return (By.XPATH, f"(//button[.//span[text()='Next']])[{index}]")

    @staticmethod
    def get_input_by_label(label_text):
        return (By.XPATH, f"//label[normalize-space(text())='{label_text}']/following-sibling::div//input")

    @staticmethod
    def get_input_by_address_label(label_text):
        return (By.XPATH, f"(//label[contains(@class, 'address-field__label') and starts-with(normalize-space(.), '{label_text}')]/following::input)[1]")

    @staticmethod
    def get_input_after_country(index, is_last=False):
        prefix = "(//input[@placeholder='Select country'])[last()]" if is_last else "//input[@placeholder='Select country']"
        return (By.XPATH, f"({prefix}/following::input[contains(@class, 'input__field')])[{index}]")

    CONTINUE_BTN = (By.XPATH, "//button[.//span[text()='Continue']]")
    PRECONDITION_CHECKBOX = (By.CSS_SELECTOR, "input.precondition-checkbox")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.formselection__search-input")
    SELECT_FORM_BTN = (By.XPATH, "//button[contains(., 'Select this form')]")
    NEW_PETITION_BTN = (By.XPATH, "//button[.//span[contains(., 'New Petition')]]")
    GENERIC_INPUTS = (By.CSS_SELECTOR, "input.input__field")

    UPLOAD_ICON = (By.XPATH, "//img[@alt='Upload']")
    UPLOAD_FROM_DEVICE_BTN = (By.XPATH, "//button[.//div[text()='Upload from Your Device']]")
    HIDDEN_FILE_INPUT = (By.CSS_SELECTOR, "input[type='file']")

    ATTORNEY_REVIEW_NO_BTN = (By.XPATH, "//button[.//span[text()='No']]")
    SHIP_MYSELF_BTN = (By.XPATH, "//button[.//span[text()=\"No, I'll ship it myself\"]]")
    STATE_DROPDOWN_INPUT = (By.CSS_SELECTOR, "input[placeholder='Select state']")
