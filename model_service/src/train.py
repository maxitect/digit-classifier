import torch
import torch.nn as nn
import torch.optim as optim
from src.data_loader import get_data_loaders
from src.model import MNISTCNN
import argparse
import os
from src.config import settings


def train(model, device, train_loader, optimizer, criterion):
    model.train()
    running_loss = 0.0
    for data, target in train_loader:
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        outputs = model(data)
        loss = criterion(outputs, target)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * data.size(0)
    epoch_loss = running_loss / len(train_loader.dataset)
    return epoch_loss


def validate(model, device, valid_loader, criterion):
    model.eval()
    running_loss = 0.0
    correct = 0
    with torch.no_grad():
        for data, target in valid_loader:
            data, target = data.to(device), target.to(device)
            outputs = model(data)
            loss = criterion(outputs, target)
            running_loss += loss.item() * data.size(0)
            pred = outputs.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()
    epoch_loss = running_loss / len(valid_loader.dataset)
    accuracy = correct / len(valid_loader.dataset)
    return epoch_loss, accuracy


def main():
    parser = argparse.ArgumentParser(description="Train MNIST CNN model")
    parser.add_argument(
        '--batch-size',
        type=int,
        default=64,
        help='Batch size for training'
    )
    parser.add_argument(
        '--num-epochs',
        type=int,
        default=20,
        help='Number of training epochs'
    )
    parser.add_argument(
        '--patience',
        type=int,
        default=3,
        help='Early stopping patience'
    )
    parser.add_argument(
        '--lr',
        type=float,
        default=0.001,
        help='Learning rate'
    )
    parser.add_argument(
        '--checkpoint-dir',
        type=str,
        default=settings.checkpoint_dir,
        help='Directory to save checkpoints'
    )
    args = parser.parse_args()

    batch_size = args.batch_size
    num_epochs = args.num_epochs
    early_stopping_patience = args.patience
    learning_rate = args.lr

    os.makedirs(args.checkpoint_dir, exist_ok=True)
    # Create a CSV log file for training metrics
    log_file = os.path.join(args.checkpoint_dir, "training_log.csv")
    with open(log_file, "w") as f:
        f.write("epoch,train_loss,valid_loss,valid_accuracy\n")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load data
    train_loader, test_loader = get_data_loaders(batch_size=batch_size)
    # For simplicity, using test_loader as validation loader in this example.
    valid_loader = test_loader

    model = MNISTCNN().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    best_accuracy = 0.0
    epochs_without_improvement = 0

    for epoch in range(1, num_epochs + 1):
        train_loss = train(model, device, train_loader, optimizer, criterion)
        valid_loss, valid_accuracy = validate(
            model, device,
            valid_loader,
            criterion
        )
        print(
            f"Epoch {epoch}: Train Loss: {train_loss:.4f}, "
            f"Valid Loss: {valid_loss:.4f}, Valid Acc: {valid_accuracy:.4f}"
        )
        # Save checkpoint for this epoch
        checkpoint_path = os.path.join(
            args.checkpoint_dir, f"epoch_{epoch}.pth")
        torch.save(model.state_dict(), checkpoint_path)
        # Log metrics to CSV file
        with open(log_file, "a") as f:
            f.write(
                f"{epoch},{train_loss:.4f},"
                f"{valid_loss:.4f},{valid_accuracy:.4f}\n"
            )

        if valid_accuracy > best_accuracy:
            best_accuracy = valid_accuracy
            epochs_without_improvement = 0
            # Save the best model
            torch.save(model.state_dict(), "model_service/src/best_model.pth")
            print("Validation accuracy improved, saving model.")
        else:
            epochs_without_improvement += 1
            if epochs_without_improvement >= early_stopping_patience:
                print("Early stopping triggered.")
                break


if __name__ == "__main__":
    main()
