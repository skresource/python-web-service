import json
import google.generativeai as genai
from app.config import Config

class AIService:
    """Service fo handling AI operations"""

    def __init__(self, api_key: str):   
        if not api_key:
            raise ValueError("API key is required")
        genai.configure(api_key=api_key)
         
        

    def _get_system_prompt(self, issue_type: str) -> str:
        """Returns the appropriate system prompt based on the issue type."""
        if issue_type == "bug":
            return """
                You are an expert in Agile development and creating JIRA bugs.
                Based on the user's request, generate a JSON object with two keys: "description" and "steps_to_reproduce".
                - "description": A detailed explanation of the bug.
                - "steps_to_reproduce": An array of strings, each describing a step to reproduce the bug.
                Do NOT include a summary or acceptance criteria.
                """
        else:  # 'story'
            return """
                You are an expert in Agile development and creating JIRA stories.
                Based on the user's request, generate a JSON object with three keys: "summary", "description", and "acceptance_criteria".
                - "summary": A concise, one-sentence title for the JIRA story.
                - "description": A detailed explanation of the user story, in the format 'As a [user], I want [goal] so that [reason]' if applicable.
                - "acceptance_criteria": An array of strings, where each string is a specific, testable criterion.
                """

    def generate_jira_issue_details(self, prompt: str, issue_type: str) -> dict:
        """Generates JIRA issue details using the Gemini model."""
        system_prompt = self._get_system_prompt(issue_type)
        model = genai.GenerativeModel(
            'gemini-1.5-flash',
            generation_config={"response_mime_type": "application/json"},
            system_instruction=system_prompt
        )

        try:
            response = model.generate_content(prompt)
            return json.loads(response.text)
        except json.JSONDecodeError as e:
            print(f"Error parsing AI response as JSON: {e}")
            raise ValueError("Failed to parse AI response.") from e
        except Exception as e:
            print(f"Gemini API error: {e}")
            raise RuntimeError("An error occurred with the AI service.") from e
       