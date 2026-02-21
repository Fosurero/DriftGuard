// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {DriftGuardRegistry} from "../src/DriftGuardRegistry.sol";

interface Vm {
    function prank(address sender) external;
    function expectRevert(bytes calldata) external;
    function expectEmit(bool, bool, bool, bool) external;
}

contract DriftGuardRegistryTest {
    Vm private constant vm = Vm(address(uint160(uint256(keccak256("hevm cheat code")))));

    DriftGuardRegistry private registry;

    event ReportPublished(bytes32 reportHash, bytes32 rulepackHash, address indexed publisher);

    function setUp() public {
        registry = new DriftGuardRegistry();
    }

    function test_ownerCanSetVersion() public {
        bytes32 hash = keccak256("rulepack");
        registry.setVersion("0.1.0", hash);

        (string memory toolVersion, bytes32 rulepackHash) = registry.version();
        require(keccak256(bytes(toolVersion)) == keccak256(bytes("0.1.0")), "version mismatch");
        require(rulepackHash == hash, "hash mismatch");
    }

    function test_nonOwnerCannotSetVersion() public {
        bytes32 hash = keccak256("rulepack");
        vm.prank(address(0xBEEF));
        vm.expectRevert(bytes("Ownable: caller is not the owner"));
        registry.setVersion("0.1.0", hash);
    }

    function test_publishReportMarksAndEmits() public {
        bytes32 rpHash = keccak256("rp");
        bytes32 reportHash = keccak256("report");

        registry.setVersion("0.1.0", rpHash);

        vm.expectEmit(true, true, true, true);
        emit ReportPublished(reportHash, rpHash, address(this));

        registry.publishReport(reportHash);

        require(registry.publishedReports(reportHash), "report not marked");
    }
}
