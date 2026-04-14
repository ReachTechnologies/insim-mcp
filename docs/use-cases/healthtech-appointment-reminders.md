# "15% of our patients don't show up. That's 6 empty chairs a week."

> **Persona**: Dr. Karim, runs a dental clinic with 3 practitioners — Marseille, France
> **Tool**: insim-mcp (MCP server + Claude Code)
> **Setup time**: 30 minutes
> **ROI estimate**: No-show rate drops from 15% to 4%, recovering ~€2,400/month in lost revenue

## The problem

Dr. Karim manages a dental clinic with 3 practitioners and 40 appointments per day. Their no-show rate is 15% — roughly 6 patients per day who simply don't turn up. That's 6 empty 30-minute slots that could have gone to someone on the 2-week waiting list.

The receptionist calls patients the day before to remind them. But with 40 calls to make between handling walk-ins, insurance paperwork, and phone bookings, she gets through maybe 25. The ones she misses are disproportionately the ones who forget. Email reminders go unread. The clinic tried a dedicated reminder SaaS, but at €300/month it felt expensive for what it did, and patients couldn't reply to reschedule — they had to call back during office hours.

What Dr. Karim wants is simple: remind every patient by SMS from the clinic's real number, and let them reply to confirm or reschedule without calling.

## The solution with inSIM

1. **Import** — Patients are added to inSIM contacts with their appointment date and time stored as tags. The agent can also import from a CSV exported from the clinic's scheduling software.
2. **48h reminder** — Two days before the appointment, the agent sends a friendly SMS with date, time, and practitioner name. The patient can reply "OK" to confirm or "reschedule" to request a new slot.
3. **2h reminder** — Two hours before, a final short reminder. If the patient hasn't confirmed, the message is slightly more direct.
4. **Reschedule handling** — When a patient replies asking to reschedule, the agent tags them for the receptionist and sends an acknowledgment. Complex rescheduling goes to a human; simple confirmations are handled automatically.

## Implementation

### Key MCP tools used

```
add_contacts(contacts=[...])                      -> Import patients
search_contacts(query="appointment-2026-04-16")    -> Find patients with appointments in 48h
send_sms(phone_number="+33...", message="...")      -> Send reminders
sms_conversation(phone_number="+33...")             -> Read patient replies
manage_contact_tags(id="...", action="add", tags=["confirmed"])
                                                   -> Track confirmation status
list_contacts(search="reschedule-requested")        -> Morning queue for receptionist
```

### Example agent interaction

**Trigger**: It's Monday morning. The agent checks for Wednesday appointments (48h ahead).

**Agent action**:
1. Searches `search_contacts(query="appointment-2026-04-16")` — finds 38 patients
2. For each patient, sends a reminder via `send_sms`. Example for Mme Dupont, +33600000003:
   > "Hello Mme Dupont, reminder: you have a dental appointment on Wednesday April 16 at 10:30am with Dr. Karim at Cabinet Sourire. Reply OK to confirm, or RESCHEDULE if you need a different time. See you soon!"
3. Tags each contact: `reminder-48h-sent`

**Patient reply** (received 2 hours later):
> "OK thanks!"

**Agent action**:
1. Reads conversation via `sms_conversation(phone_number="+33600000003")`
2. Classifies: confirmation
3. Tags contact: `confirmed`, removes `reminder-48h-sent`

**Another patient**, M. Benali (+33600000004), replies:
> "I can't make Wednesday, can I come Thursday instead?"

**Agent action**:
1. Reads conversation, classifies: reschedule request
2. Sends acknowledgment via `send_sms`:
   > "No problem, M. Benali. I'll pass your request to our receptionist who will find you a Thursday slot. You'll receive a confirmation SMS shortly."
3. Tags contact: `reschedule-requested`, removes `reminder-48h-sent`

**2 hours before appointment** — Wednesday 8:30am, the agent sends final reminders to unconfirmed patients:

```
send_sms(
    phone_number="+33600000005",
    message="Quick reminder: your appointment with Dr. Karim is today at 10:30am. See you soon at Cabinet Sourire, 12 rue de la Paix."
)
```

## Results

| Metric | Before | After |
|--------|--------|-------|
| No-show rate | 15% (6/day) | 4% (1-2/day) |
| Revenue recovered | €0 | ~€2,400/month |
| Receptionist time on reminder calls | 2 hours/day | 15 min (reschedules only) |
| Patient confirmation rate | 40% (phone) | 82% (SMS) |

The key: patients don't ignore SMS the way they ignore calls from unknown numbers. A text from the clinic's real number, with a simple "reply OK" mechanic, turns passive patients into confirmed appointments. The 2-hour final nudge catches the rest.

## Related study cases

- [E-commerce: AI night support via MCP](./ecommerce-night-support.md) — Parent study case (P2)
- [SaaS: SMS onboarding for new users](./saas-sms-onboarding.md) — Milestone-based SMS triggers
- [Debt collection: Invoice follow-up agent](./debt-collection-followup.md) — Graduated SMS sequences
