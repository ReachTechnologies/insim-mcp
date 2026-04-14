# "Our competitor launched a feature we planned for Q3. I found out a week late on Twitter."

> **Persona**: Alex, product manager at a B2B SaaS — Paris, France — 30 employees
> **Tool**: insim-mcp (MCP server + Claude Code + web monitoring)
> **Setup time**: 1 hour
> **ROI estimate**: Competitive awareness from weeks to hours, faster strategic pivots

## The problem

Alex is the product manager at DataBridge, a B2B data integration SaaS. They compete against 4 main players in a fast-moving market. Last quarter, their biggest competitor quietly launched a self-serve API builder — a feature Alex's team had on their Q3 roadmap. Alex found out a week later, scrolling Twitter on a Sunday. By then, two prospects had already asked "Competitor X has this, do you?"

The team monitors competitors manually: someone checks their blogs once a week, another scans Product Hunt, someone else watches LinkedIn. It's inconsistent, slow, and nobody owns it. Important signals — pricing changes, new integrations, key hires, funding rounds — slip through the cracks. By the time the team reacts, the market has already moved.

Alex doesn't need a full-blown competitive intelligence platform. He needs a simple alert: when something important happens, send me an SMS so I see it immediately, not buried in an email newsletter he'll read on Friday.

## The solution with inSIM

1. **Contact setup** — Alex adds himself and 3 key stakeholders (CEO, head of sales, lead engineer) as inSIM contacts, tagged by alert preference (all alerts, pricing only, features only).
2. **Monitoring agent** — A scheduled agent monitors competitor sources (blogs, changelogs, pricing pages, social media). When it detects a significant change, it drafts a concise SMS alert.
3. **Smart filtering** — Not every blog post is worth an SMS. The agent classifies signals by impact: critical (pricing change, major feature launch, funding), notable (minor feature, new integration, key hire), and noise (blog content, marketing fluff). Only critical and notable signals trigger SMS.
4. **Team distribution** — Alerts go to the right people. Pricing changes go to sales. Feature launches go to product and engineering. Funding news goes to the CEO.

## Implementation

### Key MCP tools used

```
add_contacts(contacts=[...])                      -> Add team members as alert recipients
manage_contact_tags(id="...", action="add", tags=["alert-all"])
                                                  -> Set alert preferences per person
send_sms(phone_number="+33...", message="...")     -> Deliver alert to individual
send_sms_batch(messages=[...])                    -> Broadcast critical alerts to full team
create_list(name="competitive-intel-team")         -> Group alert recipients
search_contacts(query="alert-pricing")             -> Find recipients for pricing alerts
```

### Example agent interaction

**Trigger**: Agent's monitoring cycle detects that Competitor X updated their pricing page. The /enterprise tier price dropped from $499/mo to $299/mo.

**Agent action**:
1. Classifies signal: CRITICAL (pricing change, direct competitor, significant drop)
2. Searches recipients: `search_contacts(query="alert-pricing")` — finds Alex (+33600000010), Sarah (head of sales, +33600000011), Pierre (CEO, +33600000012)
3. Sends alert via `send_sms_batch`:
   > "COMPETITOR ALERT: Competitor X dropped Enterprise pricing from $499 to $299/mo (40% cut). This undercuts our $399 tier. Source: their pricing page, changed today. — DataBridge Intel"
4. Tags all recipients: `alert-sent-2026-04-14`

**Alex replies**:
> "Can you check if they changed features on that tier too?"

**Agent action**:
1. Reads conversation via `sms_conversation(phone_number="+33600000010")`
2. The agent's next monitoring pass focuses on Competitor X's enterprise feature list
3. Sends follow-up:
   > "Checked: Enterprise tier now includes API builder (was Pro-only) and SSO (was add-on). They're bundling up-market features at a lower price. Full comparison ready when you want it."

**Another signal**: Competitor Y announces Series B funding on LinkedIn.

**Agent action**:
1. Classifies: NOTABLE (funding, indirect competitor)
2. Searches recipients: `search_contacts(query="alert-all")` — finds only Alex and Pierre
3. Sends via `send_sms`:
   > "INTEL: Competitor Y raised $18M Series B (led by Accel). They'll likely accelerate hiring and product dev. Watch for enterprise push in 6-9 months."

## Results

| Metric | Before | After |
|--------|--------|-------|
| Time to learn about competitor moves | 1-2 weeks | 2-4 hours |
| Competitive signals missed per quarter | 5-8 | 0-1 |
| Strategic response time | Weeks (next planning cycle) | Days (same-week discussion) |
| Team time spent on manual monitoring | 3 hours/week across team | 0 (fully automated) |

The insight: competitive intelligence is useless if it arrives late. An SMS alert that reaches the right person within hours of a competitor move turns information into action. The SMS format forces brevity — no 10-page reports nobody reads, just the signal and why it matters.

## Related study cases

- [Autonomous prospecting agent](./autonomous-prospecting-agent.md) — Parent study case (P4), autonomous agent pattern
- [SaaS: SMS onboarding for new users](./saas-sms-onboarding.md) — Event-triggered SMS
- [Debt collection: Invoice follow-up agent](./debt-collection-followup.md) — Graduated sequence pattern
