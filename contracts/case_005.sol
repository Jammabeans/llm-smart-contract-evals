// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Case005EpochRewarder {
    struct CumulativeClaim {
        uint256 startBlock;
        uint256 endBlock;
        uint256 amount;
    }

    mapping(address => mapping(address => mapping(uint256 => CumulativeClaim))) public claimed;

    // VULNERABLE: claim.amount == 0 gate blocks later claims in multi-epoch distributions.
    function handleProofResult(
        address userAddress,
        address rewardTokenAddress,
        uint256 distributionId,
        uint256 startBlock,
        uint256 endBlock,
        uint256 totalRewardAmount
    ) external {
        CumulativeClaim memory claim = claimed[userAddress][rewardTokenAddress][distributionId];
        require(claim.amount == 0, "Already claimed reward.");
        claim.startBlock = startBlock;
        claim.endBlock = endBlock;
        claim.amount = totalRewardAmount;
        claimed[userAddress][rewardTokenAddress][distributionId] = claim;
    }
}

