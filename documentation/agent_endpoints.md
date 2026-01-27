# Agent Endpoints Documentation

**Base URL:** `/admin/agents`  
**Authentication:** Bearer token (Admin only)  
**Header:** `Authorization: Bearer <token>`

---

## 1. Get All Agents

**Endpoint:** `GET /admin/agents`

**Request:**
- No body required
- Headers: `Authorization: Bearer <admin_token>`

**Response:** `200 OK`
```json
[
  {
    "id": "uuid-string",
    "email": "sample1@gmail.com",
    "name": "Albert",
    "is_active": true,
    "created_at": "2026-01-27T19:00:00Z",
    "updated_at": "2026-01-27T19:00:00Z"
  }
]
```

---

## 2. Create Agent

**Endpoint:** `POST /admin/agents`

**Request Body:**
```json
{
  "email": "newagent@gmail.com",
  "name": "Agent Name"
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid-string",
  "email": "newagent@gmail.com",
  "name": "Agent Name",
  "is_active": true,
  "created_at": "2026-01-27T19:00:00Z",
  "updated_at": "2026-01-27T19:00:00Z"
}
```

**Error:** `400 Bad Request`
```json
{
  "detail": "Agent with this email already exists or creation failed"
}
```

---

## 3. Update Agent

**Endpoint:** `PUT /admin/agents/{agent_id}`

**Path Parameter:**
- `agent_id`: string (UUID)

**Request Body:**
```json
{
  "email": "updated@gmail.com",
  "name": "Updated Name"
}
```
*Note: Both fields are optional - send only fields to update*

**Response:** `200 OK`
```json
{
  "id": "uuid-string",
  "email": "updated@gmail.com",
  "name": "Updated Name",
  "is_active": true,
  "created_at": "2026-01-27T19:00:00Z",
  "updated_at": "2026-01-27T19:05:00Z"
}
```

**Error:** `404 Not Found`
```json
{
  "detail": "Agent not found, email already exists, or update failed"
}
```

---

## Data Models

**AgentResponse:**
- `id`: string (UUID, auto-generated)
- `email`: string (required, unique)
- `name`: string (optional)
- `is_active`: boolean (default: true)
- `created_at`: datetime (auto-generated)
- `updated_at`: datetime (auto-updated)

**AgentCreate:**
- `email`: string (required, valid email format)
- `name`: string (optional)

**AgentUpdate:**
- `email`: string (optional, valid email format)
- `name`: string (optional)
