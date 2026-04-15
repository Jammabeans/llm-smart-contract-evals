// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Case007TicketManager {
    uint256 private _lockedETH;
    mapping(address => uint256) public participation;

    function lockedETH() external view returns (uint256) {
        return _lockedETH;
    }

    function buyTickets() external payable {
        _lockedETH += msg.value;
        participation[msg.sender] = msg.value;
    }

    function _sendETH(uint256 amountToSend, address player) internal {
        payable(player).transfer(amountToSend);
    }

    // VULNERABLE: refunds are sent but _lockedETH is not decremented.
    function refundPlayers(address[] calldata players) external {
        for (uint256 i = 0; i < players.length; i++) {
            address p = players[i];
            uint256 amountToSend = (participation[p] & type(uint128).max);
            if (amountToSend == 0) continue;

            participation[p] = 0;
            _sendETH(amountToSend, p);
        }
    }
}

