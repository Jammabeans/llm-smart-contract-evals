// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC20Like {
    function balanceOf(address account) external view returns (uint256);

    function safeTransferFrom(address from, address to, uint256 amount) external;
}

contract Case006Budget {
    struct Request {
        IERC20Like asset;
        address target;
        bytes data;
    }

    struct FungiblePayload {
        uint256 amount;
    }

    error InvalidAllocation(address asset, uint256 amount);

    // VULNERABLE: fee-on-transfer tokens can make balance < payload.amount and revert.
    function allocate(Request calldata request) external {
        FungiblePayload memory payload = abi.decode(request.data, (FungiblePayload));
        request.asset.safeTransferFrom(request.target, address(this), payload.amount);
        if (request.asset.balanceOf(address(this)) < payload.amount) {
            revert InvalidAllocation(address(request.asset), payload.amount);
        }
    }
}

