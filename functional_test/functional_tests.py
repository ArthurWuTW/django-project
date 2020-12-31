from selenium import webdriver
import unittest
import time

class NewVisitorTest(unittest.TestCase):
  def setUp(self): # before running test
    self.browser = webdriver.Firefox()
    # WARNING don't rely on implicitly_wait! it won't work for every use case
    # self.browser.implicitly_wait(10)
  def tearDown(self): # after running test
    self.browser.quit()
  def test_can_start_a_list_and_retrieve_it_later(self): # any test starts with 'test_'
    self.browser.get('https://plantmonitor.mooo.com')
    time.sleep(3)
    self.assertIn("SB Admin 2 - Dashboard", self.browser.title)

# __name__ is __main__ : that's how a Python script checks if it's been executed from the command
# line, rather than just imported by another script
if __name__ == '__main__':
  unittest.main(warnings='ignore')
