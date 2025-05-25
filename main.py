#!/usr/bin/env python3
"""
Meeting Summarizer & Action Tracker
A CrewAI-based system for processing meeting recordings into actionable insights.

This is the main entry point for the application.
"""

import os
import sys
import json
from datetime import datetime
from crew.crew import MeetingSummarizerCrew
from dotenv import load_dotenv

def setup_environment():
    """Load environment variables and validate configuration"""
    load_dotenv()
    
    # Check if OpenAI API key is set (unless in mock mode)
    mock_mode = os.getenv("MOCK_MODE", "false").lower() == "true"
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not mock_mode and not api_key:
        print("⚠️  Warning: OPENAI_API_KEY not found in environment variables.")
        print("   Set MOCK_MODE=true in your .env file to use mock responses for testing.")
        print("   Or add your OpenAI API key to the .env file.")
        return False
    
    if mock_mode:
        print("🧪 Running in MOCK MODE - using simulated responses")
    else:
        print("🔑 Using OpenAI API for real processing")
    
    return True

def validate_audio_file(file_path):
    """Validate that the audio file exists and is accessible"""
    if not os.path.exists(file_path):
        print(f"❌ Error: Audio file not found at {file_path}")
        return False
    
    # Check file extension
    valid_extensions = ['.mp3', '.wav', '.m4a', '.flac']
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext not in valid_extensions:
        print(f"⚠️  Warning: File extension {file_ext} may not be supported.")
        print(f"   Supported formats: {', '.join(valid_extensions)}")
    
    return True

def save_results_to_files(results, output_dir="output"):
    """Save results to individual files"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        # Save transcript
        with open(f"{output_dir}/transcript_{timestamp}.txt", "w", encoding="utf-8") as f:
            f.write(results["transcript"])
        
        # Save summary
        with open(f"{output_dir}/summary_{timestamp}.md", "w", encoding="utf-8") as f:
            f.write(results["summary"])
        
        # Save action items
        with open(f"{output_dir}/action_items_{timestamp}.json", "w", encoding="utf-8") as f:
            json.dump(results["action_items"], f, indent=2, ensure_ascii=False)
        
        # Save follow-up message
        with open(f"{output_dir}/followup_{timestamp}.txt", "w", encoding="utf-8") as f:
            f.write(results["followup_message"])
        
        print(f"\n💾 Results saved to {output_dir}/ directory with timestamp {timestamp}")
        
    except Exception as e:
        print(f"⚠️  Warning: Could not save results to files: {str(e)}")

def main():
    """Main application entry point"""
    print("🎯 Meeting Summarizer & Action Tracker")
    print("=" * 60)
    print("A CrewAI-powered system for meeting analysis and action item tracking")
    print()
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Determine audio file path
    if len(sys.argv) > 1:
        audio_file_path = sys.argv[1]
    else:
        # Use default sample file
        audio_file_path = "sample_data/meeting_sample.mp3"
        print(f"No audio file specified, using default: {audio_file_path}")
    
    # Validate audio file (in mock mode, this will fail but that's OK)
    mock_mode = os.getenv("MOCK_MODE", "false").lower() == "true"
    if not mock_mode and not validate_audio_file(audio_file_path):
        print("\n💡 To test without an audio file, set MOCK_MODE=true in your .env file")
        sys.exit(1)
    
    try:
        # Initialize and run the crew
        print(f"\n🚀 Processing audio file: {audio_file_path}")
        print("-" * 60)
        
        crew = MeetingSummarizerCrew()
        results = crew.run_crew(audio_file_path)
        
        # Display results
        crew.display_results(results)
        
        # Save results to files (optional)
        save_output = os.getenv("SAVE_OUTPUT", "false").lower() == "true"
        if save_output:
            save_results_to_files(results)
        
        print("\n✅ Meeting analysis completed successfully!")
        print("\n💡 Next steps:")
        print("   - Review the action items and assign them to team members")
        print("   - Send the follow-up message to meeting participants")
        print("   - Schedule follow-up meetings as needed")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Process interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("   - Check your OPENAI_API_KEY in the .env file")
        print("   - Verify the audio file path and format")
        print("   - Try running with MOCK_MODE=true for testing")
        sys.exit(1)

if __name__ == "__main__":
    main()
