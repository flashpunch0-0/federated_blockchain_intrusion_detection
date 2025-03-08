// SPDX-License-Identifier: MIT

//  THIS SMART CONTRACT WOULD BE USEFUL IF ONYLY ONE FINAL TRANSACTION IS NEEDED
// pragma solidity ^0.8.0;

// contract FLModelStorage {
//     string private modelWeights;  // Stores model weights as JSON string
//     address public owner;         // Contract owner

//     event ModelStored(string model);
//     event OwnerChanged(address newOwner);

//     constructor() {
//         owner = msg.sender;  // Set the deployer as owner
//     }

//     modifier onlyOwner() {
//         require(msg.sender == owner, "Only the owner can call this function");
//         _;
//     }

//     function storeModel(string memory weights) public onlyOwner {
//         modelWeights = weights;
//         emit ModelStored(weights); // Log event
//     }

//     function getModel() public view returns (string memory) {
//         return modelWeights;
//     }

//     function changeOwner(address newOwner) public onlyOwner {
//         owner = newOwner;
//         emit OwnerChanged(newOwner);
//     }
// }


//  working smart contract below for each round weights to be stored 

// pragma solidity ^0.8.0;

// contract FLModelStorage {
//     struct ModelUpdate {
//         uint round;
//         string weights;  // Stores model weights as JSON string
//     }

//     mapping(uint => ModelUpdate) public modelUpdates;  // Round => Model
//     uint public latestRound;  // Tracks the latest training round
//     address public owner;  // Contract owner

//     event ModelStored(uint round, string weights);
//     event OwnerChanged(address newOwner);

//     constructor() {
//         owner = msg.sender;
//     }

//     modifier onlyOwner() {
//         require(msg.sender == owner, "Only the owner can call this function");
//         _;
//     }

//     function storeModel(uint round, string memory weights) public onlyOwner {
//         require(bytes(weights).length > 0, "Weights cannot be empty");
//         require(modelUpdates[round].round == 0, "Round already exists");  // Prevent overwriting

//         modelUpdates[round] = ModelUpdate(round, weights);
//         latestRound = round;  // Update latest round
//         emit ModelStored(round, weights);
//     }

//     function getModel(uint round) public view returns (string memory) {
//         require(modelUpdates[round].round != 0, "Model for this round does not exist");
//         return modelUpdates[round].weights;
//     }

//     function changeOwner(address newOwner) public onlyOwner {
//         owner = newOwner;
//         emit OwnerChanged(newOwner);
//     }
// }



//  new smart contract to store model weights in bytes format which is the format of flower framework
pragma solidity ^0.8.0;

contract FLModelStorage {
    struct ModelUpdate {
        uint round;
        bytes[] weights;  // Stores model weights as an array of bytes
    }

    mapping(uint => ModelUpdate) public modelUpdates;  // Round => Model
    uint public latestRound;  // Tracks the latest training round
    address public owner;  // Contract owner

    event ModelStored(uint round);
    event ModelUpdated(uint round);
    event OwnerChanged(address newOwner);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function");
        _;
    }

    function storeModel(uint round, bytes[] memory weights) public onlyOwner {
        require(weights.length > 0, "Weights cannot be empty");

        if (modelUpdates[round].round == 0) {
            // New round, store it
            latestRound = round;  
            emit ModelStored(round);
        } else {
            // Overwrite existing round
            emit ModelUpdated(round);
        }

        // Store/Update model weights
        modelUpdates[round] = ModelUpdate(round, weights);
    }

    function getModel(uint round) public view returns (bytes[] memory) {
        require(modelUpdates[round].round != 0, "Model for this round does not exist");
        return modelUpdates[round].weights;
    }

    function changeOwner(address newOwner) public onlyOwner {
        owner = newOwner;
        emit OwnerChanged(newOwner);
    }
}
