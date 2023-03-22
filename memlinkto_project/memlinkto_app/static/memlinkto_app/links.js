let deleteButtons = document.querySelectorAll(".btn-delete");
for (let i = 0; i < deleteButtons.length; i++) {
    deleteButtons[i].addEventListener('click', function (evt) {
        deleteFromServer(evt);
    }, false);
}

function deleteFromServer(evt) {
    let shortUrl = evt.currentTarget.id.replace("btn_", "");
    // Send a backend request
    fetch('/rpc/', {
        method: 'POST',
        body: JSON.stringify({
            id: '1',
            jsonrpc: '2.0',
            method: 'delete_link',
            params: [shortUrl]
        }),
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(json => {
        deleteFromTable(evt);
    });
}

function deleteFromTable(evt) {
    let tr = evt.target.parentNode.parentNode;
    if (tr.nodeName !== 'TR') {
        tr = tr.parentNode;
    }
    let tbody = tr.parentNode;
    tbody.removeChild(tr);
}