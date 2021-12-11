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
        self.driver = webdriver.Chrome(executable_path=r'../chromedriver.exe')
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_untitled_test_case(self):
        driver = self.driver
        driver.get("http://3.144.105.249:3000/")
        driver.find_element_by_link_text("Edit").click()
        driver.find_element_by_name("first_name").click()
        driver.find_element_by_name("first_name").clear()
        driver.find_element_by_name("first_name").send_keys("Huck")
        driver.find_element_by_name("last_name").click()
        driver.find_element_by_name("last_name").clear()
        driver.find_element_by_name("last_name").send_keys("Fi")
        driver.find_element_by_id("formGridPhone").click()
        driver.find_element_by_id("formGridPhone").clear()
        driver.find_element_by_id("formGridPhone").send_keys("402-280-9613")
        driver.find_element_by_id("formGridStatus").click()
        Select(driver.find_element_by_id("formGridStatus")).select_by_visible_text("Volunteer")
        driver.find_element_by_id("formGridCapacity").click()
        driver.find_element_by_id("formGridCapacity").clear()
        driver.find_element_by_id("formGridCapacity").send_keys("29")
        driver.find_element_by_xpath("//div[@id='root']/div/div/div/form/div[3]/div[7]/label").click()
        driver.find_element_by_id("Arabic").click()
        driver.find_element_by_xpath("//div[@id='root']/div/div/div/form/button").click()
        driver.find_element_by_xpath("//div[@id='root']/div/div/div/form/a/button").click()
        driver.find_element_by_id("search").click()
        driver.find_element_by_id("search").clear()
        driver.find_element_by_id("search").send_keys("huc")
        # self.assertEqual("Huck", driver.find_element_by_xpath("//div[@id='root']/div/div/div/div[2]/table/tbody/tr/td").text)
        # self.assertEqual("Fi", driver.find_element_by_xpath("//div[@id='root']/div/div/div/div[2]/table/tbody/tr/td[2]").text)
        # self.assertEqual("402-280-9613", driver.find_element_by_xpath("//div[@id='root']/div/div/div/div[2]/table/tbody/tr/td[3]").text)
        driver.find_element_by_link_text("View").click()
        # self.assertEqual("Arabic", driver.find_element_by_xpath("//div[@id='root']/div/div/div/div[4]/table/tbody/tr/td[3]").text)
        # self.assertEqual("Available", driver.find_element_by_xpath("//div[@id='root']/div/div/div/div[3]/table/tbody/tr/td[6]").text)
        # self.assertEqual("29", driver.find_element_by_xpath("//div[@id='root']/div/div/div/div[2]/table/tbody/tr/td[5]").text)
        # self.assertEqual("Volunteer", driver.find_element_by_xpath("//div[@id='root']/div/div/div/div[2]/table/tbody/tr/td[6]").text)
    
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
