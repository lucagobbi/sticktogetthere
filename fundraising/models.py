from django.db import models
from django.contrib.auth.models import User
from .utils import *


class Project(models.Model):

    admin = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=200, null=True)
    goal = models.FloatField(null=True, blank=True)
    deadline = models.DateTimeField(auto_now_add=False, auto_now=False)
    description = models.CharField(max_length=5000, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="projects_imgs/", default="")
    completed = models.BooleanField(default=False)
    address = models.CharField(max_length=42)

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

    # this function is called when a new project is created
    def deploy_contract(self):

        fundraising = web3.eth.contract(abi=abi, bytecode=bytecode)

        # project's parameter are passed in the constructor
        transaction = fundraising.constructor(
            int(self.goal), int(self.deadline.timestamp())
        ).buildTransaction(
            {
                "chainId": chain_Id,
                "from": my_address,
                "nonce": web3.eth.getTransactionCount(my_address),
            }
        )

        signed_tx = web3.eth.account.sign_transaction(
            transaction, private_key=private_key
        )
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        contractAddress = tx_receipt.contractAddress

        # everytime a new contract is created this assign to the DB the related address
        self.address = contractAddress
        self.save()


class Request(models.Model):

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="requests"
    )
    description = models.CharField(max_length=2000, null=True)
    value = models.FloatField(null=True, blank=True)
    addressTo = models.CharField(max_length=42)
    completed = models.BooleanField(default=False)
    numberOfVoters = models.IntegerField(default=0)

    def __str__(self):
        return self.description

    # getting request index for a specific contract
    def getRequestNo(self):
        project = self.project
        requests = Request.objects.filter(project=project.id)

        x = 0

        for request in requests:
            x += 1

            if request == self:
                break

        # index starts from 0 in our contract
        requestNo = x - 1

        return requestNo

    def createRequest(self, _description, _recipient, _value):

        address = self.project.address
        project_contract = web3.eth.contract(abi=abi, address=address)
        # value passed during the ModelForm creation are the parameters of the function createRequest in the contract
        transaction = project_contract.functions.createRequest(
            _description, _recipient, _value
        ).buildTransaction(
            {
                "chainId": chain_Id,
                "from": my_address,
                "nonce": web3.eth.getTransactionCount(my_address),
            }
        )
        signed_tx = web3.eth.account.sign_transaction(
            transaction, private_key=private_key
        )
        web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # each request has a related sendPayment function callable only by admin when consensus is reached
    def sendPayment(self):

        requestNo = self.getRequestNo()
        address = self.project.address
        project_contract = web3.eth.contract(abi=abi, address=address)
        transaction = project_contract.functions.makePayment(
            requestNo
        ).buildTransaction(
            {
                "chainId": chain_Id,
                "from": my_address,
                "nonce": web3.eth.getTransactionCount(my_address),
            }
        )
        signed_tx = web3.eth.account.sign_transaction(
            transaction, private_key=private_key
        )
        web3.eth.send_raw_transaction(signed_tx.rawTransaction)
