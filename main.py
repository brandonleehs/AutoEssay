import os
from dotenv import load_dotenv, set_key
from pathlib import Path
import google.generativeai as genai
from docx import Document

def configure():
    load_dotenv()

def main():
    configure()

    genai.configure(api_key=os.environ["API_KEY"])

    model = genai.GenerativeModel("gemini-1.5-flash")

    # Read CURRENT_INDEX value
    if "CURRENT_INDEX" in os.environ:
        CURRENT_INDEX = int(os.environ["CURRENT_INDEX"])
    else:
        CURRENT_INDEX = 0
    
    with open("mods.txt") as f:
        mod_lst = f.read().splitlines()
        for mod in mod_lst[CURRENT_INDEX:CURRENT_INDEX + 10]:
            prompt = f"Write a 500-word undergraduate-level note about {mod}. The note should provide an overview of the key concepts, theories, and practical applications associated with {mod}. Start with a brief introduction that defines {mod} and its significance in the field of study. Then, discuss the main points or arguments, including any notable research or case studies that have shaped understanding of this topic. Ensure that the note is clear, well-structured, and avoids overly technical jargon, making it accessible to other students. Conclude with a brief reflection on how {mod} could be relevant to real-world issues or further academic inquiry."
            response = model.generate_content(prompt)
            document = Document()
            for paragraph in response.text.split("\n\n"):
                document.add_paragraph(paragraph)
            document.save(f"{mod}.docx")

    # Save updated index to .env
    env_path = Path().resolve() / ".env"
    set_key(dotenv_path = env_path, key_to_set = "CURRENT_INDEX", value_to_set = str(CURRENT_INDEX + 10))

if __name__ == "__main__":
    main()



