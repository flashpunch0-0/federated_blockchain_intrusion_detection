import flwr as fl
from flwr.server.strategy import FedAvg
from web3 import Web3
def weighted_average(metrics):
    total_examples = 0
    federated_metrics = {k: 0 for k in metrics[0][1].keys()}
    for num_examples, m in metrics:
        for k, v in m.items():
            federated_metrics[k] += num_examples * v
        total_examples += num_examples
    return {k: v / total_examples for k, v in federated_metrics.items()}

# Define a custom FedAvg strategy
strategy = FedAvg(
    fraction_fit=1.0,  # 100% of clients participate in training each round
    fraction_evaluate=1.0,  # 100% of clients participate in evaluation
    min_fit_clients=3,  # Minimum clients for training
    min_evaluate_clients=3,  # Minimum clients for evaluation
    min_available_clients=3,  # Minimum clients that should be available
    fit_metrics_aggregation_fn=weighted_average,
    evaluate_metrics_aggregation_fn=weighted_average,
)

print("🌍 Starting Federated Learning Server...")
fl.server.start_server(
    server_address="127.0.0.1:8082",
    config=fl.server.ServerConfig(num_rounds=5),  # Number of training rounds
    strategy=strategy,  # Use custom FedAvg strategy
)
