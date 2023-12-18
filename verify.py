#!/usr/bin/env python3
import os
import readline
import subprocess
import sys
import glob
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Build and verify script")
    parser.add_argument("--project_dir", help="Project directory")
    parser.add_argument("--build_output_dir", help="Build output directory")
    parser.add_argument("--image_version", help="Image version")
    parser.add_argument("--smart_contract_address", help="Smart contract address")
    parser.add_argument("--network", help="Network of the smart contract (D or M)")
    parser.add_argument("--wallet", help="Wallet file name")
    return parser.parse_args()

def check_command_installed(command, version_flag="--version"):
    try:
        subprocess.run([command, version_flag], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def complete(text, state):
    options = [x for x in os.listdir('.') if x.startswith(text)]
    try:
        return options[state]
    except IndexError:
        return None

def get_input(prompt):
    readline.set_completer_delims(' \t\n=')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)
    return input(prompt)

def validate_smart_contract_address(address):
    return address.startswith("erd1") and len(address) == 62

def find_script_file(build_output_dir):
    search_path = os.path.join(build_output_dir, "*", "*.source.json")
    files = glob.glob(search_path)
    return files[0] if files else None

def main(args=None):
    if not check_command_installed("docker"):
        sys.exit("Docker is not installed. Please install Docker and try again.")

    if not check_command_installed("mxpy"):
        sys.exit("mxpy is not installed. Please install mxpy and try again.")
        
    if args is None:
        args = get_args()

    project_dir = args.project_dir if args.project_dir else get_input("Enter the project directory (relative to current dir): ")
    build_output_dir = args.build_output_dir if args.build_output_dir else get_input("Enter the build output directory (relative to current dir): ")
    image_version = args.image_version if args.image_version else get_input("Enter the image version (e.g., v5.3.0): ")
        
    network = args.network if args.network else get_input("Enter the network of the smart contract (D or M): ")
    while network not in ['D', 'M']:
        print("Invalid network. Please enter 'D' for Devnet or 'M' for Mainnet.")
        network = args.network if args.network else get_input("Enter the network of the smart contract (D or M): ")

    verifier_url = "https://devnet-play-api.multiversx.com" if network == 'D' else "https://play-api.multiversx.com"
    image_name = f"multiversx/sdk-rust-contract-builder:{image_version}"
    project_path = os.path.join(os.getcwd(), project_dir)
    build_output_path = os.path.join(os.getcwd(), build_output_dir)

    if not os.path.isdir(build_output_path):
        print(f"Build output directory does not exist. Creating directory: {build_output_path}")
        os.makedirs(build_output_path)

    # Running the Docker build command
    build_command = [
        "sudo", "python3", "./build_with_docker.py",
        "--image", image_name,
        "--project", project_path,
        "--output", build_output_path
    ]

    print("Executing command: " + ' '.join(build_command))
    subprocess.run(build_command)

    # Find the script file
    script_file = find_script_file(build_output_path)
    if not script_file:
        print("Error: No '.source.json' file found in the build output directory.")
        return

     # Ask the user to confirm deployment
    while True:
        deploy_confirm = input("Did you deploy the smart contract created in '" + (build_output_path) + "/your_project_name' to " + ("Mainnet" if network == 'M' else "Devnet") + "? (yes/no): ").strip().lower()
        if deploy_confirm in ["yes", "y"]:
            break
        print("Deploy it and click yes")

    smart_contract_address = args.smart_contract_address if args.smart_contract_address else get_input("Enter the smart contract address: ")
    while not validate_smart_contract_address(smart_contract_address):
        print("Invalid smart contract address. It should start with 'erd1' and be 62 characters long.")
        smart_contract_address = args.smart_contract_address if args.smart_contract_address else get_input("Enter the smart contract address: ")
        
    wallet = args.wallet if args.wallet else get_input("Enter the wallet file name (with .pem or .json extension): ")
    while not wallet.endswith('.pem') and not wallet.endswith('.json'):
        print("Invalid wallet file. The extension must be .pem or .json.")
        wallet = args.wallet if args.wallet else get_input("Enter the wallet file name (with .pem or .json extension): ")

    # Construct wallet command
    wallet_command = f"--pem {wallet}" if wallet.endswith('.pem') else f"--keyfile {wallet}"

    # Running the mxpy command
    mxpy_command = [
        "mxpy", "--verbose", "contract", "verify", smart_contract_address,
        f"--packaged-src={script_file}", f"--verifier-url={verifier_url}",
        f"--docker-image={image_name}", wallet_command
    ]

    print("Executing command: " + ' '.join(mxpy_command))
    #subprocess.run(mxpy_command)

    # Ensure that the function always returns the command strings
    return ' '.join(build_command), ' '.join(mxpy_command)

if __name__ == "__main__":
    main()
