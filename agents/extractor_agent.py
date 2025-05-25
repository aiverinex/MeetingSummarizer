import os
import json
from crewai import Agent
from openai import OpenAI

class ExtractorAgent:
    """Agent responsible for extracting action items from meeting transcripts"""
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.mock_mode = os.getenv("MOCK_MODE", "false").lower() == "true"
        
    def create_agent(self):
        """Create and return the extractor agent"""
        return Agent(
            role="Action Item Extractor",
            goal="Identify and extract specific action items, tasks, and deliverables with clear ownership and deadlines",
            backstory="""You are a meticulous project coordinator with a talent for identifying 
            actionable tasks from meeting discussions. You have a keen eye for spotting commitments, 
            deadlines, and responsibilities mentioned throughout conversations. Your extractions 
            are precise, well-organized, and help teams stay accountable to their commitments.""",
            verbose=True,
            allow_delegation=False
        )
    
    def extract_action_items(self, transcript):
        """
        Extract action items from meeting transcript
        
        Args:
            transcript (str): The meeting transcript text
            
        Returns:
            list: List of action items with task, owner, and deadline
        """
        if self.mock_mode:
            return self._get_mock_action_items()
        
        try:
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            prompt = f"""Analyze the following meeting transcript and extract all action items, 
            tasks, and commitments. For each action item, identify:

            1. The specific task or action to be completed
            2. The person responsible (owner)
            3. The deadline or timeframe (if mentioned)
            4. Any additional context or dependencies

            Format your response as a JSON array where each action item is an object with these fields:
            - "task": Clear description of what needs to be done
            - "owner": Person responsible for the task
            - "deadline": Deadline or timeframe (use "Not specified" if not mentioned)
            - "priority": Estimated priority level (High/Medium/Low based on context)
            - "context": Any additional relevant information or dependencies

            Here's the transcript to analyze:

            {transcript}

            Respond with only valid JSON format."""

            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at extracting action items from meeting transcripts. Respond only with valid JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=800,
                temperature=0.1
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Ensure the result is a list of action items
            if isinstance(result, dict) and "action_items" in result:
                return result["action_items"]
            elif isinstance(result, list):
                return result
            else:
                return []
            
        except Exception as e:
            raise Exception(f"Failed to extract action items: {str(e)}")
    
    def _get_mock_action_items(self):
        """Return mock action items for testing purposes"""
        return [
            {
                "task": "Complete user authentication API development",
                "owner": "John",
                "deadline": "Friday",
                "priority": "High",
                "context": "70% complete, final 30% remaining"
            },
            {
                "task": "Resolve database schema issues for user profile structure",
                "owner": "Lisa",
                "deadline": "Wednesday",
                "priority": "High",
                "context": "Requires collaboration with John on database schema"
            },
            {
                "task": "Schedule session with John to review user profile requirements",
                "owner": "Lisa",
                "deadline": "Tomorrow morning",
                "priority": "High",
                "context": "Dependencies: Database schema resolution"
            },
            {
                "task": "Update staging environment for testing",
                "owner": "Not specified",
                "deadline": "Thursday",
                "priority": "Medium",
                "context": "Required for Mike to run full test suite"
            },
            {
                "task": "Begin comprehensive testing of authentication flow",
                "owner": "Mike",
                "deadline": "After API completion",
                "priority": "Medium",
                "context": "Test cases already prepared, waiting for API completion"
            },
            {
                "task": "Attend follow-up meeting to review progress",
                "owner": "All team members",
                "deadline": "Next Monday",
                "priority": "Medium",
                "context": "Regular progress review meeting"
            }
        ]
