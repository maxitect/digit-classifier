import streamlit as st

st.set_page_config(
    page_title="MNIST Digit Classifier",
    layout="wide"
)

def main():
    st.title("MNIST Digit Classifier")
    st.markdown("This application allows you to draw a digit on the canvas and then uses a trained CNN model to classify the digit. It also displays the prediction results and allows you to input the true label.")
    
    st.subheader("Drawing Canvas")
    st.text("Drawing canvas will be implemented here.")
    
    st.subheader("Prediction Results")
    st.text("Predicted digit and confidence scores will be shown here.")
    
    st.subheader("Input True Label")
    true_label = st.text_input("Enter the true label (0-9):")
    if true_label:
        st.write("True Label:", true_label)

if __name__ == "__main__":
    main()
