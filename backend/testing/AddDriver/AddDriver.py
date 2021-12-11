# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class UntitledTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=r"C:\\Users\\kamry\\TeamFAST\\fast-backend\\backend\\chromedriver.exe")
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_untitled_test_case(self):
        driver = self.driver
        driver.get("http://localhost:3000/")
        driver.find_element_by_link_text("Add New").click()
        driver.find_element_by_name("first_name").click()
        driver.find_element_by_name("first_name").clear()
        driver.find_element_by_name("first_name").send_keys("test driver")
        driver.find_element_by_name("last_name").clear()
        driver.find_element_by_name("last_name").send_keys("test last name")
        driver.find_element_by_id("formGridPhone").clear()
        driver.find_element_by_id("formGridPhone").send_keys("402-000-0000")
        driver.find_element_by_id("formGridStatus").click()
        Select(driver.find_element_by_id("formGridStatus")).select_by_visible_text("Employee")
        driver.find_element_by_id("formGridCapacity").click()
        driver.find_element_by_id("formGridCapacity").clear()
        driver.find_element_by_id("formGridCapacity").send_keys("1")
        driver.find_element_by_xpath("//div[@id='root']/div/div/div/form/div[3]/div[2]/label").click()
        driver.find_element_by_id("Sunday").click()
        driver.find_element_by_id("Tuesday").click()
        driver.find_element_by_id("Arabic").click()
        driver.find_element_by_id("Spanish").click()
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_id("search").click()
        driver.find_element_by_id("search").clear()
        driver.find_element_by_id("search").send_keys("tes")
        driver.find_element_by_xpath("//div[@id='root']/div/div").click()
        driver.find_element_by_id("search").click()
        driver.find_element_by_id("search").clear()
        driver.find_element_by_id("search").send_keys("test")
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
