# Install required packages
!pip install tronpy mnemonic

import time
import tronpy
from tronpy.keys import PrivateKey
from mnemonic import Mnemonic

# Initialize the Tron network client
client = tronpy.Tron()

# Initialize the Mnemonic generator
mnemo = Mnemonic('english')

# File to store results
result_file = 'result.txt'

def generate_wallet():
    # Generate a random seed phrase
    seed_phrase = mnemo.generate(strength=256)
    # Generate a private key from the seed phrase
    private_key = PrivateKey.from_mnemonic(seed_phrase)
    # Generate the corresponding wallet address
    address = private_key.public_key.to_base58check_address()

    return {
        'seed_phrase': seed_phrase,
        'private_key': private_key.hex(),
        'address': address
    }

def check_balance(address):
    # Check balance of the wallet address
    balance = client.get_account_balance(address)
    return balance

def log_wallet(wallet_info, balance):
    # Log wallet info to a file
    with open(result_file, 'a') as f:
        f.write(f"Address: {wallet_info['address']}\n")
        f.write(f"Mnemonic: {wallet_info['seed_phrase']}\n")
        f.write(f"Private Key: {wallet_info['private_key']}\n")
        f.write(f"Balance: {balance} TRX\n")
        f.write(f"{'-'*30}\n")
    print(f"Wallet with balance found and logged: {wallet_info['address']}")

def main():
    while True:
        wallet_info = generate_wallet()
        balance = check_balance(wallet_info['address'])
        print(f"Checking wallet {wallet_info['address']} with balance {balance} TRX")

        if balance > 0:
            log_wallet(wallet_info, balance)

        # Wait before generating the next wallet to avoid being rate-limited
        time.sleep(1)

if __name__ == "__main__":
    main()
