# linkedin-sdk

Python SDK for the LinkedIn API v202510.

## Installation

```bash
pip install ldraney-linkedin-sdk
```

## Quick Start

```python
from linkedin_sdk import LinkedInClient

# Reads LINKEDIN_ACCESS_TOKEN and LINKEDIN_PERSON_ID from env
client = LinkedInClient()

# Create a text post
result = client.create_post("Hello from Python!")
print(result)  # {'postUrn': 'urn:li:share:...', 'statusCode': 201}

# Get user info
info = client.get_user_info()
print(info['name'])

# Delete a post
client.delete_post("urn:li:share:7...")
```

## Authentication

Set environment variables:

```bash
export LINKEDIN_ACCESS_TOKEN="your_token"
export LINKEDIN_PERSON_ID="your_person_id"
```

Or pass directly:

```python
client = LinkedInClient(access_token="...", person_id="...")
```

## OAuth

```python
from linkedin_sdk import LinkedInClient

# Build auth URL (no client needed)
url = LinkedInClient.get_auth_url(
    client_id="...",
    redirect_uri="http://localhost:8080/callback",
    scopes=["openid", "profile", "email", "w_member_social"],
)

# Exchange code for token (classmethod)
token = LinkedInClient.exchange_code(
    code="auth_code",
    client_id="...",
    client_secret="...",
    redirect_uri="http://localhost:8080/callback",
)

# Refresh token
new_token = LinkedInClient.refresh_token(
    refresh_token="...",
    client_id="...",
    client_secret="...",
)
```

## License

MIT
