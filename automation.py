from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import time




from utils import login, ace_test

USERNAME = "ignat"
PASSWORD = "Provident2@"
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


    def answer_question():
        # get question text
        question = driver.find_element(By.CSS_SELECTOR, "div.qtext p.ltr")
        question = question.text
        print(question)

        # find text in dictionary and get answer
        answer = questions_answers[question]
        print(answer)
        # click answer
        ans = driver.find_elements(By.CSS_SELECTOR, "div.answer>div")

        if answer in ans[0].get_attribute("outerHTML"):
            ansInput = ans[0].find_element(By.CSS_SELECTOR, "input")
        elif answer in ans[1].get_attribute("outerHTML"):
            ansInput = ans[1].find_element(By.CSS_SELECTOR, "input")
        else:
            ansInput = ans[2].find_element(By.CSS_SELECTOR, "input")

        ansInput.click()

        # click next
        nextBtn = driver.find_element(By.CSS_SELECTOR, "div.submitbtns input.mod_quiz-next-nav.btn-primary")
        nextBtn.click()


    for i in range(40):
        answer_question()

    




time.sleep(150)
