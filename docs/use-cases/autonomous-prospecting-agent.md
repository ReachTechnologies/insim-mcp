# "My agent contacts 50 candidates a day. I used to do 8."

> **Persona**: Karim, freelance AI developer building agents for SMBs — Remote, France
> **Tool**: insim-mcp (MCP server + Python + Claude API)
> **Setup time**: 2 hours
> **ROI estimate**: 6x more candidates contacted, qualified pipeline generated with 0 human time

## The problem

Karim builds custom AI agents for small businesses. His latest client is Talent Express, a recruitment agency with 3 consultants. Their daily routine: search LinkedIn for candidates, copy phone numbers into a spreadsheet, call each one, take notes, call again tomorrow for the ones who didn't answer.

Each consultant contacts 8-10 candidates per day. They want to reach 50. But hiring more consultants isn't in the budget — they're a 3-person shop competing against agencies 10 times their size.

The bottleneck isn't finding candidates. Job boards and LinkedIn provide hundreds of matches. The bottleneck is the first contact: reaching out, getting a response, and qualifying interest. It's repetitive, time-consuming, and most of the effort goes to candidates who aren't interested.

Karim's pitch: "What if an AI agent handled the first contact via SMS, and your consultants only talked to people who already said yes?"

## The solution with inSIM

1. **Import** — Karim's agent imports candidates from a CSV (sourced from LinkedIn or job boards) into inSIM contacts, tagged by role and campaign.
2. **Outreach** — The agent sends personalized SMS to each candidate from the agency's real mobile number. Not a template blast — each message references the candidate's role and the specific opportunity.
3. **Monitor** — The agent checks for responses every 30 minutes. It reads each reply and classifies it: interested, not interested, question, wrong number.
4. **Qualify** — For interested candidates, the agent asks 2-3 qualifying questions via SMS. For questions, it provides answers. For "not interested," it thanks them and tags accordingly.
5. **Pipeline** — Every morning, the consultants get a qualified pipeline: candidates who responded positively, with conversation history and qualification notes.

## Implementation

### Prerequisites

- inSIM app installed on the agency's phone
- inSIM account with API access
- insim-mcp configured in your development environment
- Python 3.10+ with `anthropic` SDK

### Step 1: Configure insim-mcp

```json
{
  "mcpServers": {
    "insim": {
      "command": "insim-mcp",
      "env": {
        "INSIM_LOGIN": "recrutement@talentexpress.fr",
        "INSIM_ACCESS_KEY": "your-access-key"
      }
    }
  }
}
```

### Step 2: Import candidates

Using the CLI (or the agent can use MCP `add_contacts` tool):

```bash
# Import from CSV with tags
insim --json contacts add "+33612000001" --firstname "Alice" --lastname "Moreau"
insim contacts tags-add "CONTACT_ID" "candidate" "dev-senior" "campaign-april"

insim --json contacts add "+33612000002" --firstname "Thomas" --lastname "Petit"
insim contacts tags-add "CONTACT_ID" "candidate" "dev-senior" "campaign-april"
```

Or in bulk via MCP tool:

```python
# The agent uses add_contacts to import in bulk
add_contacts(contacts=[
    {"phone_number": "+33612000001", "firstname": "Alice", "lastname": "Moreau"},
    {"phone_number": "+33612000002", "firstname": "Thomas", "lastname": "Petit"},
])
```

### Step 3: Personalized outreach

The agent uses `send_sms` for each candidate with a personalized message:

```
send_sms(
    phone_number="+33612000001",
    message="Hi Alice, I'm reaching out from Talent Express. We have a Senior Developer position at a growing fintech in Lyon — remote-friendly, €55-65K range. Would you be open to a quick chat this week? — Marie, Talent Express"
)
```

Key: each message mentions the candidate's name, the specific role, and a real detail (location, salary range). This is not a template blast.

### Step 4: Monitor responses

Every 30 minutes, the agent checks for new incoming SMS:

```
list_sms(direction="inbound", limit=50)
```

For each response, it reads the conversation:

```
sms_conversation(phone_number="+33612000001", limit=10)
```

Then classifies the response:
- **"Yes, I'm interested"** → Tag: `interested`, send qualifying questions
- **"Not looking right now"** → Tag: `not-interested`, thank them
- **"What's the company?"** → Answer the question, continue conversation
- **"Wrong number"** → Tag: `wrong-number`, remove from campaign

### Step 5: Qualify interested candidates

For interested candidates, the agent asks qualifying questions:

```
send_sms(
    phone_number="+33612000001",
    message="Great to hear, Alice! A few quick questions: 1) Are you currently employed or in notice period? 2) What's your availability for a 30-min call this week? 3) Any salary expectations beyond the range mentioned?"
)
```

When the candidate replies, the agent:
1. Reads the response via `sms_conversation`
2. Extracts the answers
3. Tags the contact: `qualified`, `available-immediately` or `notice-period`
4. Adds qualification notes via `qualify_call` (repurposed for candidate notes)

### Step 6: Morning pipeline report

The agent generates a daily report:

```
# Find all qualified candidates
list_contacts(search="qualified")

# For each, get the conversation
sms_conversation(phone_number="...")

# Get overall stats
stats_overview()
qualification_stats()
```

Output for the consultants:

```
=== Daily Pipeline Report — April 14, 2026 ===

New qualified candidates: 7
Conversations in progress: 12
Not interested: 18
No response yet: 13

TOP PRIORITIES:
1. Alice Moreau (+33612000001) — Interested, available immediately
   "Yes I'm interested! I can do a call Wednesday afternoon."
   Tags: qualified, available-immediately, dev-senior

2. Thomas Petit (+33612000002) — Interested, notice period
   "Sounds great, but I'm in a 3-month notice. Is that OK?"
   Tags: qualified, notice-period, dev-senior

3. Sarah Lemaire (+33612000003) — Questions answered, awaiting reply
   Asked about remote policy. Replied with details 2h ago.
```

## Results

| Metric | Manual (3 consultants) | With AI agent |
|--------|----------------------|---------------|
| Candidates contacted/day | 24-30 | 50 |
| First response time | Next day (call back) | 15 minutes (SMS) |
| Response rate | 30% (phone) | 35% (SMS) |
| Qualified pipeline/week | 8-10 | 25-30 |
| Consultant time on outreach | 60% of day | 10% (review pipeline only) |
| Cost per outreach | ~€2 (time) | €0 (mobile plan + AI) |

The consultants now spend their time where it matters: talking to people who already said yes. The AI handles the tedious part — the first contact, the follow-ups, the "not interested" responses.

## Variations

- [Debt collection: Invoice follow-up agent](./debt-collection-followup.md)
- [Competitive intelligence: SMS alerts](./competitive-intelligence-alerts.md)

## Related study cases

- [E-commerce: AI night support via MCP](./ecommerce-night-support.md) — MCP for automated customer responses
- [Real estate agent: Open house follow-up](../../../insim-cli/docs/use-cases/real-estate-open-house.md) — CLI-based campaign management
