"""MCP server for inSIM API v2 — 45 tools covering contacts, SMS, calls,
qualifications, account, lists, campaigns, templates, stats, and sending."""

import json
import os
from datetime import datetime
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------
mcp = FastMCP(
    "insim",
    instructions=(
        "inSIM MCP server — manage contacts, SMS, calls, campaigns, lists, "
        "templates and statistics for the inSIM platform. "
        "All tools call the inSIM API v2 (POST-only, JSON). "
        "Auth is injected automatically from INSIM_LOGIN + INSIM_ACCESS_KEY env vars."
    ),
)

# ---------------------------------------------------------------------------
# HTTP helper
# ---------------------------------------------------------------------------
BASE_URL = os.environ.get("INSIM_BASE_URL", "https://www.insim.app")
_client: httpx.Client | None = None


def _get_client() -> httpx.Client:
    global _client
    if _client is None:
        _client = httpx.Client(
            base_url=BASE_URL,
            timeout=60.0,
            verify=False,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "mcp-insim/1.0.0",
            },
        )
    return _client


def _api_post(endpoint: str, data: dict[str, Any] | None = None) -> dict:
    """POST to an inSIM API v2 endpoint with automatic auth + empty-param filtering."""
    login = os.environ.get("INSIM_LOGIN", "")
    access_key = os.environ.get("INSIM_ACCESS_KEY", "")
    if not login or not access_key:
        return {"success": False, "error": "INSIM_LOGIN and INSIM_ACCESS_KEY env vars are required."}

    payload: dict[str, Any] = {"login": login, "accessKey": access_key}
    if data:
        for k, v in data.items():
            if v is not None and v != "" and v != []:
                payload[k] = v

    resp = _get_client().post(endpoint, json=payload)
    body = resp.json()
    return body


# ═══════════════════════════════════════════════════════════════════════════
# CONTACTS (8 tools)
# ═══════════════════════════════════════════════════════════════════════════

@mcp.tool()
def find_contact(phone_number: str) -> str:
    """Find contacts by phone number. Accepts international (+33...) or local (06...) format."""
    return json.dumps(_api_post("/api/v2/find_contact", {"phone_number": phone_number}))


@mcp.tool()
def list_contacts(
    search: str = "",
    limit: int = 50,
    cursor: str = "",
    sort: str = "date_add",
    order: str = "desc",
) -> str:
    """List contacts with optional text search, pagination, and sorting.

    Args:
        search: Filter by name, phone, email, or company.
        limit: Max results (1-100, default 50).
        cursor: Pagination cursor from previous response.
        sort: Sort field — date_add, lastname, firstname.
        order: Sort order — asc or desc.
    """
    return json.dumps(_api_post("/api/v2/contacts", {
        "search": search, "limit": limit, "cursor": cursor, "sort": sort, "order": order,
    }))


@mcp.tool()
def contact_detail(id_contact: str) -> str:
    """Get full details for a single contact by ID."""
    return json.dumps(_api_post("/api/v2/contacts/detail", {"id_contact": id_contact}))


@mcp.tool()
def search_contacts(
    name: str,
    mode: str = "smart",
    fuzzy: bool = True,
    limit: int = 20,
) -> str:
    """Search contacts by name with smart/fuzzy matching.

    Args:
        name: Name to search for.
        mode: Search mode — smart (cross-field + fuzzy), exact, starts_with.
        fuzzy: Enable typo tolerance (default true).
        limit: Max results (1-100, default 20).
    """
    return json.dumps(_api_post("/api/v2/contacts/search", {
        "name": name, "mode": mode, "fuzzy": fuzzy, "limit": limit,
    }))


@mcp.tool()
def switch_contact_pro(id_contact: str, pro: bool) -> str:
    """Toggle a contact between Pro (shared with team) and Perso (private).

    Args:
        id_contact: Contact ID.
        pro: true = Pro (shared), false = Perso (private).
    """
    return json.dumps(_api_post("/api/v2/contacts/switch_pro", {
        "id_contact": id_contact, "pro": pro,
    }))


@mcp.tool()
def delete_contact(id_contact: str) -> str:
    """Delete a contact by ID (soft delete)."""
    return json.dumps(_api_post("/api/v2/contacts/delete", {"id_contact": id_contact}))


