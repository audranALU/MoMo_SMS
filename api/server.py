import xml.etree.ElementTree as ET
import re
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import base64


# Load and parse XML
tree = ET.parse("../dsa/modified_sms_v2.xml")  # adjust path if needed
root = tree.getroot()

transactions_list = []
transactions_dict = {}

for idx, record in enumerate(root.findall("sms"), start=1):
    body = record.get("body")
    transaction_type = None
    amount = None
    sender = None
    receiver = None

    if "received" in body.lower():
        transaction_type = "received"
        match = re.search(r"received\s+([\d,]+)\s*RWF\s+from\s+(.+?)\s+\(", body)
        if match:
            amount = match.group(1).replace(",", "")
            sender = match.group(2).strip()
    elif "payment" in body.lower():
        transaction_type = "sent"
        match = re.search(r"payment of\s+([\d,]+)\s*RWF\s+to\s+(.+?)\s+\d+", body)
        if match:
            amount = match.group(1).replace(",", "")
            receiver = match.group(2).strip()

    transaction = {
        "id": idx,
        "transaction_type": transaction_type,
        "amount": amount,
        "sender": sender,
        "receiver": receiver,
        "timestamp": record.get("readable_date"),
        "raw_body": body
    }

    transactions_list.append(transaction)
    transactions_dict[idx] = transaction

# Basic Authentication
USERNAME = "admin"
PASSWORD = "password"

class MoMoAPIHandler(BaseHTTPRequestHandler):
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="MoMoAPI"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def authenticate(self):
        auth_header = self.headers.get('Authorization')
        if auth_header is None or not auth_header.startswith('Basic '):
            self.do_AUTHHEAD()
            return False
        encoded = auth_header.split(' ')[1]
        decoded = base64.b64decode(encoded).decode()
        user, pwd = decoded.split(":")
        if user == USERNAME and pwd == PASSWORD:
            return True
        else:
            self.do_AUTHHEAD()
            return False

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    # ------------------------
    # CRUD Endpoints
    # ------------------------
    def do_GET(self):
        if not self.authenticate():
            return

        if self.path == "/transactions":
            self.send_json(transactions_list)
        elif self.path.startswith("/transactions/"):
            try:
                tid = int(self.path.split("/")[-1])
                transaction = transactions_dict.get(tid)
                if transaction:
                    self.send_json(transaction)
                else:
                    self.send_json({"error": "Transaction not found"}, status=404)
            except ValueError:
                self.send_json({"error": "Invalid ID"}, status=400)
        else:
            self.send_json({"error": "Endpoint not found"}, status=404)

    def do_POST(self):
        if not self.authenticate():
            return

        if self.path != "/transactions":
            self.send_json({"error": "Endpoint not found"}, status=404)
            return

        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length)
        try:
            data = json.loads(post_data)
            new_id = max(transactions_dict.keys()) + 1
            data["id"] = new_id
            transactions_list.append(data)
            transactions_dict[new_id] = data
            self.send_json(data, status=201)
        except:
            self.send_json({"error": "Invalid data"}, status=400)

    def do_PUT(self):
        if not self.authenticate():
            return

        if not self.path.startswith("/transactions/"):
            self.send_json({"error": "Endpoint not found"}, status=404)
            return

        try:
            tid = int(self.path.split("/")[-1])
        except ValueError:
            self.send_json({"error": "Invalid ID"}, status=400)
            return

        length = int(self.headers['Content-Length'])
        put_data = self.rfile.read(length)
        try:
            data = json.loads(put_data)
            if tid in transactions_dict:
                data["id"] = tid
                for i, t in enumerate(transactions_list):
                    if t["id"] == tid:
                        transactions_list[i] = data
                        break
                transactions_dict[tid] = data
                self.send_json(data)
            else:
                self.send_json({"error": "Transaction not found"}, status=404)
        except:
            self.send_json({"error": "Invalid data"}, status=400)

    def do_DELETE(self):
        if not self.authenticate():
            return

        if not self.path.startswith("/transactions/"):
            self.send_json({"error": "Endpoint not found"}, status=404)
            return

        try:
            tid = int(self.path.split("/")[-1])
            if tid in transactions_dict:
                transactions_list[:] = [t for t in transactions_list if t["id"] != tid]
                del transactions_dict[tid]
                self.send_json({"message": "Deleted"})
            else:
                self.send_json({"error": "Transaction not found"}, status=404)
        except ValueError:
            self.send_json({"error": "Invalid ID"}, status=400)

# ------------------------
# Run Server
# ------------------------
if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MoMoAPIHandler)
    print("Server running at http://localhost:8000/")
    httpd.serve_forever()

