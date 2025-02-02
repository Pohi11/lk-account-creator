from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

PATH = "chromedriver.exe"  # or your full path
service = Service(PATH)
chrome_options = Options()

print("Starting test...")
driver = webdriver.Chrome(service=service, options=chrome_options)
print("Driver started")
driver.get("https://www.google.com")
print("Loaded Google")
driver.quit()
print("Test complete")