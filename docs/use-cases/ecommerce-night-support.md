# "Our customers text us at 11pm. We reply at 9am. By then, they've bought elsewhere."

> **Persona**: Marc, CTO of an online furniture store — Paris, France — 15 employees
> **Tool**: insim-mcp (MCP server + Claude Code)
> **Setup time**: 30 minutes
> **ROI estimate**: 60% of night inquiries resolved automatically, +23% customer satisfaction

## The problem

Marc runs the tech at Maison & Style, an online furniture store doing €2M/year. Their customers text the company phone with delivery questions, return requests, and product inquiries — often in the evening, after work.

Every morning at 9am, the support team opens inSIM and finds 12-15 unread SMS from the night before. By then, a customer who texted at 10pm asking "Is my couch being delivered tomorrow?" has already called the delivery company directly, left a 1-star review, or bought from a competitor.

Marc tried setting up auto-replies, but generic "We'll get back to you during business hours" messages feel robotic and don't actually help. He needs something that understands the question and gives a real answer.

## The solution with inSIM

1. **Setup** — Marc configures insim-mcp in Claude Code. The AI agent can read SMS conversations, search contacts, and send replies through the company's real mobile number.
2. **Triage** — When invoked, the agent reads all unread incoming SMS, looks up each contact, and classifies each message: delivery tracking (urgent), product question (normal), return request (flag for human), complaint (flag for human).
3. **Auto-reply** — For simple cases (delivery ETA, product availability, store hours), the agent drafts and sends a reply immediately. For complex cases, it tags the contact and drafts a response for human review.
4. **Morning briefing** — At 9am, the support team gets a summary: "8 SMS handled overnight, 4 need your attention" with the flagged conversations ready to go.

## Implementation

### Prerequisites

- inSIM app installed on the company phone
- inSIM account with API access
- Claude Code with insim-mcp configured

### Step 1: Configure insim-mcp in Claude Code

Add to your `.mcp.json`:

```json
{
  "mcpServers": {
    "insim": {
      "command": "insim-mcp",
      "env": {
        "INSIM_LOGIN": "support@maison-style.fr",
        "INSIM_ACCESS_KEY": "your-access-key"
      }
    }
  }
}
```

### Step 2: Create a night support prompt

In Claude Code, you can now ask the agent to handle support:

```
Read all incoming SMS from the last 12 hours. For each one:

1. Look up the contact in inSIM
2. Read the full conversation history
3. Classify the message:
   - DELIVERY: questions about shipping, tracking, ETA
   - PRODUCT: questions about products, availability, pricing
   - RETURN: return or exchange requests
   - COMPLAINT: negative feedback or issues
   - OTHER: anything else

4. For DELIVERY and PRODUCT messages:
   - Draft a helpful, friendly reply
   - Send it via inSIM
   - Tag the contact with "auto-replied"

5. For RETURN, COMPLAINT, and OTHER:
   - Tag the contact with "needs-human"
   - Do NOT send a reply

6. Give me a summary of what you handled.
```

### Step 3: What the agent does (MCP tools used)

The agent uses these insim-mcp tools automatically:

```
list_sms(direction="inbound", limit=50)     → Get recent incoming SMS
search_contacts(query="...")                  → Find the sender
sms_conversation(phone_number="+33...")       → Read full thread
send_sms(phone_number="+33...", message="..") → Reply to customer
manage_contact_tags(id="...", action="add", tags=["auto-replied"])
                                              → Tag for tracking
```

### Step 4: Example agent interaction

**Incoming SMS** (received at 10:47pm):
> "Hi, I ordered a dining table last week (order #4521). Is it being delivered tomorrow as planned?"

**Agent action**:
1. Finds contact: Claire Bernard, +33612000003
2. Reads conversation: 3 prior messages about order #4521
3. Classifies: DELIVERY (routine inquiry)
4. Sends reply via `send_sms`:
   > "Hi Claire! Your dining table (order #4521) is confirmed for delivery tomorrow between 2pm and 5pm. The delivery team will call you 30 minutes before arrival. Let me know if you need to reschedule!"
5. Tags contact: `auto-replied`, `delivery-inquiry`

**Incoming SMS** (received at 11:22pm):
> "The chair I received is damaged. I want a refund or replacement."

**Agent action**:
1. Finds contact: Jean Martin, +33612000002
2. Classifies: COMPLAINT (needs human)
3. Does NOT reply
4. Tags contact: `needs-human`, `complaint`

### Step 5: Morning briefing

At 9am, the support team runs:

```
Show me all contacts tagged "needs-human" from last night.
For each one, show the conversation and the issue classification.
```

The agent uses:

```
list_contacts(search="needs-human")  → Find flagged contacts
sms_conversation(phone_number="...")  → Show full context
```

## Results

| Metric | Before | After |
|--------|--------|-------|
| Average response time (night SMS) | 8-12 hours | 15 minutes (auto) |
| SMS handled without human | 0% | 60% |
| Customer satisfaction (NPS) | 32 | 55 (+23 points) |
| Support team morning workload | 15 SMS to process | 4-6 flagged SMS |
| Lost sales from slow response | ~€800/month | ~€200/month |

The key insight: customers don't need a human at 11pm. They need a real answer from a real number. The AI handles 60% of cases instantly, and flags the rest for morning.

## Variations

- [SaaS CTO: SMS onboarding for new users](./saas-sms-onboarding.md) *(coming soon)*
- [Healthtech CTO: Patient appointment reminders](./healthtech-appointment-reminders.md) *(coming soon)*
- [Logistics CTO: Delivery notifications](./logistics-delivery-notifications.md) *(coming soon)*

## Related study cases

- [Real estate agent: Open house SMS follow-up](../../../insim-cli/docs/use-cases/real-estate-open-house.md) — CLI-based campaign management
- [Autonomous prospecting agent](./autonomous-prospecting-agent.md) — Full autonomous agent with MCP
