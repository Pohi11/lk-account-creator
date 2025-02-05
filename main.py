from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import random
import string
from selenium.webdriver.common.action_chains import ActionChains
import re
import requests
from selenium.webdriver.chrome.options import Options
from multiprocessing import Pool
from licensing.models import *
from licensing.methods import Key, Helpers
import sys
from datetime import date
import os
from colorama import Fore, Back, Style
from selenium.webdriver.chrome.service import Service
from twocaptcha import TwoCaptcha
from webdriver_manager.chrome import ChromeDriverManager

# Global variables and options
global regionsBRUH
regionsBRUH = []
totalcounter = 0
failedaccounts = 0
chrome_options = Options()
os.system(f"title LeagueKingdom Account Creator ({totalcounter} Accounts Created, {failedaccounts} Accounts Failed)")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
PATH = r"chromedriver.exe"
naURL = r"https://signup.na.leagueoflegends.com/en/signup/index#/"
euwURL = r"https://signup.euw.leagueoflegends.com/en/signup/index#/"
euneURL = r"https://signup.eune.leagueoflegends.com/en/signup/index"
lanURL = r"https://signup.lan.leagueoflegends.com/"
lasURL = r"https://signup.las.leagueoflegends.com/"
ruURL = r"https://signup.ru.leagueoflegends.com/"
trURL = r"https://signup.tr.leagueoflegends.com/"
oceURL = r"https://signup.oce.leagueoflegends.com/"
brURL = r"https://signup.br.leagueoflegends.com/"

# Read the 2Captcha API key (still used for hCaptcha solving)
capKEY = open('2captchakey.txt', 'r').readline().strip()

logo = r"""
   _            _  __                _   _     ____   ____      U  ___ u  __  __   
  |"|          |"|/ /       ___     | \ |"| U /"___|u|  _"\      \/"_ \/U|' \/ '|u 
U | | u        | ' /       |_"_|   <|  \| |>\| |  _ /| | | |     | | | |\| |\/| |/ 
 \| |/__     U/| . \\u      | |    U| |\  |u | |_| |U| |_| |\.-,_| |_| | | |  | |  
  |_____|      |_|\_\     U/| |\u   |_| \_|   \____| |____/ u \_)-\___/  |_|  |_|  
  //  \\     ,-,>> \\,-.-,_|___|_,-.||   \\,-._)(|_   |||_         \\   <<,-,,-.
 (_")("_)     \.)   (_/ \_)-' '-(_/ (_")  (_/(__)__) (__)_)       (__)   (./  \.)
"""

def passCreate(stringLength):
    letters = string.ascii_letters
    password = ''.join(random.choice(letters) for i in range(stringLength))
    password += str(random.randint(1, 9))
    return password

def generateName():
    with open("names.txt", "r") as s:
        names = s.readlines()
    cleaned_names = [name.strip() for name in names if name.strip()]
    return random.choice(cleaned_names)

def getName():
    return generateName() + generateName() + str(random.randint(100, 999))

def auth():
    with open("license.txt") as aEnteredKey:
        LicenseKey = aEnteredKey.read().strip()

    RSAPubKey = "<RSAKeyValue><Modulus>oSSuzYFTfCvQMSR7r8Uc+fB7teHfcVMkmMMc0bmzajll4lpFYK3E21NcA2OVsxcZXjgO3wnrsF358QOwdK7R1auAlNGBZjiRU2f+u/zNcItc/CM5p08BWK4ikpXm73cpBYWcLQTFQQtzRf3W6UjWv7q2aXM1Fzphg8gFhWJ0Dz0PBdHncqzNMZ2XHd+7xHsDKovHScF472NXQ+M31QDK7WZnZ1nGdWibOFd91ohtt+sOECDM678XPMNaC5ok6xtR0EIaLyTbBeIL15uQAnUtN2mTRYNRIq5rJdF75kMl9l97QmfKP+6+Ix6Vqmm9IVJnbQ0hFE4+bS2UM4mXOjW0hQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
    authToken = "WyIyOTQyOCIsInN1UzhTSHJ2ZThWRFNNTVJQTGhsYitJdU5GeUhHb2ZURVpneHlPdUgiXQ=="

    result = Key.activate(token=authToken,
                           rsa_pub_key=RSAPubKey,
                           product_id=7195,
                           key=LicenseKey,
                           machine_code=Helpers.GetMachineCode())

    if result[0] is None or not Helpers.IsOnRightMachine(result[0]):
        print("The license does not work: {0}".format(result[1]))
        time.sleep(5)
        sys.exit()
    else:
        Menu()

