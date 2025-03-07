# # from ast import Lambda
# import flwr as fl
# from flwr.server.strategy import FedAvg
# from web3 import Web3
# import os
# import json
# import numpy as np

# w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
# contract_address = "0x8254201A7E270D491c1002fB4615019036190DE9"
# private_key = "0x30876c346fc0a479ec7a4cef831473a1a27977924fc1c85e68bfd19533a42318"
# account = w3.eth.account.from_key(private_key)

# contract_abi = [
#     {
#       "inputs": [],
#       "stateMutability": "nonpayable",
#       "type": "constructor"
#     },
#     {
#       "anonymous": False,
#       "inputs": [
#         {
#           "indexed": False,
#           "internalType": "string",
#           "name": "model",
#           "type": "string"
#         }
#       ],
#       "name": "ModelStored",
#       "type": "event"
#     },
#     {
#       "anonymous": False,
#       "inputs": [
#         {
#           "indexed": False,
#           "internalType": "address",
#           "name": "newOwner",
#           "type": "address"
#         }
#       ],
#       "name": "OwnerChanged",
#       "type": "event"
#     },
#     {
#       "inputs": [
#         {
#           "internalType": "address",
#           "name": "newOwner",
#           "type": "address"
#         }
#       ],
#       "name": "changeOwner",
#       "outputs": [],
#       "stateMutability": "nonpayable",
#       "type": "function"
#     },
#     {
#       "inputs": [],
#       "name": "getModel",
#       "outputs": [
#         {
#           "internalType": "string",
#           "name": "",
#           "type": "string"
#         }
#       ],
#       "stateMutability": "view",
#       "type": "function"
#     },
#     {
#       "inputs": [],
#       "name": "owner",
#       "outputs": [
#         {
#           "internalType": "address",
#           "name": "",
#           "type": "address"
#         }
#       ],
#       "stateMutability": "view",
#       "type": "function"
#     },
#     {
#       "inputs": [
#         {
#           "internalType": "string",
#           "name": "weights",
#           "type": "string"
#         }
#       ],
#       "name": "storeModel",
#       "outputs": [],
#       "stateMutability": "nonpayable",
#       "type": "function"
#     }
#   ]  # Replace with actual ABI
# contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# def store_model_on_blockchain(model_weights):
#     """Stores final model weights on blockchain."""
#     txn = contract.functions.storeModel(model_weights).build_transaction({
#         'from': account.address,
#         'nonce': w3.eth.get_transaction_count(account.address),
#         'gas': 3000000,
#         'gasPrice': w3.to_wei('5', 'gwei')
#     })
#     signed_txn = w3.eth.account.sign_transaction(txn, private_key)
#     tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
#     print(f"Model stored! TX Hash: {tx_hash.hex()}")
    
    
#     # custom function to handle model storage after training is completed
# def on_train_end(server_state):
#     """Triggered after training is completed to store model on blockchain."""
#     final_model_weights = server_state.global_model_parameters
#     model_json = json.dumps([w.tolist() for w in final_model_weights])  # Convert weights to JSON
#     store_model_on_blockchain(model_json)


# def weighted_average(metrics):
#     total_examples = 0
#     federated_metrics = {k: 0 for k in metrics[0][1].keys()}
#     for num_examples, m in metrics:
#         for k, v in m.items():
#             federated_metrics[k] += num_examples * v
#         total_examples += num_examples
#     return {k: v / total_examples for k, v in federated_metrics.items()}

# # Define a custom FedAvg strategy
# strategy = FedAvg(
#     fraction_fit=1.0,  # 100% of clients participate in training each round
#     fraction_evaluate=1.0,  # 100% of clients participate in evaluation
#     min_fit_clients=3,  # Minimum clients for training
#     min_evaluate_clients=3,  # Minimum clients for evaluation
#     min_available_clients=3,  # Minimum clients that should be available
#     fit_metrics_aggregation_fn=lambda  x:x,
#     evaluate_metrics_aggregation_fn=lambda x: x,
#     on_fit_config_fn=lambda _: {"epochs": 1},
#     on_aggregate_fit=on_train_end  # Calls this function after training is completed
# )

# print("🌍 Starting Federated Learning Server...")
# fl.server.start_server(
#     server_address="127.0.0.1:8082",
#     config=fl.server.ServerConfig(num_rounds=5),  # Number of training rounds
#     strategy=strategy,  # Use custom FedAvg strategy
# )



import flwr as fl
from flwr.server.strategy import FedAvg
from web3 import Web3
import json

# Connect to Blockchain
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
contract_address = "0x876686Df6F9305748a78cc301caE460C730B1376"
private_key = "0xaf01b368f3a41224194c8509558281701d3d4ec64856acd6d75925ecf7efdbbe"
account = w3.eth.account.from_key(private_key)

# Smart Contract ABI (Updated for Round Tracking)
contract_abi = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint",
                "name": "round",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "weights",
                "type": "string"
            }
        ],
        "name": "ModelStored",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "OwnerChanged",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "round",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "weights",
                "type": "string"
            }
        ],
        "name": "storeModel",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "round",
                "type": "uint256"
            }
        ],
        "name": "getModel",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "latestRound",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "changeOwner",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Connect to Contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

def get_latest_round():
    """Fetch the latest round stored on blockchain."""
    try:
        return contract.functions.latestRound().call()
    except Exception as e:
        print(f"⚠ Error fetching latest round: {e}")
        return 0  # If error, assume starting at round 0

def store_model_on_blockchain(round_num, model_weights):
    """Stores model weights per round on blockchain."""
    txn = contract.functions.storeModel(round_num, model_weights).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 3000000,
        'gasPrice': w3.to_wei('5', 'gwei')
    })
    signed_txn = w3.eth.account.sign_transaction(txn, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"✅ Model stored for Round {round_num}! TX Hash: {tx_hash.hex()}")

def on_train_end(server_round, parameters, config):
    """Triggered after each training round to store model on blockchain."""
    latest_round = get_latest_round() + 1  # Get latest round and increment
    final_model_weights = parameters
    model_json = json.dumps([w.tolist() for w in final_model_weights])  # Convert weights to JSON
    store_model_on_blockchain(latest_round, model_json)

def weighted_average(metrics):
    total_examples = 0
    federated_metrics = {k: 0 for k in metrics[0][1].keys()}
    for num_examples, m in metrics:
        for k, v in m.items():
            federated_metrics[k] += num_examples * v
        total_examples += num_examples
    return {k: v / total_examples for k, v in federated_metrics.items()}

# Define Custom FedAvg Strategy
strategy = FedAvg(
    fraction_fit=1.0,
    fraction_evaluate=1.0,
    min_fit_clients=3,
    min_evaluate_clients=3,
    min_available_clients=3,
    fit_metrics_aggregation_fn=weighted_average,
    evaluate_metrics_aggregation_fn=weighted_average,
    on_fit_config_fn=lambda _: {"epochs": 1},
    # evaluate_fn=on_train_end  # Calls this function after training ends
)

print("🚀 Starting Federated Learning Server...")
fl.server.start_server(
    server_address="127.0.0.1:8082",
    config=fl.server.ServerConfig(num_rounds=5),
    strategy=strategy
)
