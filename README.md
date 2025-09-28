# MoMo Transactions API

This project implements a REST API for mobile money SMS transactions. It includes:

- XML parsing to extract transaction data
- A REST API with CRUD operations
- Basic authentication for security
- Data structure & algorithm (DSA) comparison for search efficiency

---

## Repository Structure

```

MoMo_SMS/
│
├─ api/
│   └─ server.py        # REST API with CRUD endpoints and Basic Auth
│
├─ docs/
│   └─ api_docs.md      # API documentation
│
├─ dsa/
│   └─ parse_dsa.py     # XML parsing and DSA comparison code
│
├─ screenshots/         # Screenshots of API test cases
└─ README.md            # Setup instructions

````
## THE REPORT PDF FILE
[report.pdf](https://github.com/user-attachments/files/22585723/report.pdf)

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd <repository-folder>
````

2. **Install Python (if not installed)**

* Python 3.8 or above is recommended.

3. **Run the API server**

```bash
cd api
python server.py
```

The server will start at:

```
http://localhost:8000/
```

---

## Authentication

All endpoints require **Basic Authentication**:

* Username: `admin`
* Password: `password`

---

## How to Test the API

You can use **Postman**, **curl**, or any HTTP client.

**Example using curl:**

* GET all transactions:

```bash
curl -u admin:password http://localhost:8000/transactions
```

* GET single transaction by ID:

```bash
curl -u admin:password http://localhost:8000/transactions/1
```

* POST a new transaction:

```bash
curl -u admin:password -X POST -H "Content-Type: application/json" -d '{"transaction_type":"received","amount":"3000","sender":"Alice Doe","receiver":null,"timestamp":"2025-09-28 12:00","raw_body":"You have received 3,000 RWF from Alice Doe"}' http://localhost:8000/transactions
```

* PUT (update) a transaction:

```bash
curl -u admin:password -X PUT -H "Content-Type: application/json" -d '{"transaction_type":"sent","amount":"2500","sender":null,"receiver":"Bob Smith","timestamp":"2025-09-28 13:00","raw_body":"Payment of 2,500 RWF to Bob Smith"}' http://localhost:8000/transactions/2
```

* DELETE a transaction:

```bash
curl -u admin:password -X DELETE http://localhost:8000/transactions/2
```

---

## Notes

* The API stores data in memory; changes will be lost after the server is stopped.
* The DSA comparison is implemented in `dsa/parse_dsa.py`.
* Basic Authentication is used for simplicity; for production environments, consider **JWT** or **OAuth2**.

```

---

This README covers:

- Project overview  
- Repository structure  
- Setup and running instructions  
- Authentication info  
- How to test the API  



