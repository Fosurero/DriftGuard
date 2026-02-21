// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {DriftGuardRegistry} from "../src/DriftGuardRegistry.sol";

interface Vm {
    function envBytes32(string calldata name) external returns (bytes32);
    function startBroadcast() external;
    function stopBroadcast() external;
}

contract Deploy {
    Vm private constant vm = Vm(address(uint160(uint256(keccak256("hevm cheat code")))));

    function run() external returns (DriftGuardRegistry registry) {
        bytes32 configuredRulepackHash = vm.envBytes32("RULEPACK_HASH");
        vm.startBroadcast();
        registry = new DriftGuardRegistry();
        registry.setVersion("0.1.0", configuredRulepackHash);
        vm.stopBroadcast();
    }
}
