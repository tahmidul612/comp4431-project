//setup before functions
let typingTimer;                //timer identifier
let doneTypingInterval = 5_000;  //time in ms, 5 seconds for example
let inputLongUrl = document.querySelector('#inputLongUrl');

//on keyup, start the countdown
inputLongUrl.addEventListener('keyup', function () {
    let divSpinner = document.querySelector('#divSpinner');
    divSpinner.classList.remove("invisible");
    clearTimeout(typingTimer);
    typingTimer = setTimeout(doneTyping, doneTypingInterval);
});

//on keydown, clear the countdown
inputLongUrl.addEventListener('keydown', function () {
    clearTimeout(typingTimer);
});

//user is "finished typing," do something
function doneTyping() {
    // Send a backend request
    fetch('/rpc/', {
        method: 'POST',
        body: JSON.stringify({
            id: '1',
            jsonrpc: '2.0',
            method: 'create_link',
            params: [inputLongUrl.value]
        }),
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(json => {
        let anchorShortUrl = document.querySelector('#anchorShortUrl');
        anchorShortUrl.setAttribute("href", json.result);
        anchorShortUrl.innerHTML = json.result;
        let divSpinner = document.querySelector('#divSpinner');
        divSpinner.classList.add("invisible");
    })
}