import flwr as fl
import numpy as np
import os
import json
from typing import Callable, Dict, Optional, Tuple
from flwr.common import Parameters, Scalar
from web3 import Web3

class SaveModelStrategy(fl.server.strategy.FedAvg):
    def __init__(self,
        *,
        fraction_fit: float = 0.1,
        fraction_eval: float = 0.1,
        min_fit_clients: int = 2,
        min_eval_clients: int = 2,
        min_available_clients: int = 2,
        eval_fn: Optional[Callable[[Parameters], Optional[Tuple[float, Dict[str, Scalar]]]]] = None,
        on_fit_config_fn: Optional[Callable[[int], Dict[str, Scalar]]] = None,
        on_evaluate_config_fn: Optional[Callable[[int], Dict[str, Scalar]]] = None,
        accept_failures: bool = True,
        initial_parameters: Optional[Parameters] = None
    ) -> None:
        super().__init__(
            fraction_fit=fraction_fit,
            fraction_eval=fraction_eval,
            min_fit_clients=min_fit_clients,
            min_eval_clients=min_eval_clients,
            min_available_clients=min_available_clients,
            eval_fn=eval_fn,
            on_fit_config_fn=on_fit_config_fn,
            on_evaluate_config_fn=on_evaluate_config_fn,
            accept_failures=accept_failures,
            initial_parameters=initial_parameters
        )
        
        self.contribution = {}
        self.web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))  # Ensure this matches your Ganache/Blockchain setup
        self.contract = self.load_smart_contract()

    def load_smart_contract(self):
        """Loads the deployed smart contract"""
        with open("contract_abi.json", "r") as abi_file:
            contract_abi = json.load(abi_file)
        
        contract_address = "0x5Ea1664ae5904F5A328f2dB2dEA303fA12b1f699"  # Replace with actual deployed address
        return self.web3.eth.contract(address=contract_address, abi=contract_abi)

    def save_to_blockchain(self, round_num, aggregated_weights):
        """Saves model weights on the blockchain"""
        try:
            weights_list = [w.tolist() for w in aggregated_weights]  # Convert weights to list
            weights_str = json.dumps(weights_list)  # Convert NumPy list to JSON string
            
            tx = self.contract.functions.storeModel(round_num, weights_str).build_transaction({
                "from": self.web3.eth.accounts[0],  # Replace with the actual sender address
                "gas": 3000000,
                "gasPrice": self.web3.to_wei("5", "gwei"),
                "nonce": self.web3.eth.get_transaction_count(self.web3.eth.accounts[0])
            })
            
            signed_tx = self.web3.eth.account.sign_transaction(tx, private_key="0x30876c346fc0a479ec7a4cef831473a1a27977924fc1c85e68bfd19533a42318")
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            self.web3.eth.wait_for_transaction_receipt(tx_hash)

            print(f"✅ Round {round_num} weights saved on blockchain.")

        except Exception as e:
            print(f"⚠️ Error saving weights on blockchain: {e}")

    def aggregate_fit(self, rnd, results, failures):
        """Aggregates model updates and stores on blockchain"""
        aggregated_result = super().aggregate_fit(rnd, results, failures)

        if aggregated_result is not None:
            aggregated_weights, _ = aggregated_result  # Extract Parameters

            print(f"🔄 Saving round {rnd} aggregated weights...")

            # Convert parameters to NumPy format
            weights_np = fl.common.parameters_to_ndarrays(aggregated_weights)

            # Save to blockchain
            self.save_to_blockchain(rnd, weights_np)

            # Track client contributions
            for res in results:
                client_id = res[1].metrics.get("client_id", "unknown")
                data_size = res[1].num_examples

                print(f"📊 Client {client_id} participated with data size {data_size}")

                if client_id not in self.contribution:
                    self.contribution[client_id] = {"data_size": data_size, "num_rounds_participated": 1}
                else:
                    self.contribution[client_id]["num_rounds_participated"] += 1
        
        return aggregated_result

# Start the server
strategy = SaveModelStrategy()
fl.server.start_server(server_address="127.0.0.1:8082", strategy=strategy)
