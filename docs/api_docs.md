# MoMo Transactions API Documentation

This document describes the REST API endpoints for accessing and managing mobile money SMS transactions.

---

## Authentication

All endpoints require **Basic Authentication**:

- Username: `admin`
- Password: `password`

Unauthorized requests return:

```json
{
  "error": "Unauthorized"
}

## GET /transactions
- Description: List all transactions
- Request Example:
  GET /transactions
  Authorization: Basic <username:password>
- Response Example:
[
  {
    "id": 1,
    "transaction_type": "received",
    "amount": "5000",
    "sender": "John Doe",
    "receiver": null,
    "timestamp": "2025-09-28 10:00",
    "raw_body": "You have received 5,000 RWF from John Doe..."
  },
  ...
]
- Error Codes:
  401 Unauthorized: Invalid credentials
  404 Not Found: Endpoint does not exist
