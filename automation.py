from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

USERNAME = "ignat"
PASSWORD = "Provident2@"


# https://www.youtube.com/watch?v=NB8OceGZGjA

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)


driver.get("https://cursuri.agenti-asigurari.ro/login/index.php")


def login():
    user_element = driver.find_element(By.ID, "username" )
    pass_element = driver.find_element(By.ID, "password" )
    user_element.send_keys(USERNAME)
    pass_element.send_keys(PASSWORD)
    # time.sleep(10)
    login_button = driver.find_element(By.ID, "loginbtn")
    login_button.click()


login()

time.sleep(10)
driver.quit()