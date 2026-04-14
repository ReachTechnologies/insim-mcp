# Night Support Agent Prompt

Copy-paste this prompt into Claude Code (with insim-mcp configured) to run the night support workflow described in the [study case](../docs/use-cases/ecommerce-night-support.md).

## Prompt

```
Read all incoming SMS from the last 12 hours using the insim MCP server. For each SMS:

1. Look up the sender's contact info
2. Read the full conversation history (last 5 messages)
3. Classify the message:
   - DELIVERY: shipping, tracking, ETA questions
   - PRODUCT: availability, pricing, specs
   - RETURN: return or exchange requests
   - COMPLAINT: negative feedback
   - OTHER: anything else

4. For DELIVERY and PRODUCT messages:
   - Draft a helpful, friendly reply (max 160 characters)
   - Send it via inSIM
   - Tag the contact with "auto-replied"

5. For RETURN, COMPLAINT, and OTHER:
   - Tag the contact with "needs-human"
   - Do NOT send a reply

6. After processing all messages, give me a summary:
   - How many SMS handled
   - How many auto-replied
   - How many flagged for human review
   - List the flagged contacts with their phone number and issue
```

## Expected behavior

The agent will use these MCP tools automatically:
- `list_sms` — fetch incoming messages
- `find_contact` / `search_contacts` — look up sender
- `sms_conversation` — read thread history
- `send_sms` — send auto-reply
- `manage_contact_tags` — tag contacts