@mcp.tool()
def manage_contact_tags(
    id_contact: str,
    add: list[str] | None = None,
    remove: list[str] | None = None,
) -> str:
    """Add and/or remove tags on a contact.

    Args:
        id_contact: Contact ID.
        add: List of tags to add (e.g. ["vip", "prospect"]).
        remove: List of tags to remove.
    """
    return json.dumps(_api_post("/api/v2/contacts/tags", {
        "id_contact": id_contact,
        "add": add or [],
        "remove": remove or [],
    }))


@mcp.tool()
def list_custom_fields() -> str:
    """List all custom fields defined for contacts in this account."""
    return json.dumps(_api_post("/api/v2/contacts/custom_fields"))


# ═══════════════════════════════════════════════════════════════════════════
# SMS (4 tools)
# ═══════════════════════════════════════════════════════════════════════════

@mcp.tool()
def list_sms(
    direction: str = "all",
    phone_number: str = "",
    date_from: str = "",
    date_to: str = "",
    status: str = "",
    limit: int = 50,
    cursor: str = "",
) -> str:
    """List SMS messages with optional filters.

    Args:
        direction: all, inbound, or outbound.
        phone_number: Filter by phone number.
        date_from: Start date (ISO 8601, e.g. 2026-01-01).
        date_to: End date.
        status: Filter by status (0 = pending, sms_receive = delivered).
        limit: Max results (1-100).
        cursor: Pagination cursor.
    """
    return json.dumps(_api_post("/api/v2/sms", {
        "direction": direction, "phone_number": phone_number,
        "date_from": date_from, "date_to": date_to,
        "status": status, "limit": limit, "cursor": cursor,
    }))


@mcp.tool()
def sms_detail(sms_id: str) -> str:
    """Get full details for a specific SMS by ID, including click tracking."""
    return json.dumps(_api_post("/api/v2/sms/detail", {"sms_id": sms_id}))


@mcp.tool()
def sms_conversation(phone_number: str, limit: int = 20) -> str:
    """Get the SMS conversation thread with a phone number (chronological order).

    Args:
        phone_number: Phone number to get conversation for.
        limit: Max messages to return (default 20).
    """
    return json.dumps(_api_post("/api/v2/sms/conversation", {
        "phone_number": phone_number, "limit": limit,
    }))


@mcp.tool()
def sms_delivery_status(
    sms_id: str = "",
    sms_ids: list[str] | None = None,
) -> str:
    """Check delivery status for one or more SMS.

    Args:
        sms_id: Single SMS ID (for unit check).
        sms_ids: List of SMS IDs (for batch check, max 100).
    """
    data: dict[str, Any] = {}
    if sms_ids:
        data["sms_ids"] = sms_ids
    elif sms_id:
        data["sms_id"] = sms_id
    return json.dumps(_api_post("/api/v2/sms/delivery_status", data))


# ═══════════════════════════════════════════════════════════════════════════
# CALLS (2 tools)
# ═══════════════════════════════════════════════════════════════════════════

@mcp.tool()
def list_calls(
    call_type: str = "all",
    phone_number: str = "",
    qualified: bool | None = None,
    date_from: str = "",
    date_to: str = "",
    limit: int = 50,
    cursor: str = "",
) -> str:
    """List calls with optional filters.

    Args:
        call_type: all, incoming, outgoing, missed, blocked, voicemail.
        phone_number: Filter by phone number.
        qualified: true = qualified only, false = unqualified only.
        date_from: Start date (ISO 8601).
        date_to: End date.
        limit: Max results (1-100).
        cursor: Pagination cursor.
    """
    data: dict[str, Any] = {
        "type": call_type, "phone_number": phone_number,
        "date_from": date_from, "date_to": date_to,
        "limit": limit, "cursor": cursor,
    }
    if qualified is not None:
        data["qualified"] = qualified
    return json.dumps(_api_post("/api/v2/calls", data))


@mcp.tool()
def qualify_call(call_id: str, option_id: str, notes: str = "") -> str:
    """Qualify a call with a qualification option and optional notes.

    Args:
        call_id: Call ID to qualify.
        option_id: Qualification option ID (from list_qualification_options).
        notes: Additional notes about the call.
    """
    return json.dumps(_api_post("/api/v2/calls/qualify", {
        "call_id": call_id, "option_id": option_id, "notes": notes,
    }))


