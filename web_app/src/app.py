import streamlit as st
from streamlit_drawable_canvas import st_canvas
from utils.prediction_logger import log_prediction
from utils.client import send_prediction_request
from utils.db import fetch_all_predictions

st.set_page_config(
    page_title="MNIST Digit Classifier",
    layout="wide"
)

# Initialize session state variables if they don't exist
if 'prediction' not in st.session_state:
    st.session_state.prediction = {"confidence": {}, "prediction": "N/A"}
if 'predicted_digit' not in st.session_state:
    st.session_state.predicted_digit = "N/A"


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
                    st.session_state.prediction = send_prediction_request(
                        img_data)
                    if "prediction" in st.session_state.prediction:
                        st.session_state.predicted_digit = (
                            st.session_state.prediction["prediction"]
                        )

    with cols[1]:
        # Get predictions dictionary
        predictions = st.session_state.prediction.get("confidence", {})
        subcols = st.columns([2, 1, 1])
        with subcols[0]:
            st.subheader("Prediction Results")
        with subcols[1]:
            st.markdown("")
            st.markdown(
                f"Predicted Digit: **{st.session_state.predicted_digit}**")
        with subcols[2]:
            confidence = predictions.get(
                st.session_state.predicted_digit, "N/A")
            if confidence != "N/A":
                confidence = f"{round(confidence, 0):.0f}%"
            st.markdown("")
            st.markdown(f"Confidence Score: **{confidence}**")

        # Show bar chart of predictions if available
        if predictions:
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
                    # Only log if we have a valid prediction
                    if st.session_state.predicted_digit != "N/A" and (
                        st.session_state.predicted_digit in predictions
                    ):
                        # Log the prediction along with the true label
                        log_prediction(
                            int(st.session_state.predicted_digit),
                            predictions[st.session_state.predicted_digit]/100,
                            int(true_label)
                        )
                        st.success(
                            f"True Label accepted and logged: {true_label}")
                    else:
                        st.warning(
                            "No valid prediction to log. "
                            "Please classify a digit first."
                        )
                except Exception as e:
                    st.error(f"Failed to log prediction: {e}")
            else:
                st.error("Invalid input. Please enter a digit from 0-9.")


    # Display all logged predictions from the database
    st.subheader("Logged Predictions")
    predictions_table = fetch_all_predictions()
    if predictions_table:
        from datetime import datetime
        for record in predictions_table:
            # record columns: id, timestamp, predicted_digit, confidence_score, true_label
            try:
                dt = datetime.fromisoformat(record[1])
            except Exception:
                dt = record[1]
            if isinstance(dt, datetime):
                ts_formatted = dt.strftime("%-d %b. %Y %H:%M")
            else:
                ts_formatted = record[1]
            predicted_str = f"Predicted: {record[2]}"
            actual_str = f"Actual: {record[4]}"
            conf_str = f"Confidence: {round(record[3], 0):.0f}%"
            line = f"{ts_formatted} {predicted_str} {actual_str} {conf_str}"
            st.write(line)
    else:
        st.info("No predictions logged yet.")

if __name__ == "__main__":
    main()
