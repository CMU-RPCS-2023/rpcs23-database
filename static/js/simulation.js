SERVER = 'https://fwo91hdzog.execute-api.us-east-1.amazonaws.com/test/dynamodbmanager'

function ajaxSetting(api, data) {
    setting = {
        "async": true,
        "crossDomain": true,
        "url": SERVER + api,
        "method": "POST",
        "headers": {
            "content-type": "application/json",
        },
        "processData": false,
        "data": JSON.stringify(data),
        "cors": true
    }
    return setting
}

window.onload = function ()
{
    const data = {
        'operation': 'echo',
        'payload': 'server is ok'
    };
    console.log(data)
    $.ajax(ajaxSetting('', data)).done(function(response) {
        console.log(response)
        if (response !== 'server is ok') {
            document.getElementById('server-check-warning').style.display = 'block'
        }
    }).catch(function(error) {
        console.log(error)
        document.getElementById('server-check-warning').style.display = 'block'
    })
}

$('#get_simulation_btn').on('click', function(ev) {
    console.log(ev.target)
    payload = JSON.parse($("#get_simulation")[0].value)
    data = {
        "operation": "get_simulation",
        "payload": payload
    }
    $.ajax(ajaxSetting('', data)).done(function(response) {
        console.log(response)
        $("#response")[0].innerHTML = JSON.stringify(response, null, 4)
    })
})

$('#add_simulation_btn').on('click', function(ev) {
    console.log(ev.target)
    payload = JSON.parse($("#add_simulation")[0].value)
    console.log(payload)
    data = {
        "operation": "add_simulation",
        "payload": JSON.parse($("#add_simulation")[0].value)
    }
    $.ajax(ajaxSetting('', data)).done(function(response) {
        console.log(response)
        $("#response")[0].innerHTML = JSON.stringify(response, null, 4)
    })
})

$('#delete_simulation_btn').on('click', function(ev) {
    console.log(ev.target)
    payload = JSON.parse($("#delete_simulation")[0].value)
    data = {
        "operation": "delete_simulation",
        "payload": payload
    }
    $.ajax(ajaxSetting('', data)).done(function(response) {
        console.log(response)
        $("#response")[0].innerHTML = JSON.stringify(response, null, 4)
    })
})


function addAlert(content, type) {
    alertID = Date.now()
    clearTimeout(timeout)

    // add an alert to #alertBox
    document.getElementById("alertBox").innerHTML += `
        <div class="alert alert-` + type + ` alert-dismissible fade show JobAdded" role="alert" id="` + alertID + `">
            <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
            ` + content + `
        </div>
    `;

    timeout = setTimeout(() => { $(`.JobAdded`).alert('close') }, 3000);
}
