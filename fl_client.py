from data_loader import get_client_data
import flwr as fl
import numpy as np
from model import get_model
from web3 import Web3
import os
import json

CLIENT_ID = 0  # Change this for each client instance
NUM_CLIENTS = 3  # Total number of clients

#  connect to blockchain
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
contract_address = "0x5e2501E40E87489F6c682d599890B5c9D20eF62a"
# private_key = os.getenv("0x30876c346fc0a479ec7a4cef831473a1a27977924fc1c85e68bfd19533a42318")

contract_abi =  [
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
          "internalType": "uint256",
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
          "internalType": "address",
          "name": "newOwner",
          "type": "address"
        }
      ],
      "name": "changeOwner",
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
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "modelUpdates",
      "outputs": [
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
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "owner",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
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
    }
  ] # Replace with actual ABI
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# def fetch_model_from_blockchain():
#     """Fetches the global model from blockchain and converts it back to weights."""
#     try:
#         model_json = contract.functions.getModel().call()
#         model_weights = np.array(json.loads(model_json), dtype=object)
#         print("✅ Model fetched from blockchain!")
#         return model_weights
#     except Exception as e:
#         print("⚠️ No model found on blockchain. Using random initialization.")
#         return None
    
def fetch_model_from_blockchain():
    """Fetches the latest global model from the blockchain and converts it back to weights."""
    try:
        # Get the latest stored round
        latest_round = contract.functions.latestRound().call()

        if latest_round == 0:
            print("⚠️ No model found on blockchain. Using random initialization.")
            return None

        # Fetch model weights from the latest round
        model_json = contract.functions.getModel(latest_round).call()
        model_weights = np.array(json.loads(model_json), dtype=object)

        print(f"✅ Model fetched from blockchain! Round: {latest_round}")
        print("🔹 Initial Model Weights:", model_weights)  # Print weights

        return model_weights

    except Exception as e:
        print(f"⚠️ Error fetching model from blockchain: {e}")
        return None


# Load unique dataset for this client
X_train, Y_train, X_test, Y_test = get_client_data(CLIENT_ID, NUM_CLIENTS)

class FLClient(fl.client.NumPyClient):
    def __init__(self):
        self.model = get_model(sample_shape=(X_train.shape[1],))
        print(self.model.summary())
        # initial_weights = fetch_model_from_blockchain()
        # if initial_weights is not None:
        #   self.model.set_weights(initial_weights)
        #   print("✅ Model weights loaded successfully!")
        # else:
        #   print("⚠️ No model on blockchain. Using randomly initialized weights.")

    def get_parameters(self, config):
        return self.model.get_weights()

    def set_parameters(self, parameters):
        self.model.set_weights(parameters)

    def fit(self, parameters, config):
        self.set_parameters(parameters)
        self.model.fit(X_train, Y_train, epochs=1, batch_size=32, verbose=0)
        return self.get_parameters(config={}), len(X_train), {}

    def evaluate(self, parameters, config):
        self.set_parameters(parameters)
        loss, accuracy = self.model.evaluate(X_test, Y_test, verbose=0)
        return loss, len(X_test), {"accuracy": accuracy}

fl.client.start_numpy_client(server_address="127.0.0.1:8082", client=FLClient())
