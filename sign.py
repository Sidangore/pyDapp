import json
from web3 import HTTPProvider, Web3
from web3.contract import ConciseContract

# compile the smart contract with the truffle first 
truffleFile = json.load(open('./build/contracts/Greeter.json'))
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']

# create a web3 instance to interact with the contract
web3Instance = Web3(HTTPProvider("https://ropsten.infura.io/v3/1815651cbc7440fca737ecf87905dd31"))
# print(web3Instance.isConnected())
contractAddress = web3Instance.toChecksumAddress("0xB5093a27aA6722E34040aE6f02d1D4632364429F")
key = "0x33881bb46b880c1a1ead432fef1f04464597ee4ba1bfc36b5d798c8cd66897fc"
userAccount = web3Instance.eth.account.privateKeyToAccount(key)
accountAddress = userAccount.address

#instantiate and deploy the contract
contract = web3Instance.eth.contract(abi = abi, bytecode = bytecode)

#contract instance
contractInstance = web3Instance.eth.contract(abi = abi, address = contractAddress)

# create the transaction
tx = contractInstance.functions.greet("good afternoon pune").buildTransaction({
    'nonce': web3Instance.eth.getTransactionCount(accountAddress)
})

signed_tx = web3Instance.eth.account.signTransaction(tx, key)
hash = web3Instance.eth.sendRawTransaction(signed_tx.rawTransaction)

print(hash.hex())