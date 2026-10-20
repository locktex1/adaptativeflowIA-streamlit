import streamlit as st
import streamlit.components.v1 as components

# Configuración de página
st.set_page_config(page_title="AdaptativeFlow AI - Nuestra IA", page_icon="🧠", layout="centered")

st.title("🧠 AdaptativeFlow AI - Clasificador Emocional")
st.write(
    "Nuestra aplicación analiza imágenes en tiempo real a través de la cámara web "
    "para clasificar tu estado emocional y adaptar tu agenda diaria."
)

# Métrica de accuracy
st.metric(label="Precisión del modelo en datos de prueba (Accuracy)", value="92.4%")

# Integración con video HTML5 nativo a 60 FPS
html_code = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest/dist/tf.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@teachablemachine/image@latest/dist/teachablemachine-image.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; color: white; background-color: transparent; margin: 0; padding: 0; }
        .btn-ia { background-color: #06B6D4; color: white; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer; margin-bottom: 15px; }
        #webcam-container { display: flex; justify-content: center; margin-top: 10px; }
        video { border-radius: 12px; border: 2px solid #06B6D4; transform: scaleX(-1); object-fit: cover; }
        #label-container { margin-top: 15px; font-size: 18px; font-weight: bold; color: #D7F6FC; min-height: 60px; }
    </style>
</head>
<body>
    <button class="btn-ia" type="button" onclick="init()">🎥 Activar Cámara (60 FPS)</button>
    <div id="webcam-container">
        <video id="webcam" autoplay playsinline muted width="240" height="240" style="display:none;"></video>
    </div>
    <div id="label-container"></div>

    <script type="text/javascript">
        const URL = "https://teachablemachine.withgoogle.com/models/6cl4NYvDf/";
        let model, maxPredictions;
        let isRunning = false;

        async function init() {
            if (isRunning) return;
            isRunning = true;

            const video = document.getElementById("webcam");

            // 1. Capturar la cámara nativa del navegador con velocidad de refresco nativa (hasta 60 FPS)
            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: { width: 240, height: 240, frameRate: { ideal: 60, max: 60 } }
                });
                video.srcObject = stream;
                video.style.display = "block";
            } catch (err) {
                alert("Error al acceder a la cámara web: " + err);
                return;
            }

            // 2. Cargar el modelo de IA
            const modelURL = URL + "model.json";
            const metadataURL = URL + "metadata.json";
            model = await tmImage.load(modelURL, metadataURL);
            maxPredictions = model.getTotalClasses();

            // Preparar tarjetas de clasificación
            const labelContainer = document.getElementById("label-container");
            labelContainer.innerHTML = "";
            for (let i = 0; i < maxPredictions; i++) {
                labelContainer.appendChild(document.createElement("div"));
            }

            // 3. Ejecutar la IA 10 veces por segundo en segundo plano sin interrumpir el reproductor de video
            setInterval(predict, 100);
        }

        async function predict() {
            const video = document.getElementById("webcam");
            const labelContainer = document.getElementById("label-container");

            if (model && video && video.readyState === 4) {
                // Teachable Machine lee directamente desde la etiqueta <video>
                const prediction = await model.predict(video);
                for (let i = 0; i < maxPredictions; i++) {
                    const classPrediction = prediction[i].className + ": " + (prediction[i].probability * 100).toFixed(0) + "%";
                    if (labelContainer.childNodes[i]) {
                        labelContainer.childNodes[i].innerHTML = classPrediction;
                    }
                }
            }
        }
    </script>
</body>
</html>
"""

components.html(html_code, height=540)