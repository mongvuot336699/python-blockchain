from solcx import compile_standard , install_solc
from web3 import Web3
import os 
import json

install_solc("0.8.0")

with open("./Box.sol", "r") as file:
    simple_storage_file = file.read()

# Compile Our Solidity

compile_sol = compile_standard(
    {
        "language":"Solidity",
        "sources": {"Box.sol": {"content":simple_storage_file}},
        "settings": {
            "outputSelection":{
                "*": {"*":["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compile_sol,file)

# get bytecode 
bytecode = compile_sol["contracts"]["Box.sol"]["Box"]["evm"]["bytecode"]["object"]
# get abi 
abi = compile_sol["contracts"]["Box.sol"]["Box"]["abi"]

# for connecting to ganache 
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
chain_id = 1337
my_address = "0xD38d48995d14BE339bB05bdb6beE6013c0202d65"
private_key = os.getenv(PRIVATE_KEY)
# private_key = "0f1c81799eb38325c5d80eda7cff5f6bb7e06e25c2bf104e086180a14f55894d"

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latetest transaction
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)