import os
import json
from crewai import Agent
from openai import OpenAI
from datetime import datetime

class FollowupAgent:
    """Agent responsible for creating follow-up messages and communications"""
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.mock_mode = os.getenv("MOCK_MODE", "false").lower() == "true"
        
    def create_agent(self):
        """Create and return the follow-up agent"""
        return Agent(
            role="Follow-up Coordinator",
            goal="Create professional follow-up communications that clearly outline meeting outcomes and next steps",
            backstory="""You are an experienced executive assistant and communication specialist 
            with expertise in crafting clear, professional follow-up messages. You excel at 
            organizing information in a way that's easy to understand and act upon, ensuring 
            that all stakeholders are aligned on next steps and responsibilities.""",
            verbose=True,
            allow_delegation=False
        )
    
    def create_followup_message(self, summary, action_items, attendees=None):
        """
        Create a follow-up message based on meeting summary and action items
        
        Args:
            summary (str): Meeting summary
            action_items (list): List of action items
            attendees (list): List of meeting attendees (optional)
            
        Returns:
            str: Professional follow-up message
        """
        if self.mock_mode:
            return self._get_mock_followup_message()
        
        try:
            # Prepare action items text
            action_items_text = self._format_action_items(action_items)
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            prompt = f"""Create a professional follow-up email based on the meeting summary and action items below. 
            The email should be well-structured, clear, and actionable. Include:

            1. A brief greeting and meeting reference
            2. Key meeting highlights
            3. Clearly formatted action items with owners and deadlines
            4. Professional closing

            Meeting Summary:
            {summary}

            Action Items:
            {action_items_text}

            Format the email professionally with proper structure and clear sections."""

            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional executive assistant creating follow-up communications. Write clear, actionable, and well-structured emails."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Failed to create follow-up message: {str(e)}")
    
    def _format_action_items(self, action_items):
        """Format action items for inclusion in follow-up message"""
        if not action_items:
            return "No specific action items were identified."
        
        formatted_items = []
        for i, item in enumerate(action_items, 1):
            task = item.get("task", "No task specified")
            owner = item.get("owner", "Not assigned")
            deadline = item.get("deadline", "No deadline specified")
            priority = item.get("priority", "Medium")
            
            formatted_items.append(
                f"{i}. {task}\n   - Owner: {owner}\n   - Deadline: {deadline}\n   - Priority: {priority}"
            )
        
        return "\n\n".join(formatted_items)
    
    def _get_mock_followup_message(self):
        """Return mock follow-up message for testing purposes"""
        return f"""Subject: Follow-up: Project Planning Meeting - {datetime.now().strftime('%B %d, %Y')}

Dear Team,

Thank you for your participation in today's project planning meeting. This follow-up email summarizes our discussion and outlines the action items we agreed upon.

## Meeting Highlights

We made excellent progress reviewing our current sprint status. The user authentication API development is 70% complete, and we've identified some database schema issues that need immediate attention. Our testing preparation is on track, with test cases ready for implementation.

## Action Items

1. Complete user authentication API development
   - Owner: John
   - Deadline: Friday
   - Priority: High

2. Resolve database schema issues for user profile structure
   - Owner: Lisa
   - Deadline: Wednesday
   - Priority: High

3. Schedule session with John to review user profile requirements
   - Owner: Lisa
   - Deadline: Tomorrow morning
   - Priority: High

4. Update staging environment for testing
   - Owner: Not specified
   - Deadline: Thursday
   - Priority: Medium

5. Begin comprehensive testing of authentication flow
   - Owner: Mike
   - Deadline: After API completion
   - Priority: Medium

6. Attend follow-up meeting to review progress
   - Owner: All team members
   - Deadline: Next Monday
   - Priority: Medium

## Next Steps

Please ensure all action items are completed by their respective deadlines. If you encounter any blockers or need additional resources, please reach out immediately.

Our next progress review meeting is scheduled for Monday. Please come prepared with updates on your assigned tasks.

Best regards,
Meeting Coordinator

---
This follow-up was generated automatically by the Meeting Summarizer & Action Tracker system."""
