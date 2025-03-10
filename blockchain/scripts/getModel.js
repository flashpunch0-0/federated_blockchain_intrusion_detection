const { ethers } = require("ethers");

async function main() {
  const provider = new ethers.JsonRpcProvider("http://127.0.0.1:7545"); // Ganache RPC
  const contractAddress = "0x9eD857B7d462D12F49516875bFBDD0Db48193895"; // Replace with actual address
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
      ],
      name: "ModelStored",
      type: "event",
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
      ],
      name: "ModelUpdated",
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
          internalType: "bytes[]",
          name: "",
          type: "bytes[]",
        },
      ],
      stateMutability: "view",
      type: "function",
    },
    {
      inputs: [],
      name: "getOwner",
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
          internalType: "bytes[]",
          name: "weights",
          type: "bytes[]",
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
  // const storedModel = await contract.getModel(5);
  // console.log("Stored Model Weights for Round 5:", storedModel);
  console.log(await contract.getOwner());
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
