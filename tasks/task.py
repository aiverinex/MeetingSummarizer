from crewai import Task

class MeetingTasks:
    """Task definitions for the meeting summarization crew"""
    
    def __init__(self):
        pass
    
    def transcription_task(self, agent, audio_file_path):
        """Create transcription task"""
        return Task(
            description=f"""
            Transcribe the audio file located at {audio_file_path} into clear, readable text.
            
            Requirements:
            - Extract all spoken words accurately
            - Maintain proper formatting and punctuation
            - Identify speakers when possible
            - Handle various audio qualities and accents
            - Provide a clean, professional transcript
            
            The output should be the complete meeting transcript as plain text.
            """,
            agent=agent,
            expected_output="Complete transcript of the meeting as plain text with proper formatting"
        )
    
    def summarization_task(self, agent, transcript):
        """Create summarization task"""
        return Task(
            description=f"""
            Create a comprehensive summary of the following meeting transcript:
            
            {transcript}
            
            Requirements:
            - Structure the summary in markdown format
            - Include meeting overview with attendees
            - Highlight key discussion points
            - Document decisions made during the meeting
            - Outline next steps and follow-up items
            - Keep the summary concise but comprehensive
            - Use professional language and clear formatting
            
            The output should be a well-structured meeting summary in markdown format.
            """,
            agent=agent,
            expected_output="Well-structured meeting summary in markdown format with key points, decisions, and next steps"
        )
    
    def extraction_task(self, agent, transcript):
        """Create action item extraction task"""
        return Task(
            description=f"""
            Extract all action items, tasks, and commitments from the following meeting transcript:
            
            {transcript}
            
            Requirements:
            - Identify specific tasks and deliverables
            - Determine task ownership (who is responsible)
            - Extract deadlines and timeframes when mentioned
            - Assess priority levels based on context
            - Include relevant context and dependencies
            - Format output as structured JSON
            
            For each action item, provide:
            - task: Clear description of what needs to be done
            - owner: Person responsible for the task
            - deadline: Deadline or timeframe (use "Not specified" if not mentioned)
            - priority: Estimated priority level (High/Medium/Low)
            - context: Additional relevant information or dependencies
            
            The output should be a JSON array of action items.
            """,
            agent=agent,
            expected_output="JSON array of action items with task, owner, deadline, priority, and context fields"
        )
    
    def followup_task(self, agent, summary, action_items):
        """Create follow-up message task"""
        return Task(
            description=f"""
            Create a professional follow-up email based on the meeting summary and action items.
            
            Meeting Summary:
            {summary}
            
            Action Items:
            {action_items}
            
            Requirements:
            - Write in professional email format
            - Include appropriate subject line
            - Provide brief meeting reference and highlights
            - Format action items clearly with owners and deadlines
            - Include professional greeting and closing
            - Ensure the message is actionable and clear
            - Make it ready to send to meeting participants
            
            The output should be a complete, professional follow-up email.
            """,
            agent=agent,
            expected_output="Professional follow-up email ready to be sent to meeting participants"
        )
    
    def create_sequential_tasks(self, agents, audio_file_path):
        """
        Create a sequence of tasks that depend on each other
        
        Args:
            agents (dict): Dictionary of agent instances
            audio_file_path (str): Path to the audio file
            
        Returns:
            list: List of sequential tasks
        """
        tasks = []
        
        # Task 1: Transcription
        transcription_task = self.transcription_task(agents['transcriber'], audio_file_path)
        tasks.append(transcription_task)
        
        # Task 2: Summarization (depends on transcription)
        summarization_task = Task(
            description="""
            Create a comprehensive summary of the meeting transcript from the previous task.
            Use the transcript output to generate a well-structured summary in markdown format.
            """,
            agent=agents['summarizer'],
            expected_output="Well-structured meeting summary in markdown format"
        )
        tasks.append(summarization_task)
        
        # Task 3: Action item extraction (depends on transcription)
        extraction_task = Task(
            description="""
            Extract all action items from the meeting transcript generated in the first task.
            Analyze the transcript to identify tasks, owners, deadlines, and priorities.
            """,
            agent=agents['extractor'],
            expected_output="JSON array of action items with complete details"
        )
        tasks.append(extraction_task)
        
        # Task 4: Follow-up message (depends on summary and action items)
        followup_task = Task(
            description="""
            Create a professional follow-up email using the summary and action items from previous tasks.
            Combine the information to create a comprehensive follow-up communication.
            """,
            agent=agents['followup'],
            expected_output="Professional follow-up email ready for distribution"
        )
        tasks.append(followup_task)
        
        return tasks
