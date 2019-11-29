# Reference
# - https://ethereum.stackexchange.com/questions/44614/how-to-connect-to-infura-and-deploy-contract-use-web3-py
# - https://medium.com/@w_n1c01a5/hello-world-on-solidity-ethereum-b6a4de6a4258
import time
import sys
from web3 import Web3, HTTPProvider
from solc import compile_source

# ABI for parsing contract
contract_source_code = '''pragma solidity ^0.4.22;

contract helloworld {
 function helloWorld () public pure returns (string) {
   return 'Hello world';
 }
}'''
compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol['<stdin>:helloworld']

# The url for node connecting to Ropsten testnet (the chain), you may apply it at https://infura.io/
w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/ID_FROM_INFURA"))

# Private key of wallet on testnet
wallet_private_key = "YOUR_WALLET_PRIVATE_KEY"

# Address of wallet on testnet
wallet_address     = "YOUR_WALLET_ADDRESS"
nonce = w3.eth.getTransactionCount(wallet_address)

# New contract
contract_ = w3.eth.contract(
    abi=contract_interface['abi'],
    bytecode=contract_interface['bin'])

# Prepare your account
acct = w3.eth.account.privateKeyToAccount(wallet_private_key)

# Prepare transaction (i.e. deploying the contract)
construct_txn = contract_.constructor().buildTransaction({
    'from': acct.address,
    'nonce': nonce,
    'gas': 2000000,
    'gasPrice': w3.toWei('40', 'gwei'),
    'chainId': 3
    })

# Sign & send the contract
signed = acct.signTransaction(construct_txn)
txn_hash = w3.eth.sendRawTransaction(signed.rawTransaction)

# Wait for result
txn_receipt = None
count = 0
while txn_receipt is None and (count < 30):
    try:
        txn_receipt = w3.eth.getTransactionReceipt(txn_hash)
        print(txn_receipt)
    except:
        print('Waiting for transaction to be approved ... ({})'.format(count),end='\r')
        count+=1
        time.sleep(5)
if txn_receipt is None:
    print('Failed.')
else:
    print('Done.')
