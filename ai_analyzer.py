from google import genai
from google.genai import types

class AIAnalyzer:
    def __init__(self, key: str):
        self.client = genai.Client(api_key=key)

    def summarize_repo(self, repo_data):
        name = repo_data[0]
        desc = repo_data[1]
        readme = repo_data[2]
        commit = repo_data[3]
        issues = repo_data[4]

        system_instruction_file = open("summary_instruction.txt", "rt")
        system_instruction_contents = system_instruction_file.read()
        system_instruction_file.close()
        summary = self.client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction_contents),
            contents="Summarize the given repo using the information provided:\n\
name: " + name +"\n\
description: \n" + desc +"\n\
readme: \n" + readme +"\n\
latest commit: \n" + commmit +"\n\
latest issues: \n" + issues + "\n",
        )

        return summary.text