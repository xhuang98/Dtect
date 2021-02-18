import numpy as np
import torch
from tqdm import tqdm
from model import *
from dataset import *
import data_config


def train(model, data, epochs, save_dir):
    """
    Train model using MSE loss. Weights are saved each epoch.

    :param model: model instance
    :param data: iterable data
    :param epochs: number of epochs to train
    :param save_dir: Directory to save weights
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
    model = model.to(device)
    for epoch in range(epochs):
        print(f'Epoch: {epoch}')
        loss = 0
        dataset_iter = iter(data)
        with tqdm(total=len(data)) as progress_bar:
            for input_numpy in dataset_iter:
                progress_bar.update(1)
                input_tensor = torch.from_numpy(input_numpy).to(device)
                output = model(input_tensor.float()).double()
                train_loss = criterion(output, input_tensor)
                train_loss.backward()
                optimizer.step()
                loss += train_loss.item()
        loss /= len(data)
        print(f'Loss: {loss}')
        save_path = os.path.join(save_dir, f"model_{epoch}.pth")
        torch.save(model.state_dict(), save_path)


if __name__ == '__main__':
    dataset = Dataset(dir_path="D:\\los alamos\\auths\\train", window_size=data_config.window_size,
                      user_map_path=data_config.user_map_path, computer_map_path=data_config.computer_map_path,
                      auth_type_map_path=data_config.auth_type_map_path,
                      logon_type_map_path=data_config.logon_type_map_path)
    ae = AutoEncoder(input_shape=dataset.get_encoding_len())
    train(ae, dataset, 10, "../snapshots")
