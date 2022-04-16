from solcx import compile_standard, install_solc
from web3 import Web3
import os

# from dotenv import load_dotenv
import json

# load_dotenv()
install_solc("0.8.0")

with open("./Box.sol", "r") as file:
    simple_storage_file = file.read()

# Compile Our Solidity

compile_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"Box.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compile_sol, file)

# get bytecode
bytecode = compile_sol["contracts"]["Box.sol"]["Box"]["evm"]["bytecode"]["object"]
# get abi
abi = compile_sol["contracts"]["Box.sol"]["Box"]["abi"]

# for connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_address = "0xE05FAe7f6eD53ebaE0ede326564bA5491a5e490f"
# private_key = os.getenv(PRIVATE_KEY)
# test_dotenv = os.getenv(HELLO)
private_key = "1244a7f4b76498ba1b9260413686bd7036bbaf8bc7f31ac4a0cd62277bb3a971"

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latetest transaction
nonce = w3.eth.getTransactionCount(my_address)
# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
# print(transaction)
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying contract ......")
# Send this sidned transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("DEPLOY !!!!")
# Working with Contract, u need
# Contract ABI
# Contract Address
simple_storage = w3.eth.contract(abi=abi, address=tx_receipt.contractAddress)
# Call -> Simulate making the call and getting a return value
# Transact -> Acually make a state change
print(simple_storage.functions.retrieve().call())

store_transaction = simple_storage.functions.store(100).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_store = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
print("Updating contract .....")
store_hash = w3.eth.send_raw_transaction(signed_store.rawTransaction)
store_receipt = w3.eth.wait_for_transaction_receipt(store_hash)
print("UPDATE !!!!")
print(simple_storage.functions.retrieve().call())
