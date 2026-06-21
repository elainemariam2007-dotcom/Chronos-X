async function sendMessage(){
    addAgentLog(
    "Planner Agent",
    "Analyzing mission..."
);

setTimeout(() => {
    addAgentLog(
        "Risk Agent",
        "Evaluating risks..."
    );
}, 500);

setTimeout(() => {
    addAgentLog(
        "Task Agent",
        "Generating tasks..."
    );
}, 1000);

setTimeout(() => {
    addAgentLog(
        "Automation Agent",
        "Preparing workflows..."
    );
}, 1500);

let input =
document.getElementById("user-input");

let message =
input.value;

if(message==="") return;

let response =
await fetch("/chat",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
message:message
})

});

let data =
await response.json();

speak(data.response);

let chatBox =
document.getElementById("chat-box");

chatBox.innerHTML += `
<div class="user-msg">
${message}
</div>

<div class="bot-msg">
${data.response}
</div>
`;

input.value="";
}
async function uploadPDF(){

    let fileInput =
    document.getElementById("pdfFile");

    let file =
    fileInput.files[0];

    if(!file){
        alert("Choose a PDF");
        return;
    }

    let formData =
    new FormData();

    formData.append(
        "file",
        file
    );

    let response =
    await fetch(
        "/analyze-pdf",
        {
            method:"POST",
            body:formData
        }
    );

    let data =
    await response.json();

    document
    .getElementById("chat-box")
    .innerHTML +=

    `<div class="bot-msg">
    <b>PDF ANALYSIS</b><br>
    ${data.analysis}
    </div>`;
}
function startVoice(){

const recognition =
new(window.SpeechRecognition ||
window.webkitSpeechRecognition)();

recognition.lang="en-US";

recognition.start();

recognition.onresult=
function(event){

let transcript =
event.results[0][0].transcript;

document
.getElementById("user-input")
.value = transcript;

sendMessage();

};

}
function speak(text){

let speech =
new SpeechSynthesisUtterance(
text
);

speech.rate = 1;

speech.pitch = 1;

window.speechSynthesis
.speak(speech);

}
// ENTER TO SEND

document
.getElementById("user-input")
.addEventListener(
    "keydown",
    function(event){

        if(event.key === "Enter"){

            event.preventDefault();

            sendMessage();
        }
    }
);
function startVoice(){

    if(
        !('webkitSpeechRecognition' in window) &&
        !('SpeechRecognition' in window)
    ){
        alert("Speech Recognition not supported");
        return;
    }

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    const recognition =
        new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.interimResults = false;

    recognition.start();

    recognition.onresult = function(event){

        const transcript =
            event.results[0][0].transcript;

        document
        .getElementById("user-input")
        .value = transcript;

        sendMessage();
    };

    recognition.onerror = function(event){

        console.log(event.error);

        alert(
            "Microphone Error: " +
            event.error
        );
    };
}
function addAgentLog(agent, message){

    const feed =
        document.getElementById(
            "agent-feed-content"
        );

    const row =
        document.createElement("div");

    row.innerHTML =
        `[${agent}] ${message}`;

    feed.appendChild(row);

    feed.scrollTop =
        feed.scrollHeight;
}
function demoMode(){

    addAgentLog(
        "Planner Agent",
        "Mission detected"
    );

    addAgentLog(
        "Risk Agent",
        "Deadline identified"
    );

    addAgentLog(
        "Task Agent",
        "Created 5 subtasks"
    );

    addAgentLog(
        "Automation Agent",
        "Calendar workflow ready"
    );

    document.getElementById(
        "mission-card"
    ).innerHTML = `
        <div class="mission-item">
        Objective: Build AI Frontend
        </div>

        <div class="mission-item">
        ✓ UI Design
        </div>

        <div class="mission-item">
        ✓ Components
        </div>

        <div class="mission-item">
        ✓ API Integration
        </div>

        <div class="mission-item">
        ✓ Testing
        </div>

        <div class="mission-item">
        Risk: Medium
        </div>
    `;
}
if (
    task.includes("task") ||
    task.includes("todo")
){
    category = "TASK";
    automation = "TASK";
}
async function activateAuto(){

    let response =
    await fetch("/auto-mode");

    let data =
    await response.json();

    let chatBox =
    document.getElementById("chat-box");

    chatBox.innerHTML += `
    <div class="bot-msg">
    ${data.message}
    </div>
    `;
}