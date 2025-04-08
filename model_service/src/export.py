import torch
from torchvision import transforms
import argparse
from model import MNISTCNN

def preprocess_input(image):
    """
    Preprocess a raw PIL image into a normalized tensor suitable for inference.
    """
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    # Add a batch dimension
    return transform(image).unsqueeze(0)

def export_model(model_checkpoint, export_path, device):
    """
    Loads a trained model checkpoint, converts it to TorchScript, and exports it.
    """
    model = MNISTCNN().to(device)
    model.load_state_dict(torch.load(model_checkpoint, map_location=device))
    model.eval()
    # Convert the model to TorchScript via scripting for inference
    scripted_model = torch.jit.script(model)
    scripted_model.save(export_path)
    print(f"Model exported to {export_path}")
    
def main():
    parser = argparse.ArgumentParser(description="Export MNIST CNN model for inference")
    parser.add_argument(
        '--checkpoint',
        type=str,
        default='model_service/src/best_model.pth',
        help='Path to the trained model checkpoint'
    )
    parser.add_argument(
        '--export-path',
        type=str,
        default='model_service/src/exported_model.pt',
        help='Path to save the exported model'
    )
    args = parser.parse_args()
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    export_model(args.checkpoint, args.export_path, device)

if __name__ == "__main__":
    main()
