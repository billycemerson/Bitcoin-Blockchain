import json
import math
from datetime import datetime
from collections import Counter

def shannon_entropy(addresses):
    """Calculate Shannon entropy for a list of addresses"""
    if not addresses:
        return 0.0
    freq = Counter(addresses)
    total = len(addresses)
    entropy = -sum((count/total) * math.log2(count/total) for count in freq.values())
    return entropy

def enrich_transactions(transactions):
    """Add additional features to transaction data"""
    enriched = []

    for tx in transactions:
        # Get basic transaction data
        total_in = tx.get('total_in', 0)
        total_out = tx.get('total_out', 0)
        senders = tx.get('senders', [])
        receivers = tx.get('receivers', [])

        # Add new features
        fee_btc = total_in - total_out
        unique_senders = len(set(senders))
        unique_receivers = len(set(receivers))
        is_self_churn = unique_senders == 1 and unique_receivers == 1 and senders[0] == receivers[0]
        sender_entropy = shannon_entropy(senders)
        receiver_entropy = shannon_entropy(receivers)

        # Convert time to datetime object and extract hour and day of week
        try:
            dt = datetime.strptime(tx['time'], "%Y-%m-%d %H:%M:%S")
            hour = dt.hour
            day_of_week = dt.strftime('%A')  # e.g., 'Tuesday'
        except Exception as e:
            hour = None
            day_of_week = None

        # Join to dict
        tx_enriched = {
            **tx,
            'fee_btc': round(fee_btc, 8),
            'unique_senders': unique_senders,
            'unique_receivers': unique_receivers,
            'is_self_churn': is_self_churn,
            'sender_entropy': round(sender_entropy, 4),
            'receiver_entropy': round(receiver_entropy, 4),
            'hour': hour,
            'day_of_week': day_of_week
        }

        enriched.append(tx_enriched)

    return enriched

# Load data extracted from previous step
with open('../data/data.json') as f:
    transactions = json.load(f)

# Transform data by enriching with additional features
enriched_data = enrich_transactions(transactions)

# Save enriched data to a new JSON file
with open('../data/data_transform.json', 'w') as f:
    json.dump(enriched_data, f, indent=2)

print("Done enriching data with additional features.")