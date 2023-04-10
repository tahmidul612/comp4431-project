//setup before functions
let typingTimer;                //timer identifier
let doneTypingInterval = 2_000;  //time in ms, 2 seconds for example
let inputLongUrl = document.querySelector('#inputLongUrl');
let lastValue = "";

//on keyup, start the countdown
inputLongUrl.addEventListener('keyup', function () {
  clearTimeout(typingTimer);
  if (inputLongUrl.value && lastValue != inputLongUrl.value) {
    showSpinner();
    typingTimer = setTimeout(doneTyping, doneTypingInterval);
  }
});

//on keydown, clear the countdown
inputLongUrl.addEventListener('keydown', function () {
  hideWarning();
  hideSuccess();
  clearTimeout(typingTimer);
});

function isValidUrl(string) {
  try {
    new URL(string);
    return true;
  } catch (err) {
    return false;
  }
}

function showWarning() {
  document.querySelector("#divWarning").classList.remove("d-none");
  hideSuccess();
}

function hideWarning() {
  document.querySelector("#divWarning").classList.add("d-none");
}

function showSuccess() {
  document.querySelector("#divSuccess").classList.remove("d-none");
  hideWarning();
}

function hideSuccess() {
  document.querySelector("#divSuccess").classList.add("d-none");
}

function showSpinner() {
  document.querySelector('#divSpinner').classList.remove("invisible");
}

function hideSpinner() {
  document.querySelector('#divSpinner').classList.add("invisible");
}

//user is "finished typing," do something
function doneTyping() {

  if (!isValidUrl(inputLongUrl.value)) {
    showWarning();
    hideSpinner();
    return;
  }
  fetch('/rpc/', {
    method: 'POST',
    body: JSON.stringify({
      id: '1',
      jsonrpc: '2.0',
      method: 'link_is_safe',
      params: [inputLongUrl.value]
    }),
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json"
    }
  }).then(res => res.json()).then(json => {
    if (json.result != "safe") {
      showWarning();
      hideSpinner();
      return;
    }
    else {
      lastValue = inputLongUrl.value;

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
        let divLongUrl = document.querySelector('#divLongUrl');
        divLongUrl.innerHTML = lastValue;
        hideSpinner();
        showSuccess();
      });
    }
  });
}