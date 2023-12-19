#!/usr/bin/env python3
import os
import readline
import subprocess
import sys
import glob
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Build and verify script")
    parser.add_argument("simulate", nargs='?', help="Run in simulation mode", default="")
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
    
def find_bytecode_file(build_output_dir):
    search_path = os.path.join(build_output_dir, "*", "*.wasm")
    files = glob.glob(search_path)
    return files[0] if files else None
    
def confirm_execution(command_description):
    confirm = input(f"Do you want to execute the {command_description}? (yes/no): ").strip().lower()
    return confirm in ["yes", "y"]
    
def is_docker_image_available(image_name):
    try:
        result = subprocess.run(["sudo","docker", "image", "inspect", image_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False

def pull_docker_image(image_name):
    print(f"Pulling Docker image {image_name}...")
    subprocess.run(["sudo","docker", "pull", image_name], check=True)

def main(args=None):
    if not check_command_installed("docker"):
        sys.exit("Docker is not installed. Please install Docker and try again.")

    if not check_command_installed("mxpy"):
        sys.exit("mxpy is not installed. Please install mxpy and try again.")
        
    if args is None:
        args = get_args()
    
    project_dir = get_input("Enter the project directory (relative to current dir): ")
    build_output_dir = get_input("Enter the build output directory (relative to current dir): ")
    build_output_path = os.path.join(os.getcwd(), build_output_dir)
    if not os.path.isdir(build_output_path):
        print(f"Build output directory does not exist. Creating directory: {build_output_path}")
        os.makedirs(build_output_path)
        
    image_version = get_input("Enter the image version (e.g., v5.3.0): ")
    image_name = f"multiversx/sdk-rust-contract-builder:{image_version}"    
    if not is_docker_image_available(image_name):
        download_image = input(f"The Docker image '{image_name}' is not available locally. Do you want to download it? (yes/no): ").strip().lower()
        if download_image in ["yes", "y"]:
            pull_docker_image(image_name)
        else:
            print("Docker image is required to proceed. Exiting.")
            sys.exit(1)
            
    project_path = os.path.join(os.getcwd(), project_dir)
    

    # Running the Docker build command
    build_command = [
        "sudo", "python3", "./build_with_docker.py",
        "--image", image_name,
        "--project", project_path,
        "--output", build_output_path
    ]

    print("Executing command: " + ' '.join(build_command))
    if confirm_execution("Docker build command"):        
        subprocess.run(build_command)
    else:
        print("Skipping Docker build command.")

    # Find the script file
    script_file = find_script_file(build_output_path)
    if not script_file:
        print("Error: No '.source.json' file found in the build output directory.")
        return
    
    network = get_input("Enter the network of the smart contract (D or M): ")
    while network not in ['D', 'M']:
        print("Invalid network. Please enter 'D' for Devnet or 'M' for Mainnet.")
        network = get_input("Enter the network of the smart contract (D or M): ")
        
    wallet = get_input("Enter the wallet file name (relative to current dir) (with .pem or .json extension): ")
    while not wallet.endswith('.pem') and not wallet.endswith('.json'):
        print("Invalid wallet file. The extension must be .pem or .json.")
        wallet = get_input("Enter the wallet file name (relative to current dir) (with .pem or .json extension): ")

    # Construct wallet file path
    wallet_file_path = os.path.join(os.getcwd(), wallet)

    # Construct wallet command
    wallet_command = f"--pem" if wallet.endswith('.pem') else f"--keyfile"
    
    # Proxy URL address
    proxy_url = "https://devnet-gateway.multiversx.com" if network == 'D' else "https://gateway.multiversx.com"

    # Ask the user to deploy the contract
    print(f"Please deploy the smart contract created in '{build_output_path}' to {'Mainnet' if network == 'M' else 'Devnet'}.")
    bytecode_file = find_bytecode_file(build_output_path)
    if not bytecode_file:
        print("Error: No '.wasm' file found in the build output directory.")
        return

    # Determine the chain value based on the network
    chain_value = "D" if network == "D" else "1"
    send_simulate_flag = "--simulate" if args.simulate == "simulate" else "--send"

    deploy_command = [
        "mxpy", "--verbose", "contract", "deploy", "--recall-nonce", "--metadata-not-upgradeable", "--metadata-payable",
        "--bytecode", bytecode_file,
        wallet_command, wallet_file_path,
        "--gas-limit", "60000000",
        "--proxy", proxy_url, "--chain", chain_value,
        send_simulate_flag
    ]


    print("You can deploy the contract using the following command: " + ' '.join(deploy_command))
    if confirm_execution("mxpy contract deployment command"):        
        subprocess.run(deploy_command)
    else:
        print("Skipping contract deployment.")
    
    verifier_url = "https://devnet-play-api.multiversx.com" if network == 'D' else "https://play-api.multiversx.com"

    smart_contract_address = get_input("Enter the smart contract address: ")
    while not validate_smart_contract_address(smart_contract_address):
        print("Invalid smart contract address. It should start with 'erd1' and be 62 characters long.")
        smart_contract_address = get_input("Enter the smart contract address: ")

    # Running the mxpy command
    mxpy_command = [
        "mxpy", "--verbose", "contract", "verify", smart_contract_address,
        "--packaged-src",script_file, "--verifier-url",verifier_url,
        "--docker-image",image_name, wallet_command, wallet_file_path,
    ]

    #Check user if he wants to skip this command
    print("Executing command: " + ' '.join(mxpy_command))
    if confirm_execution("mxpy verification command"):        
        subprocess.run(mxpy_command)
    else:
        print("Skipping mxpy verification command.")

if __name__ == "__main__":
    main()
