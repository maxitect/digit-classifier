import streamlit as st
from streamlit_drawable_canvas import st_canvas
from prediction_logger import log_prediction


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

    cols = st.columns([1, 3])
    with cols[0]:
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
                    # This is where you would send the image to model service
                    # For now, just display a placeholder for model response
    with cols[1]:
        # Placeholder predictions dictionary for demo purposes
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
        subcols = st.columns([1, 1])
        with subcols[0]:
            st.subheader("Prediction Results")
        with subcols[1]:
            predicted_digit = max(predictions, key=predictions.get)
            st.markdown(f"### Predicted Digit: **{predicted_digit}**")

        # Determine predicted digit
        st.bar_chart(predictions)

    st.subheader("Input True Label")
    with st.form(key="true_label_form"):
        true_label = st.text_input("Enter the true label (0-9):")
        submit_true_label = st.form_submit_button("Submit True Label")
        if submit_true_label:
            if (true_label.isdigit() and
                    int(true_label) >= 0 and
                    int(true_label) <= 9):
                try:
                    # Log the prediction along with the true label
                    log_prediction(
                        int(predicted_digit),
                        predictions[predicted_digit],
                        int(true_label)
                    )
                    st.success(f"True Label accepted and logged: {true_label}")
                except Exception as e:
                    st.error(f"Failed to log prediction: {e}")
            else:
                st.error("Invalid input. Please enter a digit from 0-9.")


if __name__ == "__main__":
    main()
