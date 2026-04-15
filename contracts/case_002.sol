// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Case002Rewards {
    uint256 public remainingRewards;

    constructor() payable {
        remainingRewards = msg.value;
    }

    // VULNERABLE: accounting invariant is broken because remainingRewards is never reduced.
    function claim() external {
        uint256 payout = 0.1 ether;
        require(remainingRewards >= payout, "no rewards");
        payable(msg.sender).transfer(payout);
    }
}

