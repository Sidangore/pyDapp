import json
from web3 import HTTPProvider, Web3
from web3.contract import ConciseContract

#web3 instance
web3Instance = Web3(HTTPProvider("https://ropsten.infura.io/v3/1815651cbc7440fca737ecf87905dd31"))
# print (web3Instance.isConnected())

key = "0x33881bb46b880c1a1ead432fef1f04464597ee4ba1bfc36b5d798c8cd66897fc"
userAccount = web3Instance.eth.account.privateKeyToAccount(key)

#compile smart contract with truffle first
truffleFile = json.load(open('./build/contracts/Greeter.json'))
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']

contract = web3Instance.eth.contract(bytecode = bytecode, abi = abi)

# building the transaction 
contructTransaction = contract.constructor().buildTransaction({
    'from': userAccount.address,
    'nonce': web3Instance.eth.getTransactionCount(userAccount.address),
    'gas': 1728712,
    'gasPrice': web3Instance.toWei(21, 'gwei')
})

signed = userAccount.signTransaction(contructTransaction)
transactionHash = web3Instance.eth.sendRawTransaction(signed.rawTransaction)
print(transactionHash.hex())

transactionReceipt = web3Instance.eth.waitForTransactionReceipt(transactionHash)
print("contract deployed at: ", transactionReceipt['contractAddress'])