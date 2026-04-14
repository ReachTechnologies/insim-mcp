# "Customers call us 20 times a day asking where their package is."

> **Persona**: Fatima, operations manager at a regional delivery company — Toulouse, France — 25 employees
> **Tool**: insim-mcp (MCP server + Claude Code)
> **Setup time**: 1 hour
> **ROI estimate**: -75% inbound "where is my package" calls, +35 NPS points

## The problem

Fatima manages operations at LivrExpress, a regional delivery company handling 150 deliveries per day across southwest France. Their biggest operational drain isn't logistics — it's the phone. Every day, the dispatch team fields 20-25 calls from customers asking the same question: "Where is my package?"

Each call takes 3-5 minutes. The dispatcher has to look up the order, check the driver's route, estimate an ETA, and relay it to the customer. That's nearly 2 hours per day spent on calls that could be a single text message. Worse, when the phones are busy, customers who have real issues (damaged goods, wrong address, access codes) can't get through.

Fatima tried email notifications, but customers don't check email when they're waiting for a delivery. They check their phone. She needs proactive SMS updates that answer the question before the customer picks up the phone to call.

## The solution with inSIM

1. **Import** — Each morning, the agent imports the day's delivery manifest into inSIM contacts, tagged by route and estimated delivery window.
2. **Proactive updates** — The agent sends SMS at three points: morning (your delivery is scheduled today, estimated window), en route (your package is next, ~30 min away), and delivered (confirmation with driver notes).
3. **Inbound handling** — When customers text back with questions ("Can I change the address?", "What time exactly?"), the agent reads the conversation, checks the contact's delivery tags, and either answers or flags for dispatch.
4. **End-of-day report** — A summary of all deliveries: completed, rescheduled, failed, and any customer issues flagged.

## Implementation

### Key MCP tools used

```
add_contacts(contacts=[...])                       -> Import daily manifest
manage_contact_tags(id="...", action="add", tags=["route-A", "window-2pm-4pm"])
                                                   -> Tag delivery metadata
send_sms_batch(messages=[...])                     -> Bulk morning notifications
send_sms(phone_number="+33...", message="...")      -> Individual status updates
sms_conversation(phone_number="+33...")             -> Handle inbound questions
search_contacts(query="route-A")                    -> Find customers on a route
```

### Example agent interaction

**Trigger**: 8:00am — Daily manifest imported. 142 deliveries across 6 routes.

**Agent action**:
1. Imports contacts via `add_contacts` with tags: `delivery-2026-04-14`, `route-B`, `window-10am-12pm`
2. Sends morning notifications via `send_sms_batch` to all 142 customers. Example for +33600000006:
   > "Good morning! Your LivrExpress delivery is scheduled today between 10am and 12pm. We'll text you when the driver is nearby. Reply RESCHEDULE if you won't be available."

**10:15am** — Driver completes stop 4 on route B. Agent sends "next up" SMS to stop 5:

```
send_sms(
    phone_number="+33600000007",
    message="Your LivrExpress package is on its way! Estimated arrival in about 25 minutes. The driver will ring the doorbell. Need to leave special instructions? Reply here."
)
```

**10:20am** — Customer at +33600000007 replies:
> "Please leave it with the neighbor at #12, I'm not home"

**Agent action**:
1. Reads via `sms_conversation(phone_number="+33600000007")`
2. Classifies: delivery instruction (actionable, needs dispatch)
3. Tags contact: `special-instructions`
4. Sends acknowledgment:
   > "Got it! I've noted: leave package with neighbor at #12. The driver will be informed. Thanks!"

**10:45am** — Delivery complete. Agent sends confirmation:

```
send_sms(
    phone_number="+33600000007",
    message="Delivered! Your package was left with your neighbor at #12 as requested. Questions? Reply here or call 05 61 00 00 00."
)
```
Tags contact: `delivered`

**Meanwhile**, a customer on route D texts unprompted:
> "Can you deliver after 5pm instead? I won't be home until then."

**Agent action**:
1. Reads conversation, classifies: reschedule request
2. Tags: `reschedule-requested`, `route-D`
3. Sends:
   > "I'll pass your request to our dispatch team. We'll confirm a new window by SMS within the hour."

## Results

| Metric | Before | After |
|--------|--------|-------|
| "Where's my package?" calls/day | 20-25 | 4-5 |
| Dispatcher phone time | 2 hours/day | 20 min/day |
| Customer satisfaction (NPS) | 28 | 63 (+35 points) |
| Failed deliveries (not home) | 12% | 5% |

The insight: most "where is my package?" calls come from anxiety, not from actual problems. A proactive SMS at the right moment ("your package is 25 minutes away") eliminates the anxiety and the call. The dispatch team can focus on real exceptions instead of answering the same question 20 times.

## Related study cases

- [E-commerce: AI night support via MCP](./ecommerce-night-support.md) — Parent study case (P2)
- [Healthtech: Patient appointment reminders](./healthtech-appointment-reminders.md) — Time-sensitive notifications
- [Competitive intelligence: SMS alerts](./competitive-intelligence-alerts.md) — Event-triggered SMS
