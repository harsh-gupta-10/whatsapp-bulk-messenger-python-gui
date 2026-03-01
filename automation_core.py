"""
Core automation module for WhatsApp Bulk Messenger
Contains all the core functionality extracted from automator.py
"""

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from urllib.parse import quote
import os

DELAY = 30


def get_user_data_dir():
    """Returns the default user data directory path based on the operating system."""
    if os.name == 'nt':  # Windows
        return os.path.join(os.environ['LOCALAPPDATA'], 'HarshGupta', 'WABulker', 'User Data')
    elif os.name == 'posix': 
        if os.uname()[0] == 'Darwin': 
            return os.path.join(os.environ['HOME'], 'Library', 'HarshGupta', 'WABulker', 'User Data')
        else: 
            return os.path.join(os.environ['HOME'], '.config', 'harshgupta', 'wabulker', 'user_data')
    else:
        raise Exception("Unsupported operating system")


def send_messages(driver, numbers, message):
    """Send messages to a list of phone numbers"""
    for idx, number in enumerate(numbers):
        number = number.strip()
        if number == "":
            continue
        print('\n{}/{} => Sending message to {}.'.format((idx+1), len(numbers), number))
        try:
            url = f"https://web.whatsapp.com/send?phone={number}&text={message}"
            sent = False
            for i in range(3):
                if not sent:
                    driver.get(url)
                    try:
                        click_btn = WebDriverWait(driver, DELAY).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Send']")))
                    except Exception as e:
                        print(f"\nFailed to send message to: {number}, retry ({i+1}/3)")
                        print("Make sure your phone and computer is connected to the internet.")
                        print("If there is an alert, please dismiss it.")
                    else:
                        sleep(1)
                        click_btn.click()
                        sent=True
                        sleep(3)
                        print(f'Message sent to: {number}')
        except Exception as e:
            print(f'Failed to send message to {number}: {e}')


def get_message() -> str:
    """Read message from message.txt and URL encode it"""
    f = open("message.txt", "r", encoding="utf8")
    message = f.read()
    f.close()
    print('\nThis is your message-')
    print(message)
    message = quote(message)
    return message


def get_numbers() -> list:
    """Read phone numbers from numbers.txt"""
    numbers = []
    f = open("numbers.txt", "r")
    for line in f.read().splitlines():
        if line.strip() != "":
            numbers.append(line.strip())
    f.close()
    return numbers


def get_driver():
    """Initialize and return a Chrome WebDriver instance.
    ChromeDriverManager auto-downloads the correct ChromeDriver on first run."""
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--profile-directory=Default")
    options.add_argument("--user-data-dir=" + get_user_data_dir())
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver


def login_whatsapp(driver):
    """Open WhatsApp Web and wait for user to login"""
    print('Once your browser opens up sign in to web whatsapp')
    driver.get('https://web.whatsapp.com')
    input("AFTER logging into Whatsapp Web is complete and your chats are visible, press ENTER...")


def print_intro():
    """Print introduction message"""
    print("\n**********************************************************")
    print("*****                                               ******")
    print("*****  THANK YOU FOR USING WHATSAPP BULK MESSENGER  ******")
    print("*****        This tool was built by Harsh Gupta      ******")
    print("*****             www.github.com/harshgupta          ******")
    print("*****                                               ******")
    print("**********************************************************")
