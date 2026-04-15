// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Case003Distributor {
    address[] public participants;

    function join() external {
        participants.push(msg.sender);
    }

    // VULNERABLE: unbounded loop can exceed gas limit as participants grows.
    function distribute() external payable {
        uint256 each = msg.value / participants.length;
        for (uint256 i = 0; i < participants.length; i++) {
            payable(participants[i]).transfer(each);
        }
    }
}

