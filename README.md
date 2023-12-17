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

1. **"Project Directory":**  Specify the root directory where the smart contract source code is located.

2. **"Build Output Directory":**  Indicate the output directory for storing build information (note: this directory should not exist prior to running the script; it will be created automatically).

3. **"Image Version":**  Enter the image version corresponding to the MultiversX SDK used for building the deployed contract. Verify your version at MultiversX SDK Rust Contract Builder Tags.

4. **"Smart Contract Address":**  Provide the address of the deployed smart contract.

5. **"Network of the Smart Contract (D or M)":**  Specify 'D' for Devnet or 'M' for Mainnet.

6. **"Wallet File Name (PEM or JSON)":**  Enter the name of the wallet file from which the smart contract was deployed.