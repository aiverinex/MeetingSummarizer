import os
from crewai import Agent
from openai import OpenAI

class TranscriberAgent:
    """Agent responsible for transcribing audio files to text using OpenAI Whisper API"""
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.mock_mode = os.getenv("MOCK_MODE", "false").lower() == "true"
        
    def create_agent(self):
        """Create and return the transcriber agent"""
        return Agent(
            role="Meeting Transcriber",
            goal="Accurately transcribe audio recordings of meetings into clear, readable text",
            backstory="""You are an expert transcription specialist with years of experience 
            in converting audio recordings to text. You have a keen ear for detail and can 
            handle various accents, speaking speeds, and audio qualities. Your transcriptions 
            are known for their accuracy and proper formatting.""",
            verbose=True,
            allow_delegation=False
        )
    
    def transcribe_audio(self, audio_file_path):
        """
        Transcribe audio file to text
        
        Args:
            audio_file_path (str): Path to the audio file
            
        Returns:
            str: Transcribed text
        """
        if self.mock_mode:
            return self._get_mock_transcription()
        
        try:
            # Check if file exists
            if not os.path.exists(audio_file_path):
                raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
            
            with open(audio_file_path, "rb") as audio_file:
                response = self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            return response
        except Exception as e:
            raise Exception(f"Failed to transcribe audio: {str(e)}")
    
    def _get_mock_transcription(self):
        """Return mock transcription for testing purposes"""
        return """Good morning everyone, thank you for joining today's project planning meeting. 
        I'm Sarah, the project manager, and we have John from development, Lisa from design, 
        and Mike from QA with us today.

        Let's start with our agenda. First, we need to review the current sprint progress. 
        John, can you give us an update on the API development?

        John: Sure Sarah. We've completed about 70% of the user authentication API. 
        The remaining work should be done by Friday. However, we discovered some issues 
        with the database schema that might require Lisa's input on the user profile structure.

        Sarah: That's great progress John. Lisa, can you work with John to resolve the 
        database schema issues by Wednesday?

        Lisa: Absolutely, I'll schedule a session with John tomorrow morning to go through 
        the user profile requirements and update the database schema accordingly.

        Sarah: Perfect. Mike, how are we looking on the testing front?

        Mike: I've prepared the test cases for the authentication flow and I'm ready to 
        start testing as soon as the API is complete. I'll need the staging environment 
        to be updated by Thursday to run the full test suite.

        Sarah: Great. So our action items are: John to complete the API by Friday, 
        Lisa to work with John on database schema by Wednesday, and Mike needs the 
        staging environment updated by Thursday. Let's reconvene next Monday to review 
        our progress. Meeting adjourned."""
