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
