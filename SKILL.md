---
name: insim-mcp
description: >-
  MCP server connecting AI agents to real mobile telephony — send SMS, make calls,
  qualify leads, manage contacts and campaigns through a real phone number.
  46 tools across 10 domains. Compatible with Claude Code, Cursor, Windsurf, and 20+ clients.
---

# insim-mcp

Connect any AI agent to real mobile telephony. One MCP server, 20+ compatible clients.

## Installation

```bash
pip install insim-mcp
```

## Configuration (Claude Code)

```json
{
  "mcpServers": {
    "insim": {
      "command": "insim-mcp",
      "env": {
        "INSIM_LOGIN": "your@email.com",
        "INSIM_ACCESS_KEY": "your-access-key"
      }
    }
  }
}
```

## Tools by Domain

### Contacts (8 tools)
`find_contact`, `list_contacts`, `contact_detail`, `search_contacts`, `switch_contact_pro`, `delete_contact`, `manage_contact_tags`, `list_custom_fields`

### SMS (4 tools)
`list_sms`, `sms_detail`, `sms_conversation`, `sms_delivery_status`

### Calls (2 tools)
`list_calls`, `qualify_call`

### Qualifications (6 tools)
`list_qualifications`, `list_qualification_options`, `create_qualification_option`, `update_qualification_option`, `delete_qualification_option`, `qualification_stats`

### Account (2 tools)
`account_info`, `manage_webhooks`

### Lists (8 tools)
`list_lists`, `create_list`, `list_detail`, `update_list`, `delete_list`, `add_contacts_to_list`, `remove_contacts_from_list`, `add_all_contacts_to_list`

### Campaigns (5 tools)
`list_campaigns`, `create_campaign`, `campaign_detail`, `cancel_campaign`, `start_campaign`

### Templates (5 tools)
`list_templates`, `create_template`, `update_template`, `delete_template`, `send_template`

### Stats (2 tools)
`stats_overview`, `stats_clicks`

### Sending (4 tools)
`send_sms`, `send_sms_batch`, `add_contacts`, `click_to_call`

## Tips for AI Agents

1. Check credits with `account_info` before sending SMS
2. Use `search_contacts` for fuzzy name matching — handles typos and inversions
3. Always confirm with the user before `send_sms` or `start_campaign`
4. Campaign status: 0=ready, 1=launched, 3=completed. Only status 0 can be started.
5. Use `sms_conversation` to get full context before replying
