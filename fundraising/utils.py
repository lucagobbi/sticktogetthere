from web3 import Web3
from solcx import compile_standard
import json

# setting the provider

provider = "HTTP://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(provider))
chain_Id = 1337

# public and prvate key for admin

my_address = "0x2678EB36651Eeee579c2F1805aF5D01519a415d0"
private_key = "f5e98a9b94be4bc76c019d12ae227e35afdc9eb6dc4e59fbeac77514ae23c239"
nonce = web3.eth.getTransactionCount(my_address)

# compiling the contract to extract bytecode and abi - this is running only at launch

with open(
    "sticktogether\\fundraising\\contracts\\Fundraising.sol",
    "r",
) as file:
    fundraising_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"Fundraising.sol": {"content": fundraising_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol["contracts"]["Fundraising.sol"]["Fundraising"]["evm"][
    "bytecode"
]["object"]

abi = compiled_sol["contracts"]["Fundraising.sol"]["Fundraising"]["abi"]


def getBalance(contractAddress):

    address = contractAddress
    project_contract = web3.eth.contract(abi=abi, address=address)
    balance = project_contract.functions.getBalance().call()
    return balance


def getNumberOfContributors(contractAddress):

    address = contractAddress
    project_contract = web3.eth.contract(abi=abi, address=address)
    numberOfContributors = project_contract.functions.numberOfContributors().call()
    return numberOfContributors


def getNumberOfVoters(contractAddress, requestNo):

    address = contractAddress
    project_contract = web3.eth.contract(abi=abi, address=address)
    NumberOfVoters = project_contract.functions.getRequestInfo(requestNo).call()
    return NumberOfVoters[4]
