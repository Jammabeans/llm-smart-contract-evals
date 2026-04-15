// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Case002Treasury {
    uint256 public totalInterest;
    uint256 public totalInterestFromLiquidation;

    constructor() payable {
        totalInterest = msg.value / 2;
        totalInterestFromLiquidation = msg.value - totalInterest;
    }

    // VULNERABLE: checks combined balance, but subtracts only from totalInterest.
    function withdrawInterest(uint256 amount) external {
        require(
            amount <= (totalInterest + totalInterestFromLiquidation),
            "Treasury don't have enough interest"
        );
        totalInterest -= amount;
        payable(msg.sender).transfer(amount);
    }
}

