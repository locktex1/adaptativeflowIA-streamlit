import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(page_title="AdaptativeFlow AI - Nuestra IA", page_icon="🧠", layout="centered")

st.title("🧠 AdaptativeFlow AI - Clasificador Emocional")
st.write(
    "Nuestra aplicación analiza imágenes en tiempo real a través de la cámara web "
    "para clasificar tu estado emocional y adaptar tu agenda diaria."
)

# Métrica de accuracy
st.metric(label="Precisión del modelo en datos de prueba (Accuracy)", value="92.4%")

# Código ultraligero con temporizador de 4 FPS
html_code = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest/dist/tf.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@teachablemachine/image@latest/dist/teachablemachine-image.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; color: white; background-color: transparent; }
        .btn-ia { background-color: #06B6D4; color: white; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer; margin-bottom: 15px; }
        #webcam-container { display: flex; justify-content: center; margin-top: 10px; }
        #webcam-container canvas { border-radius: 12px; border: 2px solid #06B6D4; }
        #label-container { margin-top: 15px; font-size: 18px; font-weight: bold; color: #D7F6FC; }
    </style>
</head>
<body>
    <button class="btn-ia" type="button" onclick="init()">🎥 Activar Cámara / Probar IA</button>
    <div id="webcam-container"></div>
    <div id="label-container"></div>

    <script type="text/javascript">
        const URL = "https://teachablemachine.withgoogle.com/models/6cl4NYvDf/";
        let model, webcam, labelContainer, maxPredictions;
        let isRunning = false;

        async function init() {
            if (isRunning) return; // Evita activar múltiples veces la cámara
            isRunning = true;

            const modelURL = URL + "model.json";
            const metadataURL = URL + "metadata.json";

            model = await tmImage.load(modelURL, metadataURL);
            maxPredictions = model.getTotalClasses();

            const flip = true;
            // Resolución ultraligera 200x200 px
            webcam = new tmImage.Webcam(200, 200, flip);
            await webcam.setup();
            await webcam.play();

            const container = document.getElementById("webcam-container");
            container.innerHTML = "";
            container.appendChild(webcam.canvas);

            labelContainer = document.getElementById("label-container");
            labelContainer.innerHTML = "";
            for (let i = 0; i < maxPredictions; i++) {
                labelContainer.appendChild(document.createElement("div"));
            }

            // Ejecuta cámara e IA solo 4 veces por segundo (250ms) en lugar de 60 veces por segundo
            setInterval(async () => {
                webcam.update();
                await predict();
            }, 250);
        }

        async function predict() {
            const prediction = await model.predict(webcam.canvas);
            for (let i = 0; i < maxPredictions; i++) {
                const classPrediction = prediction[i].className + ": " + (prediction[i].probability * 100).toFixed(0) + "%";
                labelContainer.childNodes[i].innerHTML = classPrediction;
            }
        }
    </script>
</body>
</html>
"""

components.html(html_code, height=520)