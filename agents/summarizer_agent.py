import os
import json
from crewai import Agent
from openai import OpenAI

class SummarizerAgent:
    """Agent responsible for creating concise summaries of meeting transcriptions"""
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.mock_mode = os.getenv("MOCK_MODE", "false").lower() == "true"
        
    def create_agent(self):
        """Create and return the summarizer agent"""
        return Agent(
            role="Meeting Summarizer",
            goal="Create clear, concise summaries of meeting discussions that capture key points and decisions",
            backstory="""You are a skilled meeting facilitator and note-taker with extensive 
            experience in distilling complex discussions into clear, actionable summaries. 
            You excel at identifying the most important points, decisions made, and topics 
            discussed while maintaining the context and nuance of the conversation.""",
            verbose=True,
            allow_delegation=False
        )
    
    def summarize_meeting(self, transcript):
        """
        Generate a summary of the meeting transcript
        
        Args:
            transcript (str): The meeting transcript text
            
        Returns:
            str: Meeting summary in markdown format
        """
        if self.mock_mode:
            return self._get_mock_summary()
        
        try:
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            prompt = f"""Please create a comprehensive meeting summary from the following transcript. 
            Structure your response in markdown format with the following sections:

            ## Meeting Overview
            Brief description of the meeting purpose and attendees

            ## Key Discussion Points
            Main topics that were discussed

            ## Decisions Made
            Any decisions or agreements reached during the meeting

            ## Next Steps
            General next steps or follow-up items mentioned

            Here's the transcript to summarize:

            {transcript}
            
            Please provide a clear, professional summary that captures the essence of the meeting."""

            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert meeting summarizer. Create clear, well-structured summaries in markdown format."
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
            raise Exception(f"Failed to generate meeting summary: {str(e)}")
    
    def _get_mock_summary(self):
        """Return mock summary for testing purposes"""
        return """## Meeting Overview
This was a project planning meeting led by Sarah (Project Manager) with team members John (Development), Lisa (Design), and Mike (QA) to review sprint progress and coordinate upcoming tasks.

## Key Discussion Points
- **API Development Progress**: John reported 70% completion of user authentication API
- **Database Schema Issues**: Discovered problems with user profile structure requiring design input
- **Testing Preparation**: Mike has prepared test cases and is ready to begin testing
- **Environment Setup**: Staging environment needs updating for comprehensive testing

## Decisions Made
- Lisa will collaborate with John to resolve database schema issues
- Testing will commence after API completion
- Team will reconvene next Monday for progress review

## Next Steps
- Continue API development with focus on completion by Friday
- Resolve database schema issues through design-development collaboration
- Update staging environment to support full test suite execution
- Prepare for comprehensive testing phase following API completion"""
