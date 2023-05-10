from bs4 import BeautifulSoup
import requests

course_codes = [
    "EDAN20", "EDAP20", "FMSF10",
    "FRTN65", "FRTN85", "FRTN50"
]

FILE_NAME = "machine_intelligence_courses.txt"

full_text = ""
for code in course_codes:
    r = requests.get(f'https://kurser.lth.se/kursplaner/23_24%20eng/{code}.html')
    soup = BeautifulSoup(r.text, 'html.parser')
    raw_text = soup.get_text()
    course_name = soup.h1.text.splitlines()[1]

    text = f"{course_name}\nAim:\n"
    append = False
    for line in raw_text.splitlines():
        if not append:
            if line.lower() == "aim":
                append = True
        else:
            l = line.lower()
            if l == "examination details":
                break
            if l == "learning outcomes" or l == "contents":
                text = text + "\n" + line + ":\n"
            else:
                text = text + line + " "
    text = text + "\n\n"
    full_text = full_text + text

with open("FILE_NAME", "x") as f:
    f.write(full_text)




