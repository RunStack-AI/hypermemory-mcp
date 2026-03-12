# Memory Key Naming Conventions

Good key naming makes your memories easy to find and understand. This guide shows you the best practices.

## The Basics

Keys are unique identifiers for each memory. Think of them like file names for your information.

### Rules

1. **Use lowercase letters** - `user_preference` not `User_Preference`
2. **Separate words with underscores** - `project_deadline` not `projectdeadline`
3. **Be descriptive** - `customer_support_john` not `c1`
4. **Keep it short but clear** - `user_email` not `the_email_address_of_the_user`

## Common Patterns

### User Information

```
user_{attribute}
user_{user_id}_{attribute}
```

Examples:
- `user_name` - The user's name
- `user_preferences` - User's general preferences
- `user_john_email` - John's email address
- `user_123_settings` - Settings for user ID 123

### Project Information

```
project_{project_name}
project_{project_name}_{attribute}
```

Examples:
- `project_alpha` - Main info about Project Alpha
- `project_alpha_deadline` - Project Alpha's deadline
- `project_alpha_team` - Team members on Project Alpha
- `project_website_redesign_budget` - Budget for website redesign

### Customer Data

```
customer_{identifier}
customer_{identifier}_{attribute}
```

Examples:
- `customer_acme_corp` - Acme Corp's profile
- `customer_acme_corp_contacts` - Contact list for Acme
- `customer_12345_preferences` - Preferences for customer #12345

### Configuration & Settings

```
config_{what}
setting_{what}
```

Examples:
- `config_api_rate_limit` - API rate limit setting
- `setting_notification_frequency` - How often to send notifications
- `config_default_language` - Default language setting

### Events & Actions

```
event_{event_type}_{date_or_id}
action_{action_type}_{date_or_id}
```

Examples:
- `event_meeting_2024_03_15` - Meeting on March 15, 2024
- `action_deployment_v2_release` - v2 release deployment
- `event_quarterly_review_q1_2024` - Q1 2024 review

### Categories & Collections

```
{category}_overview
{category}_list
```

Examples:
- `projects_overview` - Overview of all projects
- `customers_vip_list` - List of VIP customers
- `tasks_urgent` - Urgent tasks

## Good vs Bad Examples

| ❌ Bad | ✅ Good | Why |
|--------|---------|-----|
| `stuff` | `user_notes` | Specific and searchable |
| `data1` | `customer_order_history` | Descriptive |
| `JohnPrefs` | `user_john_preferences` | Consistent format |
| `the-project` | `project_main` | Uses underscores |
| `X` | `config_max_retries` | Self-documenting |
| `info` | `company_about` | Clear purpose |

## Organizing Related Information

Use consistent prefixes to group related memories:

```
# Research on renewable energy
research_renewable_overview
research_renewable_solar
research_renewable_wind
research_renewable_costs

# Customer journey for Acme Corp
customer_acme_first_contact
customer_acme_requirements
customer_acme_proposal
customer_acme_contract
```

This makes it easy to find all related information with a search like "research_renewable" or "customer_acme".

## Tips for Teams

### Agree on Prefixes

Create a list of standard prefixes for your organization:

| Prefix | Use For |
|--------|---------|
| `user_` | User information |
| `project_` | Project data |
| `customer_` | Customer data |
| `config_` | Configuration |
| `task_` | Tasks and todos |
| `note_` | General notes |
| `event_` | Events and meetings |

### Document Your Conventions

Keep a shared document with your naming rules so everyone follows the same pattern.

### Be Consistent

Once you choose a pattern, stick with it. Inconsistent naming makes information hard to find:

```
# Inconsistent - hard to search
customer_data_acme
acme_customer
acme_corp_info

# Consistent - easy to search
customer_acme_profile
customer_acme_contacts
customer_acme_history
```

## What to Avoid

1. **Generic names** - `data`, `info`, `stuff`, `thing`
2. **Abbreviations only you understand** - `proj_x_req_v2` 
3. **Special characters** - `project@home`, `user#1`
4. **Spaces** - `my project` (use `my_project`)
5. **Numbers at the start** - `123_customer` (use `customer_123`)

## Quick Reference

```
Pattern                          Example
─────────────────────────────────────────────────
user_{attribute}                 user_email
user_{id}_{attribute}            user_42_preferences
project_{name}                   project_alpha
project_{name}_{attribute}       project_alpha_deadline
customer_{name}                  customer_acme
customer_{name}_{attribute}      customer_acme_contacts
config_{setting}                 config_timezone
event_{type}_{date}              event_meeting_2024_03_15
{category}_overview              projects_overview
{category}_list                  tasks_urgent_list
```

---

Need help? [Open an issue](https://github.com/RunStack-AI/hypermemory-mcp/issues)
