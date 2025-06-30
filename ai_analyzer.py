from google import genai
from google.genai import types

class AIAnalyzer:
    def __init__(self, key: str):
        self.client = genai.Client(api_key=key)

    def summarize_repo(self, repo_data):
        desc = repo_data[0]
        readme = repo_data[1]

        summary = self.client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction="You are a repository analyzer. You'll be given a repository description and readme file contents if available."),
            contents="Summarize the purpose of this repo:\n\
description: " + desc +"\n\
readme: " + readme,
        )

        return summary.text