def runRegion(region, loop):
    print(f"Running region {region} for {loop} iterations")
    region = region.lower()
    for h in range(loop):
        print(f"Starting iteration {h+1} for region {region}")
        if region == 'euw':
            startGEN(euwURL, 'EUW')
        elif region == 'na':
            startGEN(naURL, 'NA')
        elif region == 'eune':
            startGEN(euneURL, 'EUNE')
        elif region == 'lan':
            startGEN(lanURL, 'LAN')
        elif region == 'las':
            startGEN(lasURL, 'LAS')
        elif region == 'br':
            startGEN(brURL, 'BR')
        elif region == 'tr':
            startGEN(trURL, 'TR')
        elif region == 'ru':
            startGEN(ruURL, 'RU')
        elif region == 'oce':
            startGEN(oceURL, 'OCE')

def recovery(region):
    with open(f"{region}_GENNED/{region}_GENNED_RECOVERY.txt", "a") as y:
        getDate = str(date.today())
        ip_address = requests.get('https://api.ipify.org').text
        y.write(accountNAME + ":" + accountPASS + ":" + getDate + ":" + ip_address + ":" + "February 1st 2003" + "\n")

def startGEN(URLURL, region):
    try:
        print(f"Starting account generation for {region}")
        print(f"Using ChromeDriver at path: {PATH}")

        if not os.path.exists(PATH):
            print(f"Error: ChromeDriver not found at {PATH}")
            return

        global totalcounter, failedaccounts, accountNAME, accountPASS

        print("Initializing Chrome driver using webdriver-manager...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("Chrome driver initialized successfully")

        print(f"Navigating to URL: {URLURL}")
        driver.get(URLURL)

        accountNAME = getName()
        accountPASS = passCreate(8)
        print("Account details: " + accountNAME + ":" + accountPASS)

        wait = WebDriverWait(driver, 10)

        print("Waiting for email input field...")
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, """/html/body/div[2]/div/main/div[3]/div/div[2]/div/div[2]/div[1]/div/input""")))
        email_input.clear()
        email_input.send_keys(accountNAME + '@gmail.com')
        email_input.send_keys(Keys.RETURN)
        print("Email entered successfully")
        time.sleep(2)

        dobInput = wait.until(EC.presence_of_element_located((By.XPATH, """/html/body/div[2]/div/main/div[3]/div/div[2]/div/div[2]/div/div[1]/input""")))
        date_string = "09051999"
        dobInput.clear()
        dobInput.send_keys(date_string)
        print("Date entered:", date_string)
        dobInput.send_keys(Keys.RETURN)

        enterUSER = wait.until(EC.presence_of_element_located((By.XPATH, """/html/body/div[2]/div/main/div[3]/div/div[2]/div/div[2]/div/div/input""")))
        enterUSER.send_keys(accountNAME)
        enterUSER.send_keys(Keys.RETURN)

        time.sleep(1)
        enterPASS = wait.until(EC.presence_of_element_located((By.XPATH, """/html/body/div[2]/div/main/div[3]/div/div[2]/div/div[2]/div/div[1]/div/input""")))
        enterPASS.send_keys(accountPASS)
        enterPASS2 = wait.until(EC.presence_of_element_located((By.XPATH, """/html/body/div[2]/div/main/div[3]/div/div[2]/div/div[2]/div/div[4]/div[1]/input""")))
        enterPASS2.send_keys(accountPASS)
        time.sleep(1)
        enterPASS2.send_keys(Keys.RETURN)

        terms_element = wait.until(EC.presence_of_element_located((By.ID, "tos-scrollable-area")))
        terms_element.click()
        terms_element.send_keys(Keys.END)
        time.sleep(1)
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", terms_element)
        accept_thingy = wait.until(EC.presence_of_element_located((By.ID, "tos-checkbox")))
        accept_thingy.click()
        accept_thingy2 = wait.until(EC.presence_of_element_located((By.XPATH, """/html/body/div[2]/div/main/div[3]/div/div[2]/div/div[3]/button/div/span""")))
        accept_thingy2.click()
        time.sleep(1)

        # hCaptcha Solving block
        try:
            print("\n=== Starting hCaptcha Solving ===")
            print("Looking for hCaptcha sitekey in page source...")
            page_source = driver.page_source
            site_key_match = re.search(r'sitekey=([^&"\s]+)', page_source)
            if not site_key_match:
                raise Exception("Could not find hCaptcha sitekey in page source")
            site_key = site_key_match.group(1)
            print("Found sitekey:", site_key)

            solver = TwoCaptcha(capKEY)
            print("Sending hCaptcha to 2captcha...")
            result = solver.hcaptcha(
                sitekey=site_key,
                url=driver.current_url
            )
            code = result["code"]
            print("Got solution:", code[:20] + "...")
            
            # Apply the solution using JavaScript
            driver.execute_script("""
                // Find and set the hCaptcha response textarea
                var textareas = document.getElementsByTagName('textarea');
                for (var i = 0; i < textareas.length; i++) {
                    if (textareas[i].name && textareas[i].name.indexOf('h-captcha-response') !== -1) {
                        textareas[i].innerHTML = arguments[0];
                        // Trigger a change event
                        var event = new Event('change', { bubbles: true });
                        textareas[i].dispatchEvent(event);
                    }
                }
            """, code)
            
            print("Applied solution to hCaptcha")
            time.sleep(2)
            
            # Try to find and click the verify button, even if not visible
            try:
                driver.execute_script("""
                    // Find and click the verify button regardless of visibility
                    var buttons = document.querySelectorAll('div.button-submit.button[title="Verify Answers"]');
                    if (buttons.length > 0) {
                        buttons[0].style.display = 'block';  // Make it visible
                        buttons[0].click();
                    }
                """)
                print("Attempted to click verify button via JavaScript")
                
            except Exception as e:
                print(f"Error with verify button: {str(e)}")
                # Additional fallback method
                try:
                    driver.execute_script("""
                        document.querySelector('iframe[title*="hCaptcha"]').contentWindow.postMessage(
                            {type: 'submit'}, '*'
                        );
                    """)
                    print("Attempted iframe message submission")
                except Exception as e:
                    print(f"Error with iframe submission: {str(e)}")
                
            print("Attempted to verify captcha")
            time.sleep(5)
        except Exception as e:
            print(f"\nError solving hCaptcha: {str(e)}")
            print(f"Current URL: {driver.current_url}")
            failedaccounts += 1
            driver.quit()
            return

        # Check if account creation appears successful.
        soup2 = BeautifulSoup(driver.page_source, 'html.parser')
        win = soup2.find("button", {"class": "download-button"})
        try:
            win = win.text
        except Exception:
            pass

        if win is not None:
            p.write(accountNAME + ":" + accountPASS + "\n")  # Assumes file handle 'p' is defined globally.
            recovery(region)
            totalcounter += 1
            os.system(f"title LeagueKingdom Account Creator ({totalcounter} Account(s) Created, {failedaccounts} Accounts Failed)")
            print(f"Account Created, {totalcounter} account(s) created so far")
        else:
            failedaccounts += 1
            print("Account Creation Failed")

        time.sleep(2)
        driver.quit()
    except Exception as e:
        print(f"Error in startGEN: {str(e)}")
        failedaccounts += 1
        return

def Menu():
    print("Starting Menu function...")
    print(Fore.CYAN)
    print(logo)
    print("-----------------------------------------------------------------------------")
    print("- NA")
    print("- EUW")
    print("- EUNE")
    print("- LAN")
    print("- LAS")
    print("- BR")
    print("- TR")
    print("- RU")
    print("- OCE")
    print("Please select the regions separated by a comma (not case sensitive), e.g.: na, euw, eune")
    chick = input().lower().split(',')
    print(f"Selected regions: {chick}")
    loop = int(input("How many accounts would you like to create (this will apply for all regions): "))
    print(f"Creating {loop} accounts per region")
    while len(chick) != 0:
        regionsBRUH.append(chick[0].replace(" ", ""))
        chick.pop(0)
        print(f"Current regions queue: {regionsBRUH}")
    for j in range(len(regionsBRUH)):
        print(f"Starting account creation for region: {regionsBRUH[0]}")
        runRegion(regionsBRUH[0], loop)
        regionsBRUH.pop(0)

# Entry point
#auth()
Menu()
print(f"All accounts created, {totalcounter} successfully created and {failedaccounts} failed.")
input("Please press enter to close the program")