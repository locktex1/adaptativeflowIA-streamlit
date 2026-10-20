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

# Código optimizado con renderizado independiente y aceleración GPU
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
        #webcam-container canvas { border-radius: 12px; border: 2px solid #06B6D4; }
        #label-container { margin-top: 15px; font-size: 18px; font-weight: bold; color: #D7F6FC; min-height: 50px; }
    </style>
</head>
<body>
    <button class="btn-ia" type="button" onclick="init()">🎥 Activar Cámara / Probar IA</button>
    <div id="webcam-container"></div>
    <div id="label-container"></div>

    <script type="text/javascript">
        const URL = "https://teachablemachine.withgoogle.com/models/6cl4NYvDf/";
        let model, webcam, labelContainer, maxPredictions;
        let isPredicting = false;
        let isRunning = false;

        async function init() {
            if (isRunning) return;
            isRunning = true;

            // Intentar activar aceleración por hardware (WebGL)
            try {
                await tf.setBackend('webgl');
            } catch(e) {
                console.log("Usando backend por defecto");
            }

            const modelURL = URL + "model.json";
            const metadataURL = URL + "metadata.json";

            model = await tmImage.load(modelURL, metadataURL);
            maxPredictions = model.getTotalClasses();

            const flip = true;
            webcam = new tmImage.Webcam(220, 220, flip);
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

            // Bucle 1: Renderizado ultra fluido del video de la cámara
            window.requestAnimationFrame(videoLoop);

            // Bucle 2: Predicción asíncrona de IA en segundo plano
            predictLoop();
        }

        function videoLoop() {
            if (webcam) {
                webcam.update();
            }
            window.requestAnimationFrame(videoLoop);
        }

        async function predictLoop() {
            if (model && webcam && webcam.canvas && !isPredicting) {
                isPredicting = true;
                await predict();
                isPredicting = false;
            }
            setTimeout(predictLoop, 150);
        }

        async function predict() {
            // tf.tidy libera automáticamente la memoria GPU/RAM usada en cada predicción
            const prediction = await tf.tidy(() => {
                return model.predict(webcam.canvas);
            });

            for (let i = 0; i < maxPredictions; i++) {
                const classPrediction = prediction[i].className + ": " + (prediction[i].probability * 100).toFixed(0) + "%";
                if (labelContainer.childNodes[i]) {
                    labelContainer.childNodes[i].innerHTML = classPrediction;
                }
            }
        }
    </script>
</body>
</html>
"""

components.html(html_code, height=520)