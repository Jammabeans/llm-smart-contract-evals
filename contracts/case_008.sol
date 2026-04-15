// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Case008MultiSign {
    uint64 public noOfOwners;
    uint256 public requiredApprovals;
    address[] public owners;
    mapping(bytes32 => mapping(address => bool)) public approvedToUpdate;
    uint256 public param;

    constructor(address[] memory _owners, uint256 _requiredApprovals) {
        owners = _owners;
        noOfOwners = uint64(_owners.length);
        requiredApprovals = _requiredApprovals;
    }

    function approveSetterAction(bytes32 _function) external {
        approvedToUpdate[_function][msg.sender] = true;
    }

    function getSetterFunctionApproval(bytes32 _function) public view returns (uint256 approvals) {
        for (uint256 i = 0; i < owners.length; i++) {
            if (approvedToUpdate[_function][owners[i]]) {
                approvals += 1;
            }
        }
    }

    // VULNERABLE: missing owner-only guard; any caller can reset approvals.
    function executeSetterFunction(bytes32 _function, uint256 newValue) external {
        require(
            getSetterFunctionApproval(_function) >= requiredApprovals,
            "Required approvals not met"
        );
        for (uint64 i; i < noOfOwners; i++) {
            approvedToUpdate[_function][owners[i]] = false;
        }
        param = newValue;
    }
}

