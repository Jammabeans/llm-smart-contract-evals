// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC20Case004 {
    function safeTransferFrom(address from, address to, uint256 amount) external;
}

contract Case004Distributor {
    error InvalidSignature();

    IERC20Case004 public projectToken;
    mapping(address => uint256) public nonces;

    struct ClaimParams {
        address kycAddress,
        uint256 nonce,
        address[] projectTokenProxyWallets,
        uint256[] tokenAmountsToClaim,
        bytes signature
    }

    constructor(IERC20Case004 _projectToken) {
        projectToken = _projectToken;
    }

    function claim(ClaimParams calldata _params) external {
        if (!_isSignatureValid(_params)) {
            revert InvalidSignature();
        }

        // update nonce
        nonces[_params.kycAddress] = _params.nonce;

        for (uint256 i = 0; i < _params.projectTokenProxyWallets.length; i++) {
            // VULNERABLE: transfers to msg.sender instead of binding to _params.kycAddress.
            projectToken.safeTransferFrom(
                _params.projectTokenProxyWallets[i],
                msg.sender,
                _params.tokenAmountsToClaim[i]
            );
        }
    }

    function _isSignatureValid(ClaimParams calldata _params) internal pure returns (bool) {
        return _params.kycAddress != address(0) && _params.signature.length > 0;
    }
}

