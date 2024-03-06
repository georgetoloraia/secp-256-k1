from bitcoinrpc.authproxy import AuthServiceProxy

# Connect to your Bitcoin node
rpc_connection = AuthServiceProxy("http://username:password@127.0.0.1:8332")

# Define function to extract addresses from transactions
def extract_addresses(transaction):
    addresses = []
    for output in transaction['vout']:
        addresses.append(output['scriptPubKey']['addresses'][0])
    return addresses

# Iterate through blocks
for block_height in range(200001):  # Iterate from block 0 to block 200000
    block_hash = rpc_connection.getblockhash(block_height)
    block = rpc_connection.getblock(block_hash)

    # Extract transactions from the block
    for txid in block['tx']:
        transaction = rpc_connection.getrawtransaction(txid, True)
        
        # Extract addresses from transaction outputs
        addresses = extract_addresses(transaction)
        
        # Store the addresses or perform further processing
        for address in addresses:
            # Store or process the address as needed
            print(address)
