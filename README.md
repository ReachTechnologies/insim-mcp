# insim-mcp

> **Connect any AI agent to real mobile telephony.**
> One MCP server. 20+ compatible clients.

[![PyPI version](https://img.shields.io/pypi/v/insim-mcp.svg)](https://pypi.org/project/insim-mcp/)
[![MCP](https://img.shields.io/badge/MCP-compatible-brightgreen.svg)](https://modelcontextprotocol.io)
[![Python 3.10+](https://img.shields.io/pypi/pyversions/insim-mcp.svg)](https://pypi.org/project/insim-mcp/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## The problem

AI agents are powerful but phoneless. They can search the web, write code, query databases — but they can't call a real person or text a real phone number.

VoIP and virtual numbers don't work: customers don't pick up unknown numbers, and they can't call back.

## The solution

`insim-mcp` is a Model Context Protocol server that gives any AI agent the ability to send SMS, make calls, qualify leads, and manage contacts — all through a real mobile phone with a real number.

```bash
pip install insim-mcp
```

One install. 46 tools. Your agent gets a real phone.

## Compatible clients

**IDE & code agents:**
Claude Code, Cursor, Windsurf, VS Code + Copilot, Cline, Kiro (AWS), Codex CLI (OpenAI), Augment Code, OpenClaw

**AI agents:**
Claude Desktop, ChatGPT (via connectors), Devin, Manus AI, Mistral Le Chat

**Agent frameworks:**
LangChain / LangGraph, CrewAI, AutoGen (Microsoft), Pydantic AI, Vercel AI SDK, Semantic Kernel, Mastra

**Orchestrators:**
Glama, Smithery, PulseMCP, MCP Registry (GitHub)

## Quickstart

### Install

```bash
pip install insim-mcp
```

Get your API credentials from your [inSIM account settings](https://www.insim.app) under API.

### Claude Code

Add to your `.mcp.json`:

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

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

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

### Cursor

Add to `.cursor/mcp.json` in your project:

```json
{
  "mcpServers": {
    "insim": {
      "command": "insim-mcp",
      "args": [],
      "env": {
        "INSIM_LOGIN": "your@email.com",
        "INSIM_ACCESS_KEY": "your-access-key"
      }
    }
  }
}
```

### Windsurf

Add to your Windsurf MCP config:

```json
{
  "mcpServers": {
    "insim": {
      "serverUrl": "http://localhost:8000/mcp",
      "env": {
        "INSIM_LOGIN": "your@email.com",
        "INSIM_ACCESS_KEY": "your-access-key"
      }
    }
  }
}
```

> For Windsurf, run `insim-mcp --http 8000` to start in HTTP mode, then configure the `serverUrl` above.

### Environment Variables

For any client, you can also set credentials as environment variables:

```bash
export INSIM_LOGIN="your@email.com"
export INSIM_ACCESS_KEY="your-access-key"
```

## Available tools

### Contacts (8 tools)

| Tool | Description |
|------|-------------|
| `find_contact` | Find contacts by phone number |
| `list_contacts` | List contacts with search, pagination, sorting |
| `contact_detail` | Get full contact details by ID |
| `search_contacts` | Smart search by name (handles typos, inversions) |
| `switch_contact_pro` | Share or privatize a contact |
| `delete_contact` | Delete a contact |
| `manage_contact_tags` | Add or remove tags on a contact |
| `list_custom_fields` | List custom contact fields |

### SMS (4 tools)

| Tool | Description |
|------|-------------|
| `list_sms` | List SMS with filters (direction, phone, date) |
| `sms_detail` | Get full SMS details with click tracking |
| `sms_conversation` | Get conversation thread with a phone number |
| `sms_delivery_status` | Check SMS delivery status |

### Calls (2 tools)

| Tool | Description |
|------|-------------|
| `list_calls` | Call log with type and phone filters |
| `qualify_call` | Qualify a call with category and notes |

### Qualifications (6 tools)

| Tool | Description |
|------|-------------|
| `list_qualifications` | List qualified calls |
| `list_qualification_options` | List qualification categories |
| `create_qualification_option` | Create a qualification category |
| `update_qualification_option` | Rename a category |
| `delete_qualification_option` | Delete a category |
| `qualification_stats` | Qualification statistics |

### Account (2 tools)

| Tool | Description |
|------|-------------|
| `account_info` | Account details, credits, connected devices |
| `manage_webhooks` | Configure webhook URLs for SMS, calls, delivery |

### Lists (8 tools)

| Tool | Description |
|------|-------------|
| `list_lists` | List all contact lists |
| `create_list` | Create a new contact list |
| `list_detail` | Get list details with contacts |
| `update_list` | Rename a list |
| `delete_list` | Delete a list |
| `add_contacts_to_list` | Add specific contacts to a list |
| `remove_contacts_from_list` | Remove contacts from a list |
| `add_all_contacts_to_list` | Add all contacts to a list |

### Campaigns (5 tools)

| Tool | Description |
|------|-------------|
| `list_campaigns` | List all campaigns |
| `create_campaign` | Create an SMS campaign |
| `campaign_detail` | Get campaign details and stats |
| `cancel_campaign` | Cancel a pending campaign |
| `start_campaign` | Launch a campaign (sends real SMS) |

### Templates (5 tools)

| Tool | Description |
|------|-------------|
| `list_templates` | List message templates |
| `create_template` | Create a template with variables |
| `update_template` | Update template content |
| `delete_template` | Delete a template |
| `send_template` | Send SMS using a template |

### Stats (2 tools)

| Tool | Description |
|------|-------------|
| `stats_overview` | SMS, calls, clicks, contacts summary |
| `stats_clicks` | Link click tracking details |

### Sending (4 tools)

| Tool | Description |
|------|-------------|
| `send_sms` | Send an SMS to a phone number |
| `send_sms_batch` | Send SMS to multiple recipients |
| `add_contacts` | Create or update contacts in bulk |
| `click_to_call` | Initiate a call via connected device |

## What agents can do with insim-mcp

- **Answer incoming SMS** — read conversations, draft replies, send responses
- **Qualify leads** — check missed calls, send follow-up SMS, tag contacts
- **Run campaigns** — create lists, compose messages, launch SMS campaigns
- **Morning briefing** — summarize overnight SMS, missed calls, delivery reports
- **CRM operations** — search contacts, manage tags, track engagement stats

## Authentication

All tools use the `INSIM_LOGIN` and `INSIM_ACCESS_KEY` environment variables. Set them in your MCP client config or export them in your shell.

Get your credentials from your [inSIM account](https://www.insim.app) under Settings > API.

## Requirements

- Python 3.10+
- An inSIM account with API access
- The [inSIM Android app](https://play.google.com/store/apps/details?id=com.wstechnologies.ardarysolo) installed on your phone

## Study cases

- [Real estate agent: AI follow-up after open house](./docs/use-cases/) *(coming soon)*
- [E-commerce: AI answering SMS at night](./docs/use-cases/) *(coming soon)*
- [Recruitment: AI outreach to candidates](./docs/use-cases/) *(coming soon)*

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for development setup and guidelines.

## License

Apache 2.0 — see [LICENSE](./LICENSE).

---

Built by [Reach Technologies](https://www.insim.app) — the company behind inSIM.
