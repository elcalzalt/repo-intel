from google import genai
from google.genai import types
import os

class AIAnalyzer:
    def __init__(self, key: str):
        # Initialize AI client with provided API key and set base directory for instructions
        self.client = genai.Client(api_key='AIzaSyDg0zwD9K4PD8vBgoFIUHARYOrG7Q2VlT8')
        self.base_dir = os.path.dirname(__file__)

    def commit_str(self, commit):
        # Build a string representation of a commit message and its patches
        commit_message = commit[0]
        commit_patches = commit[1]

        cstr = ""
        if commit_message is not None:
            cstr += "message:\n" + commit_message + "\n"

        if commit_patches is not None:
            cstr += "patches:\n" + "".join(patch + "\n" for patch in commit_patches)

        return cstr

    def issues_str(self, issues):
        # Build a string representation of a list of open issues
        num_issues = len(issues)

        if num_issues == 0:
            return "no open issues provided"

        istr = ""
        for i in range(len(issues)):
            istr += f"issue {i+1}:\n"
            istr += "title: " + issues[i][0] + "\n"
            istr += "body:\n" + issues[i][1] + "\n"
            istr += "created date: " + issues[i][2] + "\n"

        return istr

    def summarize(self, repo_data) -> str:
        # Summarize repository data using the AI model and provided instructions
        name = repo_data[0]
        desc = "no description provided" if repo_data[1] is None else repo_data[1]        
        readme = "no readme provided" if repo_data[2] is None else repo_data[2]
        latest_commit = repo_data[3]
        open_issues = repo_data[4]


        instr_path = os.path.join(self.base_dir, 'summary_instruction.txt')
        with open(instr_path, 'rt') as system_instruction_file:
            system_instruction_contents = system_instruction_file.read()
        system_instruction_file.close()
        summary = self.client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction_contents),
            contents="Summarize the given repo using the information provided:\n\
name: " + name +"\n\
description:\n" + desc +"\n\
readme:\n" + readme +"\n\
latest commit:\n" + self.commit_str(latest_commit) +"\n\
latest five open issues:\n" + self.issues_str(open_issues) + "\n",
        )

        if type(summary.text) is not str:
            return "Unable to complete report"
        return summary.text

    def scan_file(self, file_path, contents) -> str:
        # Scan the given file for vulnerabilities using the AI model
        instr_path = os.path.join(self.base_dir, 'scan_instruction.txt')
        with open(instr_path, 'rt') as system_instruction_file:
            system_instruction_contents = system_instruction_file.read()
        system_instruction_file.close()

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction_contents),
            contents="Scan the given file for vulnerabilities:\n\
file path: " + file_path + "\n\
file contents:\n" + contents + "\n",
        )

        if type(response.text) is not str:
            return "Unable to complete report"
        return response.text

    def answer_question(self, file_path, contents, question) -> str:
        # Scan the given file and answer the question provided
        instr_path = os.path.join(self.base_dir, 'qna_instruction.txt')
        with open(instr_path, 'rt') as system_instruction_file:
            system_instruction_contents = system_instruction_file.read()
        system_instruction_file.close()

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction_contents),
            contents="Scan the given file and answer the question:\n\
file path: " + file_path + "\n\
file contents:\n" + contents + "\n\
question:\n" + question + "\n",
        )

        if type(response.text) is not str:
            return "Unable to complete report"
        return response.text