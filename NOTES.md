## GitHub + GenAI Analysis Tool

### **Repository Insights and Summaries**

- Summarize repository purpose using `README.md` and key files.
- Detect project type (e.g., web app, package) based on directory and file structure.
- Offer a brief description of the last commit, with date.
- List the amount of open issues.

### **Code Quality & Issues**

- Use GenAI to:
    - Find potential bugs in key files.
    - Detect lack of documentation.

### **Tech Stack & Usage Metrics**

- Analyze the languages, frameworks, and libraries used in the repo.
- Visualize dependency trees or top-used modules.

### **Natural Language Queries**

Let users ask things like:

- “What does this project do?”
- “How does the authentication system work?”
- “Which file is responsible for the database connection?”

---

## Project Info

### **Name of Project**

Repo Intel

---

### **What problem are you solving?**



---

### **Who / What does the project interface with?**

- **Users**: Students, developers, recruiters
- **APIs**: GitHub REST API, Google GenAI API

---

### **What are the inputs?**

- GitHub username (or repo URL)
- Optional: Filename for deep code inspection
- Optional: Natural language question

---

### **What are the outputs?**

- Repo summary and purpose
- AI-generated insights on selected files
- Bug reports or improvement suggestions
- Project health checklist and score
- Suggested questions or README additions

---

### **5 Steps From Input → Output**

1. User submits GitHub username or repo link.
2. Tool fetches repo metadata and file structure via GitHub API.
3. User selects files or uses preset analysis prompts.
4. File contents and context are passed to GenAI for analysis.
5. Tool outputs summary, suggestions, and potential issues.

---

### **What’s the biggest risk?**

- Handling large repositories efficiently
- Prompt engineering for GenAI
- Rate-limiting from Google GenAI API usage.

---

### **How will you know you're successful?**

- Accurate and meaningful AI summaries that match human-written ones.
- Users report actionable insights from the tool.
