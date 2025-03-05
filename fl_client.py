from data_loader import get_client_data
import flwr as fl
import numpy as np
from model import get_model

CLIENT_ID = 0  # Change this for each client instance
NUM_CLIENTS = 3  # Total number of clients

# Load unique dataset for this client
X_train, Y_train, X_test, Y_test = get_client_data(CLIENT_ID, NUM_CLIENTS)

class FLClient(fl.client.NumPyClient):
    def __init__(self):
        self.model = get_model(sample_shape=(X_train.shape[1],))

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
