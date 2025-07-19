# imports

import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from openai import OpenAI

# If you get an error running this cell, then please head over to the troubleshooting notebook!

load_dotenv(override=True)
print(os.getcwd())
print(os.listdir())
# Load environment variables in a file called .env

api_key = os.getenv('OPENAI_API_KEY')
 # Check the key
if not api_key:
    print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
elif not api_key.startswith("sk-proj-"):
    print("An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook")
elif api_key.strip() != api_key:
    print("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook")
else:
    print("API key found and looks good so far!")


openai = OpenAI()

# To give you a preview -- calling OpenAI with these messages is this easy. Any problems, 
#  head over to the Troubleshooting notebook.

message = "Hello, GPT! This is my first ever message to you! Hi!"
response = openai.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":message}])
print(response.choices[0].message.content)

# A class to represent a Webpage
# If you're not familiar with Classes, check out the "Intermediate Python" notebook

# Some websites need you to use proper headers when fetching them:
headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:

    def __init__(self, url):
        self.model="gpt-4o-mini"
        #self.model="gpt-3.5-turbo"
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)

        # Define our system prompt - you can experiment with this later, changing the last sentence to 
        # 'Respond in markdown in Spanish."
        self.system_prompt = "You are an assistant that analyzes the contents of a website \
        and provides a short summary, ignoring text that might be navigation related. \
        Respond in markdown."

        self.user_prompt = self.user_prompt_for()
        self.messages = [{"role": "system", "content": "You are a snarky assistant"},{"role": "user", "content": "What is 2 + 2?"}]

        # To give you a preview -- calling OpenAI with system and user messages:
        self.response = openai.chat.completions.create(
            model=self.model,
            messages=self.messages
        )
        print(self.response.choices[0].message.content)

    def messages_for(self):
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.user_prompt}
        ]

    # A function that writes a User Prompt that asks for summaries of websites:
    def user_prompt_for(self):
        website = self.url
        print(f"Creating user prompt for {website}")
        user_prompt = f"You are looking at a website titled {self.title}"
        user_prompt += "\n The contents of this website is as follows; \
        please provide a short summary of this website in markdown. \
        If it includes news or announcements, then summarize these too.\n\n"
        user_prompt += self.text
        return user_prompt
    
    def summarize(self):        
        response = openai.chat.completions.create(
            model = self.model,             
            messages = self.messages_for()
        )
        return response.choices[0].message.content

    def display_summary(self):
        summary = self.summarize()        
        return  Markdown(summary)
        
        
    

# Let's try one out. Change the website and add print statements to follow along.

# ed = Website("https://edwarddonner.com")
ed = Website("https://www.livemint.com/") 

md_obj = ed.display_summary()
print(md_obj.data)  # This prints the markdown string inside the Markdown object