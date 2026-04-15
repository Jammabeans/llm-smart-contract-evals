// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IWETHCase003 {
    function deposit() external payable;
}

contract Case003BorrowLiquidation {
    IWETHCase003 public weth;

    struct DepositDetail {
        uint256 depositedAmountInETH;
    }

    mapping(address => DepositDetail) public depositDetail;

    constructor(IWETHCase003 _weth) {
        weth = _weth;
    }

    function seedPosition(address user, uint256 depositedAmountInETH) external {
        depositDetail[user] = DepositDetail({depositedAmountInETH: depositedAmountInETH});
    }

    // VULNERABLE: assumes contract has enough native ETH to wrap and can revert.
    function liquidationType2(address user) external {
        uint256 amount = depositDetail[user].depositedAmountInETH / 2;
        weth.deposit{value: amount}();
    }
}

