import os
import requests
from crewai import Agent, Task, Crew
from requests.auth import HTTPBasicAuth
from langchain_openai import ChatOpenAI

# ----- Jira API Tool -----
class JiraTool:
    def __init__(self, base_url, username, api_token):
        self.base_url = base_url.rstrip('/')
        self.auth = HTTPBasicAuth(username, api_token)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def get_ticket(self, ticket_id):
        url = f"{self.base_url}/rest/api/3/issue/{ticket_id}"
        response = requests.get(url, headers=self.headers, auth=self.auth, timeout=10)
        response.raise_for_status()
        return response.json()

    def add_comment(self, ticket_id, comment):
        comment_data = {
            "body": {
                "version": 1,
                "type": "doc",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": comment
                            }
                        ]
                    }
                ]
            }
        }

        url = f"{self.base_url}/rest/api/3/issue/{ticket_id}/comment"
        response = requests.post(url, json=comment_data, headers=self.headers, auth=self.auth, timeout=10)

        if response.status_code == 201:
            return True
        else:
            print(f"⚠️ Jira API returned {response.status_code}: {response.text}")
            return False

# ----- Agent Definition -----
jira_admin = Agent(
    role="Jira Test Plan Generator",
    goal="Create and document test plans from Jira ticket descriptions",
    backstory="You are a QA engineer responsible for ensuring every Jira ticket has a proper test plan.",
    verbose=True,
    allow_delegation=False
)

# ----- Tasks -----
extract_ticket_info = Task(
    description="Extract key functional requirements, AC, and edge cases from the Jira ticket: {jira_ticket_text}. Also review any recent comments to capture changes, clarifications, or additional requirements that could affect the test plan.",
    expected_output="Structured summary including purpose, workflows to validate, edge cases, and relevant updates or changes found in ticket comments.",
    agent=jira_admin
)

generate_test_plan = Task(
    description="Using the extracted summary, generate a markdown test plan with test case breakdowns (happy path, edge, negative)",
    expected_output="A complete markdown-formatted test plan ready to be added to Jira.",
    agent=jira_admin
)

update_jira_ticket = Task(
    description="Take the generated test plan and add it as a comment to the original Jira ticket.",
    expected_output="Confirmation that the Jira ticket was updated.",
    agent=jira_admin
)

# ----- Main Execution Function -----
def run_test_plan_generation(ticket_id, jira_base_url, jira_email, jira_token, llm):
    jira = JiraTool(jira_base_url, jira_email, jira_token)
    ticket_data = jira.get_ticket(ticket_id)

    summary = ticket_data['fields'].get('summary', '')
    description = ticket_data['fields'].get('description', '')
    ticket_text = f"Summary: {summary}\n\nDescription: {description}"

    crew = Crew(
        agents=[jira_admin],
        tasks=[extract_ticket_info, generate_test_plan, update_jira_ticket],
        llm=llm
    )

    result = crew.kickoff(inputs={"jira_ticket_text": ticket_text})

    final_output = result.output if hasattr(result, 'output') else str(result)
    if final_output and len(final_output.strip()) >= 30:
        success = jira.add_comment(ticket_id, final_output)
        print("✅ Jira updated:" if success else f"❌ Failed to update Jira for {ticket_id}")
    else:
        print(f"⚠️ Skipping Jira comment for {ticket_id}: result was empty or too short.")

# ----- Script Entry Point for GitHub Action -----
if __name__ == '__main__':
    ticket_ids = os.environ['JIRA_TICKET_IDS'].split(',')
    jira_base_url = os.environ['JIRA_BASE_URL']
    jira_email = os.environ['JIRA_USER_EMAIL']
    jira_token = os.environ['JIRA_API_TOKEN']
    openai_api_key = os.environ['OPENAI_API_KEY']

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.3,
        api_key=openai_api_key
    )

    for raw_id in ticket_ids:
        ticket_id = raw_id.strip()
        print(f"\n🧾 Processing ticket: {ticket_id}")
        try:
            run_test_plan_generation(ticket_id, jira_base_url, jira_email, jira_token, llm)
        except Exception as e:
            print(f"❌ Failed to process {ticket_id}: {e}")
