import os
from datetime import datetime

from docxtpl import DocxTemplate
from dotenv import load_dotenv
from openai import OpenAI

JOB_TITLE = "SEM Specialist"
COMPANY_NAME = "TikTok"
USER = "firstlast"

doc = DocxTemplate(f"/Users/{USER}/python-queen/resume_gen/test.docx")

load_dotenv(f"/Users/{USER}/python-queen/.env")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  # This is the default and can be omitted
)


def get_blurb():
    prompt = f"Write a 3-4 sentence blurb for the end of my cover letter expressing interest in being a {JOB_TITLE} as {COMPANY_NAME}."
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4o",
    )

    print(chat_completion.choices[0].text)


def get_date():
    date = datetime.now()
    date_str = date.strftime("%-m/%-d/%y")
    return date_str


def get_hiring_manager(hiring_manager_name: str = None):
    if hiring_manager_name:
        return hiring_manager_name
    else:
        return "Hiring Manager"


def main():
    context = {
        "date": get_date(),
        "hiring_manager_name": get_hiring_manager(),
        "job_title": JOB_TITLE,
        "company_name": COMPANY_NAME,
    }
    doc.render(context)
    doc.save("test_v2.docx")

if __name__ == "__main__":
    main()
