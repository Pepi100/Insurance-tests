from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import time




from utils import login, ace_test

USERNAME = ""
PASSWORD = ""
COURSE_ID = 57
SAVE_TEST_ANS  = True


# https://www.youtube.com/watch?v=NB8OceGZGjA




driver = login(USERNAME, PASSWORD)
ace_test(driver, COURSE_ID=COURSE_ID)









            
            
        
            

       




def take_test():
    test_url = driver.current_url

    try:
        attempts = driver.find_elements(By.CSS_SELECTOR, "table.quizattemptsummary>tbody>tr.bestrow")
        print(len(attempts))
    except Exception as e:
        attempts = 0

    
    
    

    # go back to test page
    driver.get(test_url)

    # start test
    button = driver.find_element(By.CSS_SELECTOR, "div.singlebutton button")
    button.click()

    button2 = driver.find_element(By.CSS_SELECTOR, "div.moodle-dialogue-bd input.btn-primary")
    button2.click()


    


    
    




time.sleep(150)
