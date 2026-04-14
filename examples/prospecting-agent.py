#!/usr/bin/env python3
"""Autonomous prospecting agent example.

This script demonstrates how to build a prospecting agent that uses
insim-mcp tools via the Claude API. It contacts candidates, monitors
responses, and qualifies leads.

Prerequisites:
    pip install anthropic insim-mcp
    export ANTHROPIC_API_KEY="your-api-key"
    export INSIM_LOGIN="your@email.com"
    export INSIM_ACCESS_KEY="your-access-key"

See the full study case:
    docs/use-cases/autonomous-prospecting-agent.md
"""

# This is a conceptual example showing the agent workflow.
# In production, you would use the Claude API with MCP tool_use
# to let the agent autonomously call insim-mcp tools.

OUTREACH_PROMPT = """
You are a recruitment assistant. Your job is to:

1. Check for new incoming SMS responses using list_sms(direction="inbound")
2. For each response, read the conversation with sms_conversation()
3. Classify the response:
   - INTERESTED: tag "interested", ask qualifying questions
   - NOT_INTERESTED: tag "not-interested", send thank-you
   - QUESTION: answer the question, continue conversation
4. For interested candidates, send qualifying questions via send_sms()
5. Generate a daily pipeline report

Use the insim MCP tools to execute each step.
"""

QUALIFYING_QUESTIONS = (
    "Great to hear! A few quick questions:\n"
    "1) Are you currently employed or in notice period?\n"
    "2) What's your availability for a 30-min call this week?\n"
    "3) Any salary expectations?"
)

if __name__ == "__main__":
    print("This is a conceptual example.")
    print("To run a real prospecting agent:")
    print("1. Configure insim-mcp in your Claude Code .mcp.json")
    print("2. Use the prompt from the study case")
    print("3. Or integrate with the Claude API using tool_use")
    print()
    print(f"Outreach prompt:\n{OUTREACH_PROMPT}")
