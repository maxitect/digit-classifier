from torchvision import datasets, transforms
from torch.utils.data import DataLoader


def get_data_loaders(batch_size=64, download=True):
    """
    Downloads the MNIST dataset and creates data loaders for training and
    testing. Applies normalisation and necessary transformations.
    """
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))  # Mean and std for MNIST
    ])

    train_dataset = datasets.MNIST(
        root='./data',
        train=True,
        download=download,
        transform=transform
    )

    test_dataset = datasets.MNIST(
        root='./data',
        train=False,
        download=download,
        transform=transform
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False
    )

    return train_loader, test_loader


if __name__ == "__main__":
    train_loader, test_loader = get_data_loaders()
    print("Number of training batches:", len(train_loader))
    print("Number of testing batches:", len(test_loader))
