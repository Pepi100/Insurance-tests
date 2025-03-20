from utils import login, save_test_answers
from selenium.webdriver.common.by import By
import time


USERNAME = ""
PASSWORD = ""
COURSE_ID = 57
SAVE_TEST_ANS  = True
# max time per question in seconds
Q_TIME = 2










def save_answers():
    driver = login(USERNAME, PASSWORD)
    driver.get(f"https://cursuri.agenti-asigurari.ro/course/view.php?id={COURSE_ID}")
    quizzes = driver.find_elements(By.CSS_SELECTOR, "li.activity.quiz.modtype_quiz")

    # check if all have been completed

    from collections import defaultdict
    questions_answers = defaultdict(list)

    tests = len(quizzes)
    for i in range(tests):
        driver.get(f"https://cursuri.agenti-asigurari.ro/course/view.php?id={COURSE_ID}")
        quizzes = driver.find_elements(By.CSS_SELECTOR, "li.activity.quiz.modtype_quiz")
        quiz = quizzes[i]
        test = quiz.find_element(By.CSS_SELECTOR, "span.instancename")
        test.click()
        time.sleep(Q_TIME)
        attempts = driver.find_elements(By.CSS_SELECTOR, "table.quizattemptsummary>tbody>tr")
        anaBtn = attempts[0].find_element(By.CSS_SELECTOR, "a")
        anaBtn.click()
        time.sleep(Q_TIME)

        ans = save_test_answers(driver.page_source)

        for key, value in ans.items():
            questions_answers[key].extend(value)

    import json
    # Salvare în fișier text
    with open("questions_answers.json", "w", encoding="utf-8") as json_file:
        json.dump(questions_answers, json_file, ensure_ascii=False, indent=4)



save_answers()




