const { ethers } = require("ethers");

async function main() {
  const provider = new ethers.JsonRpcProvider("http://127.0.0.1:7545"); // Ganache RPC
  const contractAddress = "0x5e2501E40E87489F6c682d599890B5c9D20eF62a"; // Replace with actual address
  const abi = [
    {
      inputs: [],
      stateMutability: "nonpayable",
      type: "constructor",
    },
    {
      anonymous: false,
      inputs: [
        {
          indexed: false,
          internalType: "uint256",
          name: "round",
          type: "uint256",
        },
        {
          indexed: false,
          internalType: "string",
          name: "weights",
          type: "string",
        },
      ],
      name: "ModelStored",
      type: "event",
    },
    {
      anonymous: false,
      inputs: [
        {
          indexed: false,
          internalType: "address",
          name: "newOwner",
          type: "address",
        },
      ],
      name: "OwnerChanged",
      type: "event",
    },
    {
      inputs: [
        {
          internalType: "address",
          name: "newOwner",
          type: "address",
        },
      ],
      name: "changeOwner",
      outputs: [],
      stateMutability: "nonpayable",
      type: "function",
    },
    {
      inputs: [
        {
          internalType: "uint256",
          name: "round",
          type: "uint256",
        },
      ],
      name: "getModel",
      outputs: [
        {
          internalType: "string",
          name: "",
          type: "string",
        },
      ],
      stateMutability: "view",
      type: "function",
    },
    {
      inputs: [],
      name: "latestRound",
      outputs: [
        {
          internalType: "uint256",
          name: "",
          type: "uint256",
        },
      ],
      stateMutability: "view",
      type: "function",
    },
    {
      inputs: [
        {
          internalType: "uint256",
          name: "",
          type: "uint256",
        },
      ],
      name: "modelUpdates",
      outputs: [
        {
          internalType: "uint256",
          name: "round",
          type: "uint256",
        },
        {
          internalType: "string",
          name: "weights",
          type: "string",
        },
      ],
      stateMutability: "view",
      type: "function",
    },
    {
      inputs: [],
      name: "owner",
      outputs: [
        {
          internalType: "address",
          name: "",
          type: "address",
        },
      ],
      stateMutability: "view",
      type: "function",
    },
    {
      inputs: [
        {
          internalType: "uint256",
          name: "round",
          type: "uint256",
        },
        {
          internalType: "string",
          name: "weights",
          type: "string",
        },
      ],
      name: "storeModel",
      outputs: [],
      stateMutability: "nonpayable",
      type: "function",
    },
  ];

  // Connect to the deployed contract
  const contract = new ethers.Contract(contractAddress, abi, provider);

  // Fetch the stored model for round 5
  const storedModel = await contract.getModel(5);
  console.log("Stored Model Weights for Round 5:", storedModel);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
