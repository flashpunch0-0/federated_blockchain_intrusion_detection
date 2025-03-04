import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import numpy as np

def get_client_data(client_id, num_clients):
    """
    Loads and preprocesses data, then returns a unique subset for a given client.
    :param client_id: Unique client identifier (0, 1, 2, ...)
    :param num_clients: Total number of clients in FL system
    :return: X_train_client, Y_train_client, X_test, Y_test
    """
    train_data = _load_data("data/preprocessed_train_data.csv")
    test_data = _load_data("data/preprocessed_test_data.csv")

    train_data = _preprocess_data(train_data)
    test_data = _preprocess_data(test_data)

    # Split training data among clients
    client_train_data = _split_data_for_client(train_data, client_id, num_clients)

    X_train, Y_train = _separate_features_and_labels(client_train_data)
    X_test, Y_test = _separate_features_and_labels(test_data)  # Test data is shared

    return X_train, Y_train, X_test, Y_test

def _load_data(file_path):
    data = pd.read_csv(file_path)
    data = data.drop(columns=["attack_cat"])  # Drop unnecessary columns
    return data

# def _preprocess_data(data):
#     # Encode categorical features
#     for column in data.columns:
#         if data[column].dtype == type(object):
#             le = preprocessing.LabelEncoder()
#             data[column] = le.fit_transform(data[column])

#     # Normalize features
#     min_max_scaler = preprocessing.MinMaxScaler()
#     for column in data.columns:
#         data[column] = min_max_scaler.fit_transform(data[column].values.reshape(-1,1))
#     return data

def _preprocess_data(data):
    # Encode categorical features
    categorical_columns = data.select_dtypes(include=['object']).columns
    for column in categorical_columns:
        le = preprocessing.LabelEncoder()
        data[column] = le.fit_transform(data[column])

    # Normalize features
    min_max_scaler = preprocessing.MinMaxScaler()
    numerical_columns = data.select_dtypes(include=['float64', 'int64']).columns
    data[numerical_columns] = min_max_scaler.fit_transform(data[numerical_columns])

    return data


def _split_data_for_client(data, client_id, num_clients):
    """
    Splits the dataset into `num_clients` parts and returns the portion for `client_id`
    """
    data_splits = np.array_split(data, num_clients)  # Split dataset into parts
    return data_splits[client_id]  # Return client-specific portion

def _separate_features_and_labels(data):
    Y = data.label.to_numpy()
    X = data.drop(columns="label").to_numpy()
    return X, Y
