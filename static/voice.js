// const audioContext = new AudioContext();

// var recordButton = document.getElementById("recorder");

// recordButton.addEventListener("click", startRecording);




document.getElementById("recordBtn").addEventListener("click", startRecording);

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(function(stream) {


      // Use the stream object to access the audio data

        const mediaRecorder = new MediaRecorder(stream);


        mediaRecorder.start();

        const audioChunks = [];

        mediaRecorder.addEventListener("dataavailable", event => {
            audioChunks.push(event.data);
        });
        
        mediaRecorder.addEventListener("stop", () => {
        const audioBlob = new Blob(audioChunks);
        const audioUrl = URL.createObjectURL(audioBlob);
        document.getElementById("recorder").src = audioUrl;
    
        });
        
        setTimeout(() => {
            mediaRecorder.stop();
        }, 5000);

    });
  }