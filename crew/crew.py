import os
from crewai import Crew, Task
from agents.transcriber_agent import TranscriberAgent
from agents.summarizer_agent import SummarizerAgent
from agents.extractor_agent import ExtractorAgent
from agents.followup_agent import FollowupAgent
from tasks.task import MeetingTasks

class MeetingSummarizerCrew:
    """Main crew class that orchestrates the meeting summarization process"""
    
    def __init__(self):
        # Initialize agent instances
        self.transcriber_agent = TranscriberAgent()
        self.summarizer_agent = SummarizerAgent()
        self.extractor_agent = ExtractorAgent()
        self.followup_agent = FollowupAgent()
        
        # Initialize tasks
        self.meeting_tasks = MeetingTasks()
        
        # Create agents
        self.transcriber = self.transcriber_agent.create_agent()
        self.summarizer = self.summarizer_agent.create_agent()
        self.extractor = self.extractor_agent.create_agent()
        self.followup = self.followup_agent.create_agent()
        
    def run_crew(self, audio_file_path):
        """
        Execute the complete meeting summarization workflow
        
        Args:
            audio_file_path (str): Path to the meeting audio file
            
        Returns:
            dict: Complete results including transcript, summary, action items, and follow-up
        """
        try:
            print("🎯 Starting Meeting Summarizer & Action Tracker...")
            print("=" * 60)
            
            # Step 1: Transcribe audio
            print("\n📝 Step 1: Transcribing audio...")
            transcript = self.transcriber_agent.transcribe_audio(audio_file_path)
            print("✅ Transcription completed")
            
            # Step 2: Create summary
            print("\n📋 Step 2: Generating meeting summary...")
            summary = self.summarizer_agent.summarize_meeting(transcript)
            print("✅ Summary generated")
            
            # Step 3: Extract action items
            print("\n🎯 Step 3: Extracting action items...")
            action_items = self.extractor_agent.extract_action_items(transcript)
            print("✅ Action items extracted")
            
            # Step 4: Create follow-up message
            print("\n📧 Step 4: Creating follow-up message...")
            followup_message = self.followup_agent.create_followup_message(summary, action_items)
            print("✅ Follow-up message created")
            
            # Compile results
            results = {
                "transcript": transcript,
                "summary": summary,
                "action_items": action_items,
                "followup_message": followup_message
            }
            
            print("\n🎉 Meeting analysis completed successfully!")
            print("=" * 60)
            
            return results
            
        except Exception as e:
            print(f"❌ Error during crew execution: {str(e)}")
            raise e
    
    def create_crew_with_tasks(self, audio_file_path):
        """
        Create a CrewAI crew with defined tasks (alternative approach)
        
        Args:
            audio_file_path (str): Path to the meeting audio file
            
        Returns:
            Crew: Configured CrewAI crew instance
        """
        # Create tasks
        transcription_task = Task(
            description=f"Transcribe the audio file located at {audio_file_path} into clear, readable text",
            agent=self.transcriber,
            expected_output="Complete transcript of the meeting as plain text"
        )
        
        summarization_task = Task(
            description="Create a comprehensive summary of the meeting transcript in markdown format",
            agent=self.summarizer,
            expected_output="Well-structured meeting summary with key points, decisions, and next steps"
        )
        
        extraction_task = Task(
            description="Extract all action items, tasks, and commitments from the meeting transcript",
            agent=self.extractor,
            expected_output="JSON list of action items with task, owner, deadline, and priority"
        )
        
        followup_task = Task(
            description="Create a professional follow-up email based on the meeting summary and action items",
            agent=self.followup,
            expected_output="Professional follow-up email ready to be sent to meeting participants"
        )
        
        # Create and return crew
        crew = Crew(
            agents=[self.transcriber, self.summarizer, self.extractor, self.followup],
            tasks=[transcription_task, summarization_task, extraction_task, followup_task],
            verbose=True
        )
        
        return crew
    
    def display_results(self, results):
        """
        Display the results in a formatted way
        
        Args:
            results (dict): Results from the crew execution
        """
        print("\n" + "=" * 80)
        print("📋 MEETING ANALYSIS RESULTS")
        print("=" * 80)
        
        print("\n📝 TRANSCRIPT:")
        print("-" * 40)
        print(results["transcript"])
        
        print("\n📋 SUMMARY:")
        print("-" * 40)
        print(results["summary"])
        
        print("\n🎯 ACTION ITEMS:")
        print("-" * 40)
        if results["action_items"]:
            for i, item in enumerate(results["action_items"], 1):
                print(f"{i}. {item.get('task', 'No task specified')}")
                print(f"   Owner: {item.get('owner', 'Not assigned')}")
                print(f"   Deadline: {item.get('deadline', 'No deadline')}")
                print(f"   Priority: {item.get('priority', 'Medium')}")
                if item.get('context'):
                    print(f"   Context: {item.get('context')}")
                print()
        else:
            print("No action items found.")
        
        print("\n📧 FOLLOW-UP MESSAGE:")
        print("-" * 40)
        print(results["followup_message"])
        
        print("\n" + "=" * 80)
