import streamlit as st
import streamlit.components.v1 as components

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
    canvas_html = """
<style>
  #canvas {
      border: 1px solid #000;
      touch-action: none;
      width: 280px;
      height: 280px;
  }
</style>
<canvas id="canvas" width="280" height="280"></canvas>
<br>
<button onclick="clearCanvas()">Clear</button>
<script>
var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");
var drawing = false;
canvas.addEventListener("mousedown", function(e) {
    drawing = true;
    ctx.beginPath();
    ctx.moveTo(e.offsetX, e.offsetY);
});
canvas.addEventListener("mousemove", function(e) {
    if (drawing) {
        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.stroke();
    }
});
canvas.addEventListener("mouseup", function(e) {
    drawing = false;
});
canvas.addEventListener("mouseleave", function(e) {
    drawing = false;
});
function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}
</script>
"""
    components.html(canvas_html, height=350)

    st.subheader("Prediction Results")
    st.text("Predicted digit and confidence scores will be shown here.")

    st.subheader("Input True Label")
    true_label = st.text_input("Enter the true label (0-9):")
    if true_label:
        st.write("True Label:", true_label)


if __name__ == "__main__":
    main()
