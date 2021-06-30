import "@nomiclabs/hardhat-waffle"
import "@nomiclabs/hardhat-ethers"
import {ethers} from 'hardhat'
import "@nomiclabs/hardhat-waffle"
import { HardhatUserConfig, task } from "hardhat/config"
import "hardhat-deploy"
import "hardhat-deploy-ethers"
import "@typechain/hardhat"

// This is a sample Hardhat task. To learn how to create your own go to
// https://hardhat.org/guides/create-task.html
task("accounts", "Prints the list of accounts", async () => {
  const accounts = await ethers.getSigners();

  for (const account of accounts) {
    console.log(account.address);
  }
});

module.exports = {
  networks: {
    forking: {
      url: "",
    },
    hardhat: {
      allowUnlimitedContractSize: true,
      //saveDeployments: false
    },
    testnet: {
      url: "https://mainnet.infura.io/v3/ccb956822bcc4716a8090b35c3d07c1b",
      chainId: 4,
      gasPrice: 20000000000,
    },
    local: {
      url: "http://127.0.0.1:8545",
      gasPrice: 20000000000,
    },
  },
  solidity: {
    compilers: [
      {
        version: "0.8.4",
      },
      {
        version: "0.6.7",
        settings: {},
      },
      {
        version: "0.6.6",
        settings: {},
      },
    ],
    settings: {
      optimizer: { enabled: true, runs: 1 },
      evmVersion: "istanbul",
    },
  },
  mocha: {
    timeout: 60000,
  },
  typechain: {
    outDir: "src/types",
    target: "ethers-v5",
  },
};
