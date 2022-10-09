from solcx import compile_standard, install_solc
import json
import solcx
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

install_solc("0.6.0")
# compiling solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = os.getenv("PRIVATE_KEY")

# create a contract with python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)

# build a transaction
# sign a transaction
# send a transaction

transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
# signing the transaction

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# send the signed transaction

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# working with contract
# contract address
# contract abi

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# call -> simulate making the call and getting a return a value
# transact -> actually making a state change

# initial value of favorite number

# print(simple_storage.functions.store(15).call())
# print(simple_storage.functions.retrieve().call())

store_transaction = simple_storage.functions.store(15).build_transaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
    }
)

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

send_store_txn = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_txn)
print(simple_storage.functions.retrieve().call())
