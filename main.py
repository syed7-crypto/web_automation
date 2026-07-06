import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

name = input("Enter your name: ")
user_email = input("Enter email: (This will also be the sender email!) ") 
linkedin_password = input("Enter password: (This is Linkedin password!) ")
app_password = input("Enter Password: (This will be Gmail app password for sending mail!) ")

driver.get("https://www.linkedin.com/login")
time.sleep(3)

emailfield = driver.find_element(By.ID, "username")
emailfield.send_keys(user_email)

passwordfield = driver.find_element(By.ID, "password")
passwordfield.send_keys(linkedin_password)

login = driver.find_element(By.XPATH, '//button[@type="submit"]') 
login.click()
time.sleep(8)

searchbar = driver.find_element(By.CLASS_NAME, "search-global-typeahead__input")
search = input("What to search for: ")
searchbar.send_keys(search)
time.sleep(1)
searchbar.send_keys(Keys.ENTER)
time.sleep(5)

try:
    posts_filter_button = driver.find_element(By.XPATH, '//button[text()="Posts"]')
    posts_filter_button.click()
except Exception:
    try:
        posts_filter_button = driver.find_element(By.XPATH, '//button[contains(., "Posts")]')
        posts_filter_button.click()
    except Exception:
        pass

time.sleep(5)

for _ in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

post_elements = driver.find_elements(By.CLASS_NAME, "feed-shared-update-v2__description-wrapper")
email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
found_emails = []

for post in post_elements:
    text = post.text
    emails = re.findall(email_pattern, text)
    if emails:
        for extracted_email in emails:  
            if extracted_email not in found_emails:
                found_emails.append(extracted_email)

if found_emails:
    sender_email = user_email
    resume_path = "Resume.pdf" 

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls() 
        server.login(sender_email, app_password)
        
        for recipient in found_emails:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient
            msg['Subject'] = "Application for Java Developer (Contract) Role"

            body = f"Hello,\n\nI saw your recent LinkedIn post regarding the contract Java Developer opportunity and would love to apply. Please find my resume attached.\n\nBest regards,\n{name}"
            msg.attach(MIMEText(body, 'plain'))
            
            try:
                with open(resume_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={resume_path}")
                msg.attach(part)
                
                server.send_message(msg)
            except FileNotFoundError:
                break  
        server.quit()
        
    except Exception:
        pass

driver.quit()