# ═══════════════════════════════════════════════════════════════════════════
# QUALIFICATIONS (6 tools)
# ═══════════════════════════════════════════════════════════════════════════

@mcp.tool()
def list_qualifications(
    phone_number: str = "",
    option_id: str = "",
    date_from: str = "",
    date_to: str = "",
    limit: int = 50,
) -> str:
    """List qualified calls with optional filters.

    Args:
        phone_number: Filter by phone number.
        option_id: Filter by qualification category.
        date_from: Start date (ISO 8601).
        date_to: End date.
        limit: Max results.
    """
    return json.dumps(_api_post("/api/v2/qualifications", {
        "phone_number": phone_number, "option_id": option_id,
        "date_from": date_from, "date_to": date_to, "limit": limit,
    }))


@mcp.tool()
def list_qualification_options() -> str:
    """List all available qualification categories/options."""
    return json.dumps(_api_post("/api/v2/qualifications/options"))


@mcp.tool()
def create_qualification_option(label: str) -> str:
    """Create a new qualification option/category.

    Args:
        label: Label for the new option (e.g. "Interested", "Not available").
    """
    return json.dumps(_api_post("/api/v2/qualifications/options/create", {"label": label}))


@mcp.tool()
def update_qualification_option(option_id: str, label: str) -> str:
    """Update a qualification option label.

    Args:
        option_id: Option ID to update.
        label: New label.
    """
    return json.dumps(_api_post("/api/v2/qualifications/options/update", {
        "option_id": option_id, "label": label,
    }))


@mcp.tool()
def delete_qualification_option(option_id: str) -> str:
    """Delete a qualification option by ID."""
    return json.dumps(_api_post("/api/v2/qualifications/options/delete", {"option_id": option_id}))


@mcp.tool()
def qualification_stats(date_from: str = "", date_to: str = "") -> str:
    """Get qualification statistics, optionally filtered by date range.

    Args:
        date_from: Start date (ISO 8601).
        date_to: End date.
    """
    return json.dumps(_api_post("/api/v2/qualifications/stats", {
        "date_from": date_from, "date_to": date_to,
    }))


# ═══════════════════════════════════════════════════════════════════════════
# ACCOUNT (2 tools)
# ═══════════════════════════════════════════════════════════════════════════

@mcp.tool()
def account_info() -> str:
    """Get account information: login, plan, SMS credits, active options, connected devices."""
    return json.dumps(_api_post("/api/v2/account"))


@mcp.tool()
def manage_webhooks(
    action: str = "get",
    incoming_sms: str = "",
    delivery_status: str = "",
    link_clicks: str = "",
    call_events: str = "",
    call_qualifications: str = "",
) -> str:
    """Read or configure account webhooks. Premium feature.

    Args:
        action: "get" to read current webhooks, omit or any other value to set them.
        incoming_sms: Webhook URL for incoming SMS.
        delivery_status: Webhook URL for delivery receipts.
        link_clicks: Webhook URL for link click tracking.
        call_events: Webhook URL for call events.
        call_qualifications: Webhook URL for call qualifications.
    """
    if action == "get":
        return json.dumps(_api_post("/api/v2/account/webhooks", {"action": "get"}))
    return json.dumps(_api_post("/api/v2/account/webhooks", {
        "webhooks": {
            "incoming_sms": incoming_sms,
            "delivery_status": delivery_status,
            "link_clicks": link_clicks,
            "call_events": call_events,
            "call_qualifications": call_qualifications,
        },
    }))


# ═══════════════════════════════════════════════════════════════════════════
# LISTS (8 tools)
# ═══════════════════════════════════════════════════════════════════════════

@mcp.tool()
def list_lists() -> str:
    """List all contact lists in the account."""
    return json.dumps(_api_post("/api/v2/lists"))


@mcp.tool()
def create_list(name: str, description: str = "") -> str:
    """Create a new contact list.

    Args:
        name: List name.
        description: Optional description.
    """
    return json.dumps(_api_post("/api/v2/lists/create", {
        "name": name, "description": description,
    }))


@mcp.tool()
def list_detail(list_id: str) -> str:
    """Get details and members of a contact list.

    Args:
        list_id: List ID.
    """
    return json.dumps(_api_post("/api/v2/lists/detail", {"list_id": list_id}))


