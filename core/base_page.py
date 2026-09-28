import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from core.common_locators import CommonLocators

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)
        self.fast_wait = WebDriverWait(self.driver, 5)

    def click_element(self, locator, use_js=False):
        elem = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
        time.sleep(0.3)
        if use_js:
            self.driver.execute_script("arguments[0].click();", elem)
        else:
            try:
                elem.click()
            except:
                self.driver.execute_script("arguments[0].click();", elem)
        time.sleep(0.5)
        return elem

    def enter_text(self, locator, text, use_js_click=False):
        elem = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
        time.sleep(0.3)
        if use_js_click:
            self.driver.execute_script("arguments[0].click();", elem)
        else:
            try:
                elem.click()
            except:
                self.driver.execute_script("arguments[0].click();", elem)
        time.sleep(0.3)
        elem.send_keys(text)
        time.sleep(0.5)

    def select_dropdown(self, locator, value):
        elem = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
        time.sleep(0.5)
        elem.click()
        time.sleep(0.5)
        elem.send_keys(value)
        time.sleep(1)
        elem.send_keys(Keys.ENTER)
        time.sleep(1)

    def click_next(self, index="last()"):
        self.click_element(CommonLocators.get_next_button(index))
        time.sleep(2)
