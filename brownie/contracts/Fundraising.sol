//SPDX-License-Identifier: GPL-3.0

pragma solidity 0.8.0;

contract Fundraising {
    mapping(address => uint256) public contributors;
    address public admin;
    uint256 public numberOfContributors;
    uint256 public minContribution;
    uint256 public deadline; // timestamp
    uint256 public goal;
    uint256 public raisedAmount;

    struct Request {
        string description;
        address payable recipient;
        uint256 value;
        bool completed;
        uint256 numberOfVoters;
        mapping(address => bool) voters;
    }

    mapping(uint256 => Request) public requests;

    uint256 public numberOfRequests;

    constructor(uint256 _goal, uint256 _deadline) {
        goal = _goal;
        deadline = block.timestamp + _deadline;
        minContribution = 100 wei;
        admin = msg.sender;
    }

    event ContributeEvent(address _sender, uint256 _value);

    event CreateRequestEvent(
        string _description,
        address _recipient,
        uint256 _value
    );

    event MakePaymentEvent(address _recipient, uint256 _value);

    function contribute() public payable {
        require(block.timestamp < deadline, "Deadline has passed!");
        require(msg.value >= minContribution, "Minimum Contribution not met!");

        if (contributors[msg.sender] == 0) {
            numberOfContributors++;
        }

        contributors[msg.sender] += msg.value;
        raisedAmount += msg.value;

        emit ContributeEvent(msg.sender, msg.value);
    }

    receive() external payable {
        contribute();
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only Admin can call this function!");
        _;
    }

    function createRequest(
        string memory _description,
        address payable _recipient,
        uint256 _value
    ) public onlyAdmin {
        Request storage newRequest = requests[numberOfRequests];
        numberOfRequests++;

        newRequest.description = _description;
        newRequest.recipient = _recipient;
        newRequest.value = _value;
        newRequest.completed = false;
        newRequest.numberOfVoters = 0;

        emit CreateRequestEvent(_description, _recipient, _value);
    }

    function getRequestInfo(uint256 _requestIndex)
        public
        view
        returns (
            string memory,
            address,
            uint256,
            bool,
            uint256
        )
    {
        Request storage r = requests[_requestIndex];
        return (
            r.description,
            r.recipient,
            r.value,
            r.completed,
            r.numberOfVoters
        );
    }

    function voteRequest(uint256 _requestNo) public {
        require(
            contributors[msg.sender] > 0,
            "You must be a contributor to vote"
        );
        Request storage thisRequest = requests[_requestNo];

        require(
            thisRequest.voters[msg.sender] == false,
            "You have already voted!"
        );
        thisRequest.voters[msg.sender] = true;
        thisRequest.numberOfVoters++;
    }

    function makePayment(uint256 _requestNo) public onlyAdmin {
        Request storage thisRequest = requests[_requestNo];
        require(
            raisedAmount >= thisRequest.value,
            "You have not raised enough ETH!"
        );
        require(
            thisRequest.completed == false,
            "The request has been completed!"
        );
        require(thisRequest.numberOfVoters > numberOfContributors / 2); // 50% of contributors voted for this request

        thisRequest.recipient.transfer(thisRequest.value);
        thisRequest.completed = true;

        emit MakePaymentEvent(thisRequest.recipient, thisRequest.value);
    }
}
