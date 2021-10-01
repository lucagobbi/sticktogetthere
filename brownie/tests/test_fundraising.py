from brownie import Fundraising, accounts


# deployment test
def test_deploy():
    admin = accounts[0]
    # test the deployment of a new contract goal = 1 ETH deadline = 1 week
    fundraising = Fundraising.deploy(1000000000000000000, 604800, {"from": admin})
    # assert that this contract is a new one with a balance equal to zero
    expected = 0
    raised_amount = fundraising.raisedAmount()
    assert raised_amount == expected


# contribution test
def test_contribute():
    admin = accounts[0]
    contributor = accounts[1]
    # creating the contract
    fundraising = Fundraising.deploy(1000000000000000000, 604800, {"from": admin})
    # after the deploment a new user called contributor is sending 0.1 ETH to the contract
    fundraising.contribute({"from": contributor, "value": 100000000000000000})
    expected = 100000000000000000
    raised_amount = fundraising.raisedAmount()
    assert expected == raised_amount


# request creation test
def test_createRequest():
    admin = accounts[0]
    recipient = accounts[1]
    fundraising = Fundraising.deploy(1000000000000000000, 604800, {"from": admin})
    # the administrator is creating a request with title "request" to send ETH to "recipient" for a value of 0.1 ETH
    fundraising.createRequest("request", recipient, 100000000000000000, {"from": admin})
    # if the request has been created the parameter completed must be false
    expected = False
    completed = fundraising.getRequestInfo(0)[3]
    assert expected == completed


# voting test
def test_voteRequest():
    admin = accounts[0]
    contributor = accounts[1]
    recipient = accounts[2]
    fundraising = Fundraising.deploy(1000000000000000000, 604800, {"from": admin})
    # the administrator is creating a request
    fundraising.createRequest("request", recipient, 100000000000000000, {"from": admin})
    # contribution is required to vote a request
    fundraising.contribute({"from": contributor, "value": 100000000000000000})
    # now the contributor is allowed to vote
    fundraising.voteRequest(0, {"from": contributor})
    # the number of voters for the request is now increased by 1
    expected = 1
    number_of_voters = fundraising.getRequestInfo(0)[4]
    assert expected == number_of_voters


# payment test
def test_makePayment():
    admin = accounts[0]
    contributor = accounts[1]
    contribution = 100000000000000000
    recipient = accounts[2]
    balance_before_payment = recipient.balance()
    fundraising = Fundraising.deploy(1000000000000000000, 604800, {"from": admin})
    fundraising.createRequest("request", recipient, 100000000000000000, {"from": admin})
    fundraising.contribute({"from": contributor, "value": contribution})
    fundraising.voteRequest(0, {"from": contributor})
    # if the quorum is reached the administrator can send the payment
    fundraising.makePayment(0, {"from": admin})
    # check the difference of balance after the payment
    balance_after_payment = recipient.balance()
    difference = balance_after_payment - balance_before_payment
    # recipient must have received 0.1 ETH as settled in the request
    expected = contribution
    assert expected == difference
