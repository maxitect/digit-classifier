import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import argparse
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
from model import MNISTCNN

def get_test_loader(batch_size=64, download=True):
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    test_dataset = datasets.MNIST(root='./data', train=False, download=download, transform=transform)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    return test_loader

def evaluate(model, device, test_loader):
    model.eval()
    all_preds = []
    all_targets = []
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            outputs = model(data)
            preds = outputs.argmax(dim=1)
            all_preds.extend(preds.cpu().numpy())
            all_targets.extend(target.cpu().numpy())
    all_preds = np.array(all_preds)
    all_targets = np.array(all_targets)
    acc = accuracy_score(all_targets, all_preds)
    prec = precision_score(all_targets, all_preds, average='weighted', zero_division=0)
    rec = recall_score(all_targets, all_preds, average='weighted', zero_division=0)
    cm = confusion_matrix(all_targets, all_preds)
    return acc, prec, rec, cm

def main():
    parser = argparse.ArgumentParser(description="Evaluate MNIST CNN model")
    parser.add_argument('--checkpoint', type=str, default='model_service/src/best_model.pth', help='Path to model checkpoint')
    parser.add_argument('--batch-size', type=int, default=64, help='Batch size for evaluation')
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = MNISTCNN().to(device)
    model.load_state_dict(torch.load(args.checkpoint, map_location=device))
    
    test_loader = get_test_loader(batch_size=args.batch_size)
    
    acc, prec, rec, cm = evaluate(model, device, test_loader)
    
    print(f"Accuracy: {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall: {rec:.4f}")
    print("Confusion Matrix:")
    print(cm)
    
    if acc < 0.85:
        print("Warning: Model accuracy is below 85%")
    else:
        print("Model meets the accuracy requirement of at least 85%")

if __name__ == "__main__":
    main()
