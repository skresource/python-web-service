from jira import JIRA, JIRAError

class JiraService:
    """Service for handling JIRA operations."""

    def __init__(self, server: str, username: str, api_token: str):
        if not all([server, username, api_token]):
            raise ConnectionError("JIRA connection details are missing.")
        try:
            self.jira = JIRA(
                options={'server': server},
                basic_auth=(username, api_token)
            )
        except JIRAError as e:
            print(f"Error connecting to JIRA: {e}")
            raise ConnectionError("Failed to connect to JIRA.") from e

    def _prepare_issue_dict(self, project_key: str, issue_type: str, details: dict, asigned_to: str, parentId: str) -> dict:
        """Prepares the dictionary for creating a JIRA issue."""
        if issue_type == "bug":
            description = details.get('description', '')            
            steps = details.get('steps_to_reproduce', [])
            summary = description.split('\n')[0][:80] if description else "Bug Report"
            full_description = f"{description}\n\n*Steps to Reproduce:*\n"
            full_description += "".join([f"- {step}\n" for step in steps])
            return {
                'project': {'key': project_key},
                'summary': summary,
                'description': full_description,
                'assignee':   {'accountId': asigned_to},
                'issuetype': {'name': 'Bug'},
            }
        else: # 'story'
            summary = details.get('summary', 'AI Generated Story')
            description = details.get('description', '')
            acceptance_criteria = details.get('acceptance_criteria', [])
            story_points = details.get('story_points')
            assignee = asigned_to
            parent = parentId
            full_description = f"{description}\n\n*Acceptance Criteria:*\n"
            full_description += "".join([f"- {criteria}\n" for criteria in acceptance_criteria])
            issue_data = {
                'project': {'key': project_key},
                'summary': summary,
                'description': full_description,
                'issuetype': {'name': 'Story'},
            }
            

            
            # if assignee:
            # issue_data['assignee'] =   {'accountId': '712020:f19737b7-15f3-4ca1-86cb-a9d845357bc6'}
            issue_data['assignee'] =   {'accountId': asigned_to}
            # issue_data['customfield_10007'] = parent
            # "customfield_10007": "EPIC_KEY_HERE"
             
            # if parent:
            #     issue_data['parent'] = { 'key': parent }
            #     print("\033[94m#### Parent id set to ####\033[0m")
            #     print(f"\033[94m{parent}\033[0m")
            print(f"Issue data: {issue_data}")   
            # return false error
            return issue_data
        

    def create_jira_issue(self, project_key: str, issue_type: str, details: dict, asigned_to: str, parentId: str) -> str:
        """Creates a JIRA issue (story or bug)."""
        issue_dict = self._prepare_issue_dict(project_key, issue_type, details, asigned_to, parentId)
        print(f"Creating JIRA issue: {issue_dict}")
        try:
            new_issue = self.jira.create_issue(fields=issue_dict)
            return new_issue.key
        except JIRAError as e:
            print(f"Error creating JIRA issue: {e}")
            raise RuntimeError("Failed to create JIRA issue.") from e


    def update_story_points(self, issue_key: str, points: int) -> bool:
        """Updates the story points for a given JIRA issue."""
        try:
            issue = self.jira.issue(issue_key)
            # The custom field ID for Story Points can vary. 
            # 'customfield_10016' is a common default, but you should verify it in your JIRA instance.
            issue.update(fields={'customfield_10016': points})
            print(f"Successfully updated story points for {issue_key} to {points}.")
            return True
        except JIRAError as e:
            print(f"Error updating story points for {issue_key}: {e}")
            return False
