from bs4 import BeautifulSoup
import requests
import os

COURSE_CODES = [
    "EDAN20", "EDAP20", "FMSF10",
    "FRTN65", "FRTN85", "FRTN50"
]

FILE_NAME = "machine_intelligence_courses.txt"
HEADERS = ["aim", "learning outcomes", "contents"] # assuming header names are consistent across all course web pages

#
def get_body_text(header) -> str:
    text = ""
    for elem in header.next_siblings:
        if elem.name == 'h2':
            return text.strip()
        elif elem.name == 'p':
            text += f"{elem.text}\n"
        elif elem.name == 'ul':
            for li in elem.find_all('li'):
                text += f'- {li.text}\n'
            text += '\n'

    raise Exception("SHOULD NOT HAPPEN: next <h2> tag not found")


os.chdir(os.path.dirname(os.path.realpath(__file__)))
full_text = ""
if not os.path.exists(FILE_NAME):
    text = ""
    for code in COURSE_CODES:
        r = requests.get(
            f'https://kurser.lth.se/kursplaner/23_24%20eng/{code}.html')
        soup = BeautifulSoup(r.text, 'html.parser')

        course_name = soup.h1.text.splitlines()[1].upper()
        h2s = [h for h in soup.find_all('h2') if h.text.lower() in HEADERS]

        text += f"{course_name}\n"
        for h in h2s:
            text += f"{h.text}:\n"
            text += f"{get_body_text(h)}\n"
            text += "\n"

    text = text.strip()
    with open(FILE_NAME, 'w') as file:
        print(f"word count: {len(text.split())}")
        file.write(text)

else:
    print("File already exists")
