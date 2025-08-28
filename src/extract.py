import requests
import json
import time
from datetime import datetime

def get_latest_block():
    """Get the latest block hash"""
    try:
        response = requests.get('https://blockchain.info/latestblock')
        return response.json()['hash']
    except:
        print("Error getting latest block")
        return None

def get_block_data(block_hash):
    """Get block data by hash"""
    try:
        url = f'https://blockchain.info/rawblock/{block_hash}'
        response = requests.get(url)
        return response.json()
    except:
        print(f"Error getting block data for {block_hash}")
        return None

def process_transaction(tx):
    """Process transaction data"""
    hash_transaction = tx['hash']
    tx_time = tx.get('time', None)
    # Convert epoch to datetime string
    time_dt = datetime.utcfromtimestamp(tx_time).strftime('%Y-%m-%d %H:%M:%S') if tx_time else None

    # Calculate input
    inputs = tx.get('inputs', [])
    indegree = len(inputs)

    in_btc_list = []
    senders = []
    for inp in inputs:
        if 'prev_out' in inp and inp['prev_out']:
            btc_value = inp['prev_out']['value'] / 100000000  # Satoshi to BTC
            in_btc_list.append(btc_value)
            addr = inp['prev_out'].get('addr')
            if addr:
                senders.append(addr)

    # Calculate output
    outputs = tx.get('out', [])
    outdegree = len(outputs)
    out_btc_list = []
    receivers = []
    for out in outputs:
        btc_value = out['value'] / 100000000  # Satoshi to BTC
        out_btc_list.append(btc_value)
        addr = out.get('addr')
        if addr:
            receivers.append(addr)

    # Statistics
    total_in = sum(in_btc_list)
    total_out = sum(out_btc_list)
    mean_in_btc = total_in / len(in_btc_list) if in_btc_list else 0.0
    mean_out_btc = total_out / len(out_btc_list) if out_btc_list else 0.0

    return {
        'hash_transaction': hash_transaction,
        'time': time_dt,
        'indegree': indegree,
        'outdegree': outdegree,
        'in_btc': in_btc_list,
        'out_btc': out_btc_list,
        'total_in': total_in,
        'total_out': total_out,
        'mean_in_btc': mean_in_btc,
        'mean_out_btc': mean_out_btc,
        'senders': senders,
        'receivers': receivers
    }

def main():
    print("Fetching Bitcoin transactions from last 5 blocks...")

    latest_block_hash = get_latest_block()
    if not latest_block_hash:
        return

    block_hash = latest_block_hash
    results = []
    num_blocks = 5

    for i in range(num_blocks):
        block_data = get_block_data(block_hash)
        if not block_data:
            break

        transactions = block_data.get('tx', [])[:200]  # Limit to first 100 transactions
        for tx in transactions:
            result = process_transaction(tx)
            results.append(result)
            time.sleep(0.1)  # Rate limiting

        # Get previous block hash
        block_hash = block_data.get('prev_block')
        if not block_hash:
            break

    # Save to JSON file
    with open('../data/data.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"Total transactions processed: {len(results)}")

if __name__ == "__main__":
    main()