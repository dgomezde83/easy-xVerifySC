# easy-xVerifySC
Seamlessly verify a smart contract on the MultiversX devnet or mainnet

How to use?

Install Docker

Follow the Generic Installation Steps: https://docs.docker.com/desktop/install/linux-install/

Place your wallet file (.pem) or (.json) next to the file verify.py for an easier use.

run python verify.py
The scipt will prompt you for some information:

"Project directory": The root directory where the smart contract source code is located
"Build output directory": The output directory to store the build information (should not exist, the script will create it)
"Image version": the image version corresponding to the multiversx sdk the deployed contract was built on. Check your version at: https://hub.docker.com/r/multiversx/sdk-rust-contract-builder/tags
"Smart contract address": The address of the deployed smart contract
"Network of the smart contract (D or M)": Devenet or Mainnet
"Wallet file name (pem or JSON)": The wallet from which the SC was deployed 


# easy-xVerifySC
**Seamlessly verify a smart contract on the MultiversX devnet or mainnet.**

## How to Use?

### Step 1: Install Docker
1. **Install Docker** following the [Generic Installation Steps](https://docs.docker.com/desktop/install/linux-install/).

### Step 2: Prepare Your Wallet File
2. Place your wallet file (`.pem` or `.json`) adjacent to the `verify.py` file for streamlined usage.

### Step 3: Run the Verification Script
3. Execute the script using the command:
   ```bash
   python verify.py

The script will prompt you for several pieces of information:

"Project Directory": Specify the root directory where the smart contract source code is located.
"Build Output Directory": Indicate the output directory for storing build information (note: this directory should not exist prior to running the script; it will be created automatically).
"Image Version": Enter the image version corresponding to the MultiversX SDK used for building the deployed contract. Verify your version at MultiversX SDK Rust Contract Builder Tags.
"Smart Contract Address": Provide the address of the deployed smart contract.
"Network of the Smart Contract (D or M)": Specify 'D' for Devnet or 'M' for Mainnet.
"Wallet File Name (PEM or JSON)": Enter the name of the wallet file from which the smart contract was deployed.