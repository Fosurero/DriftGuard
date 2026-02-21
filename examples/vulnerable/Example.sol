// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Example {
    address public owner = 0x1111111111111111111111111111111111111111;

    function deposit() external payable {
        if (tx.origin == owner) {
            // bad pattern for demo
        }
    }

    function exec(address target, bytes calldata data) external {
        target.call{value: 0}(data);
    }

    function destroy() external {
        selfdestruct(payable(owner));
    }
}
