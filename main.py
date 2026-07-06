import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

print("Navigating to LinkedIn...")
driver.get("https://www.linkedin.com/login")
time.sleep(5)

emailfield = driver.find_element(By.ID, "username")
emailfield.send_keys("........@gmail.com")
time.sleep(5)

passwordfield = driver.find_element(By.ID, "password")
passwordfield.send_keys("password")
time.sleep(5)

login = driver.find_element(By.ID, "button")
login.click()
time.sleep(10)