// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FLModelStorage {
    string private modelWeights;  // Stores model weights as JSON string
    address public owner;         // Contract owner

    event ModelStored(string model);
    event OwnerChanged(address newOwner);

    constructor() {
        owner = msg.sender;  // Set the deployer as owner
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function");
        _;
    }

    function storeModel(string memory weights) public onlyOwner {
        modelWeights = weights;
        emit ModelStored(weights); // Log event
    }

    function getModel() public view returns (string memory) {
        return modelWeights;
    }

    function changeOwner(address newOwner) public onlyOwner {
        owner = newOwner;
        emit OwnerChanged(newOwner);
    }
}
