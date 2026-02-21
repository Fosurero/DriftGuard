// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DriftGuardRegistry {
    address public owner;
    string public toolVersion;
    bytes32 public rulepackHash;

    mapping(bytes32 => bool) public publishedReports;

    event VersionUpdated(string toolVersion, bytes32 rulepackHash);
    event ReportPublished(bytes32 reportHash, bytes32 rulepackHash, address indexed publisher);

    modifier onlyOwner() {
        require(msg.sender == owner, "Ownable: caller is not the owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function setVersion(string calldata newVersion, bytes32 newRulepackHash) external onlyOwner {
        toolVersion = newVersion;
        rulepackHash = newRulepackHash;
        emit VersionUpdated(newVersion, newRulepackHash);
    }

    function publishReport(bytes32 reportHash) external {
        publishedReports[reportHash] = true;
        emit ReportPublished(reportHash, rulepackHash, msg.sender);
    }

    function version() external view returns (string memory, bytes32) {
        return (toolVersion, rulepackHash);
    }
}
