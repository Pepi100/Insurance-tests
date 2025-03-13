from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time



def login(USERNAME, PASSWORD):
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    
    driver.get("https://cursuri.agenti-asigurari.ro/login/index.php")

    user_element = driver.find_element(By.ID, "username" )
    pass_element = driver.find_element(By.ID, "password" )
    user_element.send_keys(USERNAME)
    pass_element.send_keys(PASSWORD)
    # time.sleep(10)
    login_button = driver.find_element(By.ID, "loginbtn")
    login_button.click()

    return driver
    



def format_text(text):
    
    # Înlocuiește newline-urile cu un șir gol
    text =  text.replace('\n', " ").replace('\r', " ").strip()  # .strip() to remove any leading or trailing spaces
    return text



def save_answers(html_content, SAVE_TEST_ANS = True):

    from collections import defaultdict
    questions_answers = defaultdict(list)

    soup = BeautifulSoup(html_content, "html.parser")

    # Găsește toate blocurile de întrebări
    question_blocks = soup.find_all("div", class_="content")

    for question_block in question_blocks:
        if question_block.find("div", class_="formulation clearfix"):
            # Extrage textul întrebării
            question_text = question_block.find("div", class_="formulation clearfix").find("div", class_="qtext").get_text(strip=True)
            question_answer = question_block.find("div", class_="rightanswer").find("p").get_text(strip=True)

            question_text = format_text(question_text)
            question_answer = format_text(question_answer)

            # Adaugă întrebarea și răspunsul în dicționar
            questions_answers[question_text].append(question_answer)

    if SAVE_TEST_ANS:
        import json
        # Salvare în fișier text
        with open("questions_answers.json", "w", encoding="utf-8") as json_file:
            json.dump(questions_answers, json_file, ensure_ascii=False, indent=4)
    
    return questions_answers


def attend_course():
    pass


def ace_test(driver, COURSE_ID):
    
    driver.get(f"https://cursuri.agenti-asigurari.ro/course/view.php?id={COURSE_ID}")

    quizzes = driver.find_elements(By.CSS_SELECTOR, "li.activity.quiz.modtype_quiz")

    # get list of quizzes 
    # print(f"Number of quizzes: {len(quizzes)}")
    next_quiz = None
    for quiz in quizzes:
        try:
            # Check if the <span> with class "badge-success" exists inside the quiz
            badge = quiz.find_element(By.CSS_SELECTOR, "span.badge-success")
        except Exception as e:
            # attempt to take the test
            next_quiz = quiz
            break;

    if next_quiz:
        test = next_quiz.find_element(By.CSS_SELECTOR, "span.instancename")
        test.click()

        test_url = driver.current_url

        try:
            attempts = driver.find_elements(By.CSS_SELECTOR, "table.quizattemptsummary>tbody>tr")
            print(len(attempts))
        except Exception as e:
            attempts = []

        if len(attempts) == 0:
            empty_attempt(driver=driver)
        else:
            # click first attempt
            anaBtn = attempts[0].find_element(By.CSS_SELECTOR, "a" )
            anaBtn.click()

        # currently in bad attempt page

        test_answers = save_answers(driver.page_source)

        driver.get(test_url)
        start_attempt(driver=driver)
        for i in range(40):
            answer_question(driver=driver, questions_answers=test_answers)


        

    else:
        print("No tests")



def answer_question(driver, questions_answers):
        
        time.sleep(1)
        # get question text
        question = driver.find_element(By.CSS_SELECTOR, "div.qtext>p")
        question = question.text
        print(question)

        # find text in dictionary and get answer
        answer = questions_answers[question]
        print(answer)
        # click answer
        ans = driver.find_elements(By.CSS_SELECTOR, "div.answer>div")

        if answer[0] in ans[0].get_attribute("outerHTML"):
            ansInput = ans[0].find_element(By.CSS_SELECTOR, "input")
        elif answer[0] in ans[1].get_attribute("outerHTML"):
            ansInput = ans[1].find_element(By.CSS_SELECTOR, "input")
        else:
            ansInput = ans[2].find_element(By.CSS_SELECTOR, "input")

        ansInput.click()

        # click next
        nextBtn = driver.find_element(By.CSS_SELECTOR, "div.submitbtns input.mod_quiz-next-nav.btn-primary")
        nextBtn.click()



def start_attempt(driver):
    button = driver.find_element(By.CSS_SELECTOR, "div.singlebutton button")
    button.click()

    button2 = driver.find_element(By.CSS_SELECTOR, "div.moodle-dialogue-bd input.btn-primary")
    button2.click()

def empty_attempt(driver):
    start_attempt(driver=driver)

    # finish test 

    finBtn = driver.find_element(By.CSS_SELECTOR, "div.othernav a.endtestlink")
    finBtn.click()