@mcp.tool()
def update_list(list_id: str, name: str = "", description: str = "") -> str:
    """Update a contact list name and/or description.

    Args:
        list_id: List ID.
        name: New name (leave empty to keep current).
        description: New description.
    """
    return json.dumps(_api_post("/api/v2/lists/update", {
        "list_id": list_id, "name": name, "description": description,
    }))


@mcp.tool()
def delete_list(list_id: str) -> str:
    """Delete a contact list (soft delete)."""
    return json.dumps(_api_post("/api/v2/lists/delete", {"list_id": list_id}))


@mcp.tool()
def add_contacts_to_list(list_id: str, contact_ids: list[str]) -> str:
    """Add contacts to a list by their IDs.

    Args:
        list_id: Target list ID.
        contact_ids: List of contact IDs to add.
    """
    return json.dumps(_api_post("/api/v2/lists/contacts/add", {
        "list_id": list_id, "contact_ids": contact_ids,
    }))


@mcp.tool()
def remove_contacts_from_list(list_id: str, contact_ids: list[str]) -> str:
    """Remove contacts from a list by their IDs.

    Args:
        list_id: Target list ID.
        contact_ids: List of contact IDs to remove.
    """
    return json.dumps(_api_post("/api/v2/lists/contacts/remove", {
        "list_id": list_id, "contact_ids": contact_ids,
    }))


@mcp.tool()
def add_all_contacts_to_list(list_id: str) -> str:
    """Add ALL contacts from the account to a list.

    Args:
        list_id: Target list ID.
    """
    return json.dumps(_api_post("/api/v2/lists/contacts/addall", {"list_id": list_id}))


# ═══════════════════════════════════════════════════════════════════════════
# CAMPAIGNS (5 tools)
# ═══════════════════════════════════════════════════════════════════════════

@mcp.tool()
def list_campaigns(limit: int = 10) -> str:
    """List SMS campaigns.

    Args:
        limit: Max results (default 10).
    """
    return json.dumps(_api_post("/api/v2/campaigns", {"limit": limit}))


@mcp.tool()
def create_campaign(
    name: str,
    message: str,
    list_id: str = "",
    contact_ids: list[str] | None = None,
    phone_numbers: list[str] | None = None,
    priority: int = 1,
    url: str = "",
) -> str:
    """Create a new SMS campaign. Provide list_id, contact_ids, or phone_numbers as recipients.

    Args:
        name: Campaign name.
        message: SMS message body. Use [link] placeholder for tracked URLs.
        list_id: Target list ID (recipients from a list).
        contact_ids: List of contact IDs as recipients.
        phone_numbers: List of phone numbers as recipients.
        priority: Campaign priority (1 = normal).
        url: URL to track (used with [link] in message).
    """
    data: dict[str, Any] = {
        "name": name, "message": message, "priority": priority, "url": url,
    }
    if list_id:
        data["list_id"] = list_id
    if contact_ids:
        data["contact_ids"] = contact_ids
    if phone_numbers:
        data["phone_numbers"] = phone_numbers
    return json.dumps(_api_post("/api/v2/campaigns/create", data))


@mcp.tool()
def campaign_detail(campaign_id: str) -> str:
    """Get details of a campaign including recipient count.

    Args:
        campaign_id: Campaign ID.
    """
    return json.dumps(_api_post("/api/v2/campaigns/detail", {"campaign_id": campaign_id}))


@mcp.tool()
def cancel_campaign(campaign_id: str) -> str:
    """Cancel a campaign (only status 0 or 2 can be cancelled).

    Args:
        campaign_id: Campaign ID to cancel.
    """
    return json.dumps(_api_post("/api/v2/campaigns/cancel", {"campaign_id": campaign_id}))


@mcp.tool()
def start_campaign(campaign_id: str) -> str:
    """Launch a campaign — this sends SMS to all recipients. Premium feature.

    Args:
        campaign_id: Campaign ID to start. Must be status 0 with recipients.
    """
    return json.dumps(_api_post("/api/v2/campaigns/start", {"campaign_id": campaign_id}))


# ═══════════════════════════════════════════════════════════════════════════
# TEMPLATES (5 tools)
# ═══════════════════════════════════════════════════════════════════════════

@mcp.tool()
def list_templates() -> str:
    """List all SMS message templates."""
    return json.dumps(_api_post("/api/v2/templates"))


