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
email=input("Enter email: ")
emailfield.send_keys(email)
time.sleep(5)

passwordfield = driver.find_element(By.ID, "password")
password=input("Enter password: ")
passwordfield.send_keys(password)
time.sleep(5)

login = driver.find_element(By.XPATH, '//button[@type="button"]')
login.click()
time.sleep(10)

searchbar = driver.find_element(By.CLASS_NAME, "search-global-typeahead__input")
search = input("What to search for: ")
searchbar.send_keys(search)
time.sleep(1)
print("Press enter...")
searchbar.send_keys(Keys.ENTER)