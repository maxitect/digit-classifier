import torch
import torch.nn as nn
import torch.optim as optim
from model_service.src.data_loader import get_data_loaders
from model_service.src.model import MNISTCNN

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
    # Settings
    batch_size = 64
    num_epochs = 20
    early_stopping_patience = 3
    learning_rate = 0.001

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
        valid_loss, valid_accuracy = validate(model, device, valid_loader, criterion)
        print(f"Epoch {epoch}: Train Loss: {train_loss:.4f}, Valid Loss: {valid_loss:.4f}, Valid Acc: {valid_accuracy:.4f}")

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
