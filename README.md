
# Meeting Summarizer & Action Tracker

A powerful CrewAI-based system that automatically processes meeting recordings to generate transcripts, summaries, action items, and follow-up communications using a multi-agent AI approach.

## What it does

This CrewAI crew transforms your meeting audio into actionable insights through four specialized AI agents:

- **🎤 Transcriber Agent** - Converts audio to text using OpenAI Whisper API
- **📝 Summarizer Agent** - Creates structured meeting summaries with GPT-4o  
- **🎯 Extractor Agent** - Identifies and organizes action items with owners and deadlines
- **📧 Follow-up Agent** - Generates professional follow-up communications

Perfect for teams that want to automate meeting documentation and ensure nothing falls through the cracks.

## Running the Crew

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (or use mock mode for testing)

### Installation

This crew is ready to run in Replit! Just click the **Run** button to start.

For local development:

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Add your OpenAI API key to .env
# OPENAI_API_KEY=your_api_key_here
```

### Usage

**In Replit:**
1. Set your OpenAI API key in the Secrets tool or `.env` file
2. Click the **Run** button
3. The crew will process the sample audio file

**Local/Custom usage:**
```bash
# Process a specific audio file
python main.py path/to/your/meeting.mp3

# Or run with default sample
python main.py
```

**Mock Mode for Testing:**
Set `MOCK_MODE=true` in your `.env` file to test without API calls.

### Configuration

Environment variables in `.env`:
- `OPENAI_API_KEY` - Your OpenAI API key
- `MOCK_MODE` - Set to "true" for testing without API calls
- `SAVE_OUTPUT` - Set to "true" to save results to files

## Crew Output

The crew generates:

1. **📄 Complete Transcript** - Clear, readable text from audio
2. **📋 Meeting Summary** - Structured markdown with key points and decisions
3. **✅ Action Items** - JSON list with tasks, owners, deadlines, and priorities
4. **📧 Follow-up Message** - Professional email ready to send

Example output structure:
```json
{
  "transcript": "Complete meeting transcript...",
  "summary": "# Meeting Summary\n\n## Key Points...",
  "action_items": [
    {
      "task": "Review quarterly budget",
      "owner": "John Smith",
      "deadline": "Next Friday",
      "priority": "High"
    }
  ],
  "followup_message": "Subject: Follow-up from Today's Meeting..."
}
```

## How it Works

The crew uses a sequential workflow:

1. **Audio Processing** - Transcriber agent converts meeting audio to text
2. **Content Analysis** - Summarizer agent creates structured meeting summary
3. **Action Extraction** - Extractor agent identifies tasks and commitments
4. **Communication** - Follow-up agent generates professional follow-up message

Each agent is powered by OpenAI's latest models and designed with specific roles, goals, and backstories for optimal performance.

## Customization

### Adding New Agents
Extend the crew by adding new agents in the `agents/` directory following the existing pattern.

### Modifying Output Format
Update agent prompts and expected outputs in the respective agent files.

### Different Audio Formats
The transcriber supports various audio formats: MP3, WAV, M4A, FLAC.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues or questions:
- Check the troubleshooting section in the code comments
- Ensure your OpenAI API key is properly set
- Try mock mode for testing: `MOCK_MODE=true`

---

*This crew follows the [CrewAI Marketplace Template](https://github.com/crewAIInc/marketplace-crew-template) structure and is compatible with the [CrewAI Marketplace](https://marketplace.crewai.com/).*
