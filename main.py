import requests
from bs4 import BeautifulSoup
import unicodedata

# Datele pentru login
LOGIN_URL = "https://cursuri.agenti-asigurari.ro/login/index.php"
USERNAME = "ignat"
PASSWORD = "Provident2@"
COURSE_URL = "https://cursuri.agenti-asigurari.ro/course/view.php?id=57"

def login(LOGIN_URL = LOGIN_URL, USERNAME = USERNAME, PASSWORD = PASSWORD, COURSE_URL = COURSE_URL):
    # Inițializează o sesiune pentru a păstra cookie-urile
    session = requests.Session()

    # Obține pagina de login
    login_page = session.get(LOGIN_URL)
    soup = BeautifulSoup(login_page.text, "html.parser")

    # Extrage token-ul CSRF
    csrf_token = soup.find("input", {"name": "logintoken"})
    csrf_token = csrf_token["value"] if csrf_token else None

    print("CSRF Token:", csrf_token)

    # Trimite cererea de login cu token-ul
    payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "logintoken": csrf_token  # Adaugă token-ul
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    response = session.post(LOGIN_URL, data=payload, headers=headers)
    # Verifică dacă login-ul a avut succes
    if "dashboard" in response.text.lower():  # Verifică dacă apare un indiciu de succes în pagină
        print("Autentificare reușită!")
    else:
        print("Autentificare eșuată! Verifică username-ul și parola.")
    return session


def save_as_html(text):
    with open("test" +".html", "w", encoding="utf-8") as file:
            file.write(text)

def get_answers():
    # go to course page
    course_page = session.get(COURSE_URL)
    soup = BeautifulSoup(course_page.text, "html.parser")   


    # scrape current test url:
    current_quiz = ""
    for a_tag in soup.find_all("a", href=True):
        if "/mod/quiz/view.php?id=" in a_tag["href"]:  # Filtrăm doar link-urile de teste
            current_quiz = a_tag["href"]
    
    # go to quiz page
    quiz_page = session.get(current_quiz)
    soup = BeautifulSoup(quiz_page.text, "html.parser")

    # start quiz

    quiz_form = soup.find("form", {"action": "https://cursuri.agenti-asigurari.ro/mod/quiz/startattempt.php"})

    cmid = quiz_form.find("input", {"name": "cmid"})["value"]
    sesskey = quiz_form.find("input", {"name": "sesskey"})["value"]

    # 3️ Trimite cererea POST pentru a începe testul
    quiz_start_url = "https://cursuri.agenti-asigurari.ro/mod/quiz/startattempt.php"
    payload = {
        "cmid": cmid,
        "sesskey": sesskey
    }
    
    response = session.post(quiz_start_url, data=payload)

    # Dacă este necesar un al doilea submit, găsește formularul de confirmare
    forms = BeautifulSoup(response.text, "html.parser").find_all("form")
    confirmation_form = forms[0]
    # # 
    # print(confirmation_form)
    
    # Extrage valorile necesare pentru cererea POST de confirmare
    confirm_payload = {}
    for input_tag in confirmation_form.find_all("input"):
        confirm_payload[input_tag["name"]] = input_tag.get("value", "")

    # Trimite cererea POST pentru formularul de confirmare
    confirm_response = session.post(confirmation_form["action"], data=confirm_payload, headers=headers)

    # Verifică răspunsul la cererea de confirmare
    if "attempt" in confirm_response.url or "quiz-attempt" in confirm_response.text:
        print("Testul a fost confirmat și a început cu succes!")
    else:
        print("Eroare la confirmarea testului")
        # save_as_html(confirm_response.text)

def format_text(text, diacritics = True):
    # Normalizează textul și elimină diacriticele
    text = unicodedata.normalize('NFD', text)
    
    if diacritics:
        # Elimină diacriticele
        text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    
    # Înlocuiește newline-urile cu un șir gol
    text =  text.replace('\n', "").replace('\r', " ").strip()  # .strip() to remove any leading or trailing spaces
    
    
    return text
    


session = login()




attempt_urls = [
    "https://cursuri.agenti-asigurari.ro/mod/quiz/review.php?attempt=159804&cmid=2994",
    "https://cursuri.agenti-asigurari.ro/mod/quiz/review.php?attempt=159834&cmid=2995",
    "https://cursuri.agenti-asigurari.ro/mod/quiz/review.php?attempt=159834&cmid=2996",
    
    
]

from collections import defaultdict

# Crează un dicționar pentru întrebări și răspunsuri, folosind o listă
questions_answers = defaultdict(list)

for url in attempt_urls:
    response = session.get(url)



    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    # Găsește toate blocurile de întrebări
    question_blocks = soup.find_all("div", class_="content")

    for question_block in question_blocks:
        if question_block.find("div", class_="formulation clearfix"):
            # Extrage textul întrebării
            question_text = question_block.find("div", class_="formulation clearfix").find("div", class_="qtext").get_text(strip=True)
            question_answer = question_block.find("div", class_="rightanswer").get_text(strip=True)

            question_text = format_text(question_text)
            question_answer = format_text(question_answer)

            # Adaugă întrebarea și răspunsul în dicționar
            questions_answers[question_text].append(question_answer)

    # Salvare în fișier text
    with open("questions_answers.txt", "w", encoding="utf-8") as text_file:
        for question, answer in questions_answers.items():
            text_file.write(f"Întrebare: {question}\n")
            text_file.write(f"{answer}\n\n")

    print("Dicționarul a fost salvat în fișier text.")
