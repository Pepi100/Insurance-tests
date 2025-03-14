from selenium.webdriver.common.by import By
import time
from utils import login, ace_test

USERNAME = "enculescu"
PASSWORD = "Provident2@"
COURSE_ID = 57
SAVE_TEST_ANS  = True
# max time per question in seconds
Q_TIME = 10


# https://www.youtube.com/watch?v=NB8OceGZGjA




driver = login(USERNAME, PASSWORD)

try:
    ace_test(driver, COURSE_ID=COURSE_ID, Q_TIME=Q_TIME)
    ace_test(driver, COURSE_ID=COURSE_ID, Q_TIME=Q_TIME)
    ace_test(driver, COURSE_ID=COURSE_ID, Q_TIME=Q_TIME)
    ace_test(driver, COURSE_ID=COURSE_ID, Q_TIME=Q_TIME)
    ace_test(driver, COURSE_ID=COURSE_ID, Q_TIME=Q_TIME)
except Exception as e:
    print(e)
    print("No more tests")



time.sleep(150)
