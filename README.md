# Meeting Summarizer & Action Tracker

A powerful CrewAI-based system that automatically processes meeting recordings to generate transcripts, summaries, action items, and follow-up communications. This project leverages multiple AI agents working together to transform your meeting audio into actionable insights.

## 🎯 Overview

This project uses a multi-agent CrewAI system to:

- **Transcribe** meeting audio using OpenAI Whisper API
- **Summarize** discussions with GPT-4o
- **Extract** action items with owners and deadlines
- **Generate** professional follow-up messages

Perfect for teams that want to automate meeting documentation and ensure nothing falls through the cracks.

## 🏗️ Architecture

The system consists of four specialized AI agents:

1. **Transcriber Agent** - Converts audio to text using OpenAI Whisper
2. **Summarizer Agent** - Creates structured meeting summaries
3. **Extractor Agent** - Identifies and organizes action items
4. **Follow-up Agent** - Generates professional follow-up communications

This project follows the [CrewAI Marketplace Template](https://github.com/crewAIInc/marketplace-crew-template) structure and is compatible with the [CrewAI Marketplace](https://marketplace.crewai.com/).

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (or use mock mode for testing)

### Installation

1. **Clone or download this project**
```bash
git clone <repository-url>
cd meeting-summarizer
