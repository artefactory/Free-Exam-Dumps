import requests
from bs4 import BeautifulSoup
import json


def fetch_page_content(url):
    """Fetch the webpage content from the given URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None


def parse_exam_question(html_content):
    """Parse the HTML content and extract exam question details."""
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract question
    question_text = soup.find("div", class_="question-body").get_text(
        strip=True, separator=" "
    )

    # Extract answer choices
    choices = {}
    for li in soup.find_all("li", class_="multi-choice-item"):
        choice_letter = (
            li.find("span", class_="multi-choice-letter").text.strip().replace(".", "")
        )
        choice_text = (
            li.get_text(strip=True, separator=" ").replace(choice_letter, "", 1).strip()
        )
        choices[choice_letter] = choice_text

    # Extract suggested answer
    suggested_answer = soup.find("span", class_="correct-answer").text.strip()

    # Extract community vote distribution
    votes_script = soup.find("script", type="application/json")
    vote_distribution = json.loads(votes_script.string) if votes_script else []

    return {
        "question": question_text,
        "choices": choices,
        "suggested_answer": suggested_answer,
        "vote_distribution": vote_distribution,
    }


def main():
    url = "https://www.examtopics.com/discussions/amazon/view/147689-exam-aws-certified-machine-learning-specialty-topic-1/"
    html_content = fetch_page_content(url)

    if html_content:
        parsed_data = parse_exam_question(html_content)

        print("\n**Exam Question:**")
        print(parsed_data["question"])

        print("\n**Answer Choices:**")
        for choice, text in parsed_data["choices"].items():
            print(f"{choice}: {text}")

        print("\n**Suggested Answer:**")
        print(parsed_data["suggested_answer"])

        print("\n**Community Vote Distribution:**")
        for vote in parsed_data["vote_distribution"]:
            print(f"{vote['choice']}: {vote['percentage']}")


if __name__ == "__main__":
    main()
