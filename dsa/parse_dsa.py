import xml.etree.ElementTree as ET
import re
import time


# Parse XML

# Load XML file
tree = ET.parse("modified_sms_v2.xml")
root = tree.getroot()

# store of transactions
transactions_list = []
transactions_dict = {}

for idx, record in enumerate(root.findall("sms"), start=1):
    body = record.get("body")
    
    transaction_type = None
    amount = None
    sender = None
    receiver = None

    # Detect transaction type and extract details
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


# Task 5: DSA Comparison

# Linear search function
def linear_search(t_list, tid):
    start = time.time()
    for t in t_list:
        if t["id"] == tid:
            end = time.time()
            return t, end - start
    return None, None

# Dictionary lookup function
def dict_lookup(t_dict, tid):
    start = time.time()
    result = t_dict.get(tid)
    end = time.time()
    return result, end - start


# Example usage and timing

example_id = 10  # i can test with any transaction ID

result_list, time_list = linear_search(transactions_list, example_id)
result_dict, time_dict = dict_lookup(transactions_dict, example_id)

print(f"Searching for transaction ID {example_id}:")
print("Linear search result:", result_list)
print(f"Linear search time: {time_list*1000:.6f} ms")

print("Dictionary lookup result:", result_dict)
print(f"Dictionary lookup time: {time_dict*1000:.6f} ms")


# Optional: Compare multiple IDs

for test_id in range(1, min(21, len(transactions_list)+1)):  # first 20 IDs
    _, t_lin = linear_search(transactions_list, test_id)
    _, t_dict = dict_lookup(transactions_dict, test_id)
    print(f"ID {test_id}: Linear {t_lin*1000:.6f} ms, Dict {t_dict*1000:.6f} ms")

