// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Case001Escrow {
    address public owner;

    constructor() payable {
        owner = msg.sender;
    }

    // VULNERABLE: missing access control.
    function emergencyWithdraw() external {
        payable(msg.sender).transfer(address(this).balance);
    }
}

