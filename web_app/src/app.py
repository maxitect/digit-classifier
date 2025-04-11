import streamlit as st
from streamlit_drawable_canvas import st_canvas


st.set_page_config(
    page_title="MNIST Digit Classifier",
    layout="wide"
)


def main():
    st.title("MNIST Digit Classifier")
    st.markdown(
        "This application allows you to draw a digit on the canvas and then "
        "uses a trained CNN model to classify the digit. It also displays "
        "the prediction results and allows you to input the true label."
    )

    st.subheader("Drawing Canvas")

    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0.0)",  # Transparent background
        stroke_width=15,  # Brush size
        stroke_color="#FFFFFF",  # White brush
        background_color="#000000",  # Black background (MNIST-like)
        width=280,  # Canvas width (MNIST size)
        height=280,  # Canvas height (MNIST size)
        drawing_mode="freedraw",
        key="canvas",
    )

    # Add a classify button
    if st.button("Classify Digit"):
        if canvas_result.image_data is not None:
            # Convert the image data to grayscale
            img_data = canvas_result.image_data
            if img_data is not None and img_data.shape[0] > 0:
                st.write("Image captured! Ready to send to model service.")
                # This is where you would send the image to the model service
                # For now, just display a placeholder for the model response

    st.subheader("Prediction Results")
    # Placeholder predictions dictionary for demo purposes (replace with actual predictions)
    predictions = {
        '0': 0.05,
        '1': 0.1,
        '2': 0.05,
        '3': 0.6,
        '4': 0.05,
        '5': 0.05,
        '6': 0.02,
        '7': 0.04,
        '8': 0.02,
        '9': 0.02
    }
    # Determine predicted digit
    predicted_digit = max(predictions, key=predictions.get)
    st.markdown(f"### Predicted Digit: **{predicted_digit}**")
    st.bar_chart(predictions)

    st.subheader("Input True Label")
    true_label = st.text_input("Enter the true label (0-9):")
    if true_label:
        st.write("True Label:", true_label)


if __name__ == "__main__":
    main()
