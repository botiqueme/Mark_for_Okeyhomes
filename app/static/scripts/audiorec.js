let mediaRecorder;
let audioChunks = [];
let isRecording = false;
let startDelay;

async function toggleRecording() {
    const recordButton = document.getElementById('recordButton');

    if (!isRecording) {
        // Introduci un leggero ritardo prima di iniziare la registrazione
        startDelay = setTimeout(async () => {
            audioChunks = [];
            stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = () => {
                sendAudio();
                stopStream();
                recordButton.classList.remove("recording");
            };

            mediaRecorder.start();
            recordButton.classList.add("recording");
        }, 250); // Ritardo di 250 millisecondi

        isRecording = true;
    } else {
        clearTimeout(startDelay); // Cancella il ritardo se il pulsante viene rilasciato rapidamente
        if (mediaRecorder && mediaRecorder.state === "recording") {
            mediaRecorder.stop();
        }
        isRecording = false;
    }
}

function sendAudio() {
    document.querySelector('.typing_dots').style.display = 'flex';

    const audioBlob = new Blob(audioChunks, {type: 'audio/wav'});
    const audioUrl = URL.createObjectURL(audioBlob); // Crea un URL per il Blob
    const formData = new FormData();
    formData.append("audio_message", audioBlob);

    appendAudioMessage(PERSON_NAME, PERSON_IMG, "right", audioUrl);

    fetch("/get", {
        method: "POST",
        body: formData
    }).then(response => {
        const contentType = response.headers.get("content-type");

        if (contentType && contentType.includes("audio")) {
            return response.blob().then(blob => {
                document.querySelector('.typing_dots').style.display = 'none';

                const audioUrlback = URL.createObjectURL(blob);
                appendAudioMessage(BOT_NAME, BOT_IMG, "left", audioUrlback);
            });
        } else {
            return response.text().then(text => {
                document.querySelector('.typing_dots').style.display = 'none';

                appendMessage(BOT_NAME, BOT_IMG, "left", text);
            });
        }
    }).catch(error => {
        console.error("Errore nella ricezione della risposta:", error);
    });

}

function appendAudioMessage(name, img, side, audioUrl) {
    const msgHTML = `
<div class="msg ${side}-msg">
  <div class="msg-img" style="background-image: url(${img})"></div>

  <div class="msg-bubble">
    <div class="msg-info">
      <div class="msg-info-name">${name}</div>
      <div class="msg-info-time">${formatDate(new Date())}</div>
    </div>

    <div class="msg-text">
      <audio controls class="audio-message">
        <source src="${audioUrl}" type="audio/wav">
        Il tuo browser non supporta l'elemento audio.
      </audio>
    </div>
  </div>
</div>
`;
    msgerChat.insertAdjacentHTML("beforeend", msgHTML);
    msgerChat.scrollTop += 500;
}

function stopStream() {
    if (mediaRecorder) {
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
    }
    mediaRecorder = null;
    stream = null;
}

function preventDefaultAction(event) {
    event.preventDefault();
    toggleRecording();
}

document.getElementById('recordButton').addEventListener('mousedown', preventDefaultAction);
document.getElementById('recordButton').addEventListener('touchstart', preventDefaultAction);

// Ascolta mouseup e touchend sull'intero documento
document.addEventListener('mouseup', event => {
    if (isRecording) {
        toggleRecording();
    }
});
document.addEventListener('touchend', event => {
    if (isRecording) {
        toggleRecording();
    }
});
