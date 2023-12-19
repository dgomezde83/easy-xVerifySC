# easy-xVerifySC
**Seamlessly deploy and verify a smart contract on the MultiversX devnet or mainnet.**

## What is it?
**easy-xVerifySC** is a Python-based tool designed to streamline the process of compiling a smart contract from its source code in a reproducible manner, deploying it onto the blockchain, and executing the verification process within the MultiversX explorer. This script simplifies each step, ensuring a seamless and efficient workflow.

## Why use it?
Ensuring the integrity of smart contracts on the blockchain is best achieved by compiling the contract in a reproducible manner and then uploading it. This process validates that the code executed on the blockchain corresponds precisely to the source code being verified. Using this script makes the process much simpler if you intend to deploy your contract from a local PEM or JSON file. If you want more information, check the [documentation](https://docs.multiversx.com/developers/reproducible-contract-builds) and [this](https://www.youtube.com/watch?v=yW1TyslJ-28) video.

## How to Use?

### Step 1: Install Docker
1. **Install Docker** following the [Generic Installation Steps](https://docs.docker.com/desktop/install/linux-install/).

### Step 2: Run the Verification Script
There are two ways to run the script: either in "simulate" mode or in normal mode. The "simulate" mode will not deploy the SC to the devnet/mainnet but will only simulate its deployment to verify that everything is functioning correctly before actual deployment.

```bash
python verify.py simulate
```
```bash
python verify.py
```

The script will prompt you for several pieces of information:

1. **"Project Directory":** Specify the root directory where the smart contract source code is located.

2. **"Build Output Directory":**  Indicate the output directory for storing build information (note: this directory should not exist prior to running the script; it will be created automatically).

3. **"Image Version":**  Enter the latest image version from [DockerHub](https://hub.docker.com/r/multiversx/sdk-rust-contract-builder/tags).

After this, the script will create a reproducible build for the specified image. Then, two additional pieces of information will be requested:

4. **"Network of the Smart Contract (D or M)":**  Specify 'D' for Devnet or 'M' for Mainnet.

5. **"Wallet File Name (PEM or JSON)":**   Enter the name of the wallet file with which you are going to deploy and verify your contract.

A prompt will ask you to deploy the newly created wasm file to the chosen network. The script will suggest an mxpy command to deploy a payable, non-upgradable, readable contract. You are free to copy/paste and modify the suggested command template into another terminal to deploy the contract as you like.

One more piece of information will be requested to verify the contract:

6. **"Smart Contract Address":**  Provide the address of the deployed smart contract.

A prompt will ask you to confirm that you want to launch the verification process with the suggested mxpy command. Enter 'yes' or 'y' to confirm.

Now, the verification process will start. It may take a few minutes to complete, and another few minutes to appear on the chain. Be patient!

Enjoy :)