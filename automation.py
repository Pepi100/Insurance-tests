
import time
from utils import login, ace_test, course_completion

USERNAME = ""
PASSWORD = ""
COURSE_ID = 57
SAVE_TEST_ANS  = True
# max time per question in seconds
Q_TIME = 10


# https://www.youtube.com/watch?v=NB8OceGZGjA




driver = login(USERNAME, PASSWORD)
course_completion(driver, COURSE_ID)





time.sleep(150)
