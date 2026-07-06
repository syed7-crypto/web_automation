import time
import  re
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
time.sleep(10)


print("Filtering results by Posts...")
time.sleep(4)

try:
    posts_filter_button = driver.find_element(By.XPATH, '//button[text()="Posts"]')
    posts_filter_button.click()
    print("Successfully clicked Posts filter.")
except Exception:
    posts_filter_button = driver.find_element(By.XPATH, '//button[contains(., "Posts")]')
    posts_filter_button.click()
    print("Successfully clicked Posts filter (fallback).")

time.sleep(5)


print("Extracting posts and looking for emails...")
time.sleep(5)
post_elements = driver.find_elements(By.CLASS_NAME, "feed-shared-update-v2__description-wrapper")
email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
found_emails = []

for post in post_elements:
    text = post.text
    emails = re.findall(email_pattern, text)
    if emails:
        for email in emails:
            if email not in found_emails:
                found_emails.append(email)

print(f"Extraction complete. Found {len(found_emails)} unique email(s):")
print(found_emails)