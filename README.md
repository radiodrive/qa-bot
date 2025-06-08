# QA-Bot 🧪🤖

QA-Bot is an AI-powered automation assistant that generates structured test plans directly from Jira tickets using CrewAI and OpenAI (GPT-3.5). It integrates with GitHub Actions to run on demand and posts test plans as comments back to the relevant Jira tickets.

---

## ✅ Features (Current)

### 🎯 Test Plan Generator from Jira Ticket
- Reads Jira ticket summary and description
- Optionally considers recent comments (for changes or clarifications)
- Generates a test plan using GPT-3.5 via CrewAI
- Posts it as a structured comment back to the Jira ticket
- Runs via GitHub Actions using a manual trigger

### 🔐 Required GitHub Secrets
| Secret Name         | Description                              |
|---------------------|------------------------------------------|
| `JIRA_API_TOKEN`    | Your Jira API token                      |
| `JIRA_BASE_URL`     | Your Jira base URL (e.g. `https://...`)  |
| `JIRA_USER_EMAIL`   | Email associated with the API token      |
| `OPENAI_API_KEY`    | Your OpenAI API key (for GPT-3.5)        |

---

## 🚀 How It Works

1. Workflow is triggered manually in GitHub Actions (pass Jira ticket ID)
2. The Python script fetches the ticket, constructs a CrewAI task
3. GPT-3.5 generates a test plan
4. QA-Bot posts the test plan back to Jira as an ADF-formatted comment

---

## 📁 Structure

```bash
qa-bot/
├── .github/
│   └── workflows/
│       └── qa-bot.yml            # GitHub Actions workflow
├── scripts/
│   └── generatetestplan.py      # Main logic (CrewAI + Jira + LLM)
├── requirements.txt             # Python dependencies
└── README.md                    # 📄 You're here!
```

---

## 🛠️ Planned Enhancements (Roadmap)

### ✅ PR Diff → Test Case Generator
- Automatically generate tests from GitHub pull request diffs
- Post proposed tests in PR comments or linked Jira ticket

### ✅ Regression Risk Estimator
- Use LLM to identify impacted areas of the system
- Flag tickets or PRs with high regression risk labels

### ✅ Cucumber Feature Skeleton Generator
- Convert generated test plans into `.feature` files
- Optional PR or Gherkin preview in comment

### ✅ Jira Test Coverage Validator
- Periodic audit of tickets missing test plans, test evidence, or ACs

### ✅ Flaky Test Detector
- Analyze test run history to flag unstable test scenarios
- Post summaries in Slack or GitHub issues

### ✅ QA Evidence Reviewer
- Let the LLM assess screenshots, logs, or descriptions
- Flag missing steps or inconsistencies in evidence

### ✅ Slack QA Assistant
- Ask "What do I need to test for WYN-456?"
- Get test plan links, open bugs, past scenarios

---

## 🙌 Contributions
Feel free to fork, clone, or extend. PRs welcome for integrations with Cypress, Serenity, Playwright MCP, etc.

---

## 💬 Questions?
Message the team or file an issue. QA-Bot is here to make quality effortless!
