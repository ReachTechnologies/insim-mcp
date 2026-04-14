# "We have 45K in overdue invoices. Nobody wants to make those calls."

> **Persona**: Marie, office manager at an architecture firm — Bordeaux, France — 6 employees
> **Tool**: insim-mcp (MCP server + Claude Code)
> **Setup time**: 45 minutes
> **ROI estimate**: 70% of overdue invoices resolved within 30 days, 3 hours/week saved on follow-up

## The problem

Marie handles administration at Atelier Duval, a small architecture firm. The architects are brilliant at design, terrible at chasing payments. Right now, there's EUR45K in overdue invoices spread across 12 clients. Some are 2 weeks late. Two are 90+ days. Nobody on the team wants to make the awkward phone call — so the invoices just sit there.

Marie sends reminder emails, but they get lost in inboxes. She's tried calling, but half the clients don't pick up, and the other half promise to pay "next week" and then don't. The firm's cash flow suffers. Last month they delayed paying their own suppliers because a EUR12K invoice was 60 days overdue from a client who "forgot."

What Marie needs is a system that follows up persistently but professionally — escalating the tone gradually from friendly reminder to formal notice — without anyone on the team having to make uncomfortable calls.

## The solution with inSIM

1. **Import** — Marie adds the 12 overdue clients as inSIM contacts, tagged by invoice number, amount, and days overdue. Each client gets a payment stage: `gentle`, `firm`, or `final-notice`.
2. **Graduated reminders** — The agent sends SMS reminders that escalate in tone based on how overdue the invoice is: gentle (1-14 days), firm (15-30 days), and final notice (30+ days). Each message references the specific invoice and amount.
3. **Response handling** — When clients reply (promise to pay, dispute, request payment plan), the agent classifies the response and either continues the sequence, tags for Marie's attention, or acknowledges a payment commitment.
4. **Weekly collections report** — Every Friday, Marie gets a summary: who paid, who promised, who's silent, who needs escalation.

## Implementation

### Key MCP tools used

```
add_contacts(contacts=[...])                       -> Import overdue clients
manage_contact_tags(id="...", action="add", tags=["invoice-2024-087", "overdue-30d", "stage-firm"])
                                                   -> Track invoice and escalation stage
send_sms(phone_number="+33...", message="...")      -> Send graduated reminders
sms_conversation(phone_number="+33...")             -> Read client responses
search_contacts(query="stage-gentle")               -> Find clients at each stage
create_template(name="reminder-gentle", content="...") -> Reusable reminder templates
send_template(template_id="...", phone_number="...") -> Send from template
```

### Example agent interaction

**Trigger**: Monday morning. Agent checks overdue invoices and sends appropriate reminders.

**Stage 1 — Gentle (8 days overdue)**: Client Mme Rousseau, +33600000020, owes EUR3,200 (invoice #2024-087).

```
send_sms(
    phone_number="+33600000020",
    message="Hello Mme Rousseau, this is Atelier Duval. A quick reminder that invoice #2024-087 (EUR3,200) was due on April 6. It may have slipped through — these things happen! Could you let us know when we can expect payment? Thanks! — Marie"
)
```
Tags: `reminder-1-sent`, `stage-gentle`

**Mme Rousseau replies** (same day):
> "Sorry Marie! I'll transfer it by Wednesday."

**Agent action**:
1. Reads via `sms_conversation(phone_number="+33600000020")`
2. Classifies: payment promise with date
3. Tags: `promised-2026-04-16`, removes `stage-gentle`
4. Sends acknowledgment:
   > "Perfect, thanks Mme Rousseau! I'll note Wednesday. Don't hesitate if you need our bank details again."

**Stage 2 — Firm (25 days overdue)**: Client M. Laurent, +33600000021, owes EUR8,500 (invoice #2024-072). No response to first reminder.

```
send_sms(
    phone_number="+33600000021",
    message="Hello M. Laurent, this is Atelier Duval. Invoice #2024-072 (EUR8,500) is now 25 days overdue. We haven't received payment or a response to our previous message. Could you please confirm a payment date at your earliest convenience? — Marie, Atelier Duval"
)
```
Tags: `reminder-2-sent`, `stage-firm`

**Stage 3 — Final notice (65 days overdue)**: Client SCI Montagne, +33600000022, owes EUR12,000 (invoice #2024-041). Two prior reminders, no response.

```
send_sms(
    phone_number="+33600000022",
    message="SCI Montagne — Invoice #2024-041 (EUR12,000) is now 65 days overdue. Despite two prior reminders, we have not received payment or a response. Please settle this within 7 days to avoid formal collection proceedings. Contact us at 05 56 00 00 00 to discuss. — Atelier Duval"
)
```
Tags: `final-notice-sent`, `stage-final`

**M. Laurent finally replies** (3 days after firm reminder):
> "We're having cash flow issues. Can we pay in 2 installments?"

**Agent action**:
1. Reads conversation, classifies: payment plan request (needs human decision)
2. Tags: `payment-plan-requested`, `needs-human`
3. Sends:
   > "Thank you for getting back to us, M. Laurent. I'll have Marie contact you to arrange a payment plan that works for both sides."

## Results

| Metric | Before | After |
|--------|--------|-------|
| Overdue invoices resolved within 30 days | 30% | 70% |
| Average days to payment (overdue) | 52 days | 18 days |
| Time spent on payment follow-up | 3 hours/week | 30 min/week (review only) |
| Bad debt write-offs per year | ~EUR8K | ~EUR2K |

The insight: most late payments aren't malicious — they're forgotten. A simple SMS reminder from the firm's real number resolves 50% of overdue invoices on the first message. The graduated escalation handles the rest without anyone on the team having an uncomfortable conversation. By the time Marie needs to get involved personally, it's only 2-3 truly difficult cases instead of 12.

## Related study cases

- [Autonomous prospecting agent](./autonomous-prospecting-agent.md) — Parent study case (P4), graduated outreach pattern
- [SaaS: SMS onboarding for new users](./saas-sms-onboarding.md) — Stage-based SMS sequences
- [Healthtech: Patient appointment reminders](./healthtech-appointment-reminders.md) — Confirmation handling pattern