@mcp.tool()
def create_template(name: str, message: str) -> str:
    """Create a new message template. Variables: {firstname}, {lastname}, {email}, {phone_number}, {custom.X}.

    Args:
        name: Template name.
        message: Template body with optional variables.
    """
    return json.dumps(_api_post("/api/v2/templates/create", {
        "name": name, "message": message,
    }))


@mcp.tool()
def update_template(template_id: str, name: str = "", message: str = "") -> str:
    """Update a message template name and/or body.

    Args:
        template_id: Template ID.
        name: New name (leave empty to keep current).
        message: New message body.
    """
    data: dict[str, Any] = {"template_id": template_id}
    if name:
        data["name"] = name
    if message:
        data["message"] = message
    return json.dumps(_api_post("/api/v2/templates/update", data))


@mcp.tool()
def delete_template(template_id: str) -> str:
    """Delete a message template (soft delete)."""
    return json.dumps(_api_post("/api/v2/templates/delete", {"template_id": template_id}))


@mcp.tool()
def send_template(template_id: str, recipients: list[dict]) -> str:
    """Send a template to one or more recipients with personalized variables. Premium feature.

    Args:
        template_id: Template ID to send.
        recipients: List of recipients, each with phone_number and variables dict.
            Example: [{"phone_number": "+33612345678", "variables": {"firstname": "Marie"}}]
    """
    return json.dumps(_api_post("/api/v2/templates/send", {
        "template_id": template_id, "recipients": recipients,
    }))


# ═══════════════════════════════════════════════════════════════════════════
# STATS (2 tools)
# ═══════════════════════════════════════════════════════════════════════════

@mcp.tool()
def stats_overview(date_from: str = "", date_to: str = "") -> str:
    """Get account statistics overview: SMS sent/received/delivered, calls, clicks, contacts.

    Args:
        date_from: Start date (ISO 8601, e.g. 2026-01-01).
        date_to: End date.
    """
    return json.dumps(_api_post("/api/v2/stats/overview", {
        "date_from": date_from, "date_to": date_to,
    }))


@mcp.tool()
def stats_clicks(limit: int = 10) -> str:
    """Get link click tracking details.

    Args:
        limit: Max results (default 10).
    """
    return json.dumps(_api_post("/api/v2/stats/clicks", {"limit": limit}))


# ═══════════════════════════════════════════════════════════════════════════
# SENDING (3 tools)
# ═══════════════════════════════════════════════════════════════════════════

@mcp.tool()
def send_sms(
    phone_number: str,
    message: str,
    url: str = "",
    priority: int = 1,
) -> str:
    """Send an SMS to a single phone number. Premium feature.

    Args:
        phone_number: Recipient phone number (international or local format).
        message: SMS body. Use [link] for tracked URL.
        url: URL to track (used with [link] in message).
        priority: Sending priority (1 = normal).
    """
    return json.dumps(_api_post("/api/v2/sendsms", {
        "messages": [{
            "phone_number": phone_number,
            "message": message,
            "url": url,
            "priority": priority,
            "date_to_send": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }],
    }))


@mcp.tool()
def send_sms_batch(messages: list[dict]) -> str:
    """Send SMS to multiple recipients in a single batch. Premium feature.

    Args:
        messages: List of messages, each with phone_number, message, and optional url/priority.
            Example: [{"phone_number": "+33612345678", "message": "Hello!", "url": "", "priority": 1}]
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for m in messages:
        m.setdefault("priority", 1)
        m.setdefault("url", "")
        m.setdefault("date_to_send", now)
    return json.dumps(_api_post("/api/v2/sendsms", {"messages": messages}))


@mcp.tool()
def add_contacts(contacts: list[dict]) -> str:
    """Add or update contacts (upsert by phone number). Free feature.

    Args:
        contacts: List of contacts with phone_number (required), firstname, lastname, email, address.
            Example: [{"phone_number": "+33612345678", "firstname": "Jean", "lastname": "Dupont"}]
    """
    return json.dumps(_api_post("/api/v2/addcontacts", {"contacts": contacts}))


@mcp.tool()
def click_to_call(phone_number: str) -> str:
    """Initiate a click-to-call via the connected inSIM device. Premium feature.

    Args:
        phone_number: Phone number to call.
    """
    return json.dumps(_api_post("/api/v2/clictocall", {"phone_number": phone_number}))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    """Entry point for the insim-mcp command."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
