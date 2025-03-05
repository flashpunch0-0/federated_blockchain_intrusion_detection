const hre = require("hardhat");

async function main() {
  const FLModelStorage = await hre.ethers.getContractFactory("FLModelStorage");
  const contract = await FLModelStorage.deploy(); // Deploy without constructor arguments

  // ✅ Wait for deployment
  await contract.waitForDeployment();

  console.log(`Contract deployed at: ${contract.target}`); // ✅ Use `target` for address
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
