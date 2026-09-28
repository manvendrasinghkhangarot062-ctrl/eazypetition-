import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from core.base_page import BasePage

class BaseTest:
    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("https://121.eazypetition.org/?step=part2")
        self.page = BasePage(self.driver)
        yield
        self.driver.quit()
