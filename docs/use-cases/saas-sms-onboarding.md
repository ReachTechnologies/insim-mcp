# "30% of new signups never finish onboarding. We lose them in silence."

> **Persona**: Julie, CTO of a project management SaaS — Lyon, France — 8 employees
> **Tool**: insim-mcp (MCP server + Claude Code)
> **Setup time**: 45 minutes
> **ROI estimate**: +40% onboarding completion, -25% churn in first 30 days

## The problem

Julie runs the tech at PlanFlow, a project management SaaS for freelancers and small agencies. They get 200 new signups per month, but analytics tell a painful story: 30% of users never complete onboarding. They sign up, maybe click around for 2 minutes, and vanish.

The team tried email drip sequences. Open rates hovered at 18%. Most onboarding emails landed in promotions tabs or got ignored entirely. Julie noticed something else: when the sales team personally texted a high-value lead, the response rate was 70%. SMS cuts through the noise — but nobody has time to text 200 new users a month, let alone personalize each message based on where they are in the onboarding flow.

## The solution with inSIM

1. **Import** — When a user signs up, the agent adds them to inSIM via `add_contacts` with tags indicating signup date and plan tier. A webhook triggers the onboarding flow.
2. **Milestone SMS** — The agent sends personalized SMS at three key moments: 24 hours after signup (welcome + first action nudge), after first project created (congratulations + next tip), and after 3 days of inactivity (re-engagement with help offer).
3. **Conversation handling** — When users reply (questions, confusion, frustration), the agent reads the conversation, classifies the issue, and either answers directly or tags for human follow-up.
4. **Weekly report** — Every Monday, the team gets onboarding metrics: how many users were contacted, who replied, who completed onboarding, who needs a human touch.

## Implementation

### Key MCP tools used

```
add_contacts(contacts=[...])                    -> Import new signups
manage_contact_tags(id="...", action="add", tags=["signup-day1"])
                                                -> Track onboarding stage
send_sms(phone_number="+33...", message="...")   -> Send milestone SMS
sms_conversation(phone_number="+33...")          -> Read user replies
search_contacts(query="inactive-3d")             -> Find disengaged users
list_contacts(search="needs-human")              -> Morning review queue
```

### Example agent interaction

**Trigger**: User signed up 24 hours ago, has not created a project.

**Agent action**:
1. Searches contacts tagged `signup-day1` via `search_contacts`
2. Finds: Sophie Leroux, +33600000001, signed up yesterday, free trial, 0 projects
3. Sends via `send_sms`:
   > "Hi Sophie! It's Julie from PlanFlow. You signed up yesterday — nice! Most users create their first project in under 2 minutes. Want to try? Here's a quick start guide: https://planflow.io/start — Reply here if you need help!"
4. Updates tags: removes `signup-day1`, adds `nudge-sent`

**2 hours later** — Sophie replies:
> "Hi! I tried but I can't figure out how to invite my team."

**Agent action**:
1. Reads conversation via `sms_conversation(phone_number="+33600000001")`
2. Classifies: product question (answerable)
3. Sends reply via `send_sms`:
   > "Great question! In your project, tap the 'Team' tab at the top, then 'Invite by email.' You can add up to 5 people on the free plan. Let me know if it works!"
4. Tags contact: `engaged`, `asked-question`

**3 days later** — Another user, Marc Duval (+33600000002), has not logged in since signup.

**Agent action**:
1. Finds Marc via `search_contacts(query="inactive-3d")`
2. Sends re-engagement SMS via `send_sms`:
   > "Hi Marc, Julie from PlanFlow here. I noticed you haven't had a chance to explore yet. No worries — want me to set up a sample project for you so you can see how it works? Just reply 'yes' and I'll do it in 2 minutes."
3. Tags: `reengagement-sent`

## Results

| Metric | Before | After |
|--------|--------|-------|
| Onboarding completion rate | 70% | 88% (+18 points) |
| First-week churn | 25% | 12% |
| User response rate (SMS vs email) | 18% (email) | 65% (SMS) |
| Support tickets from new users | 40/month | 15/month |

The insight: onboarding is not a funnel problem, it's a timing problem. Users get stuck at predictable moments. An SMS that arrives at exactly the right time — with a real answer from a real number — turns a silent dropout into an active user.

## Related study cases

- [E-commerce: AI night support via MCP](./ecommerce-night-support.md) — Parent study case (P2)
- [Healthtech: Patient appointment reminders](./healthtech-appointment-reminders.md) — Another sector variant
- [Logistics: Delivery notifications](./logistics-delivery-notifications.md) — Proactive status updates
