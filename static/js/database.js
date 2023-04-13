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
    $.ajax(ajaxSetting('', data)).done(function(response) {
        console.log(response)
        if (response !== 'server is ok') {
            document.getElementById('server-check-warning').style.display = 'block'
        }
    }).catch(function(error) {
        console.log(error)
        document.getElementById('server-check-warning').style.display = 'block'
    })

    $('#create')[0].value = JSON.stringify(
        {"Item": {"id": "TestCreate1", "number": 1234}}
    , null, 4)
    $('#delete')[0].value = JSON.stringify(
        {"Key": {"id": "TestCreate1"}}
    , null, 4)
    $('#read')[0].value = JSON.stringify(
        {"Key": {"id": "TestCreate1"}}
    , null, 4)
    $('#update')[0].value = JSON.stringify(
        {"Key": {"id": "TestCreate1"}, "AttributeUpdates": {"number": {"Value": [{"test1": "val1", "key2": "val2"}]}}}
    , null, 4)
}

$('#create_btn').on('click', function(ev) {
    payload = JSON.parse($("#create")[0].value)
    data = {
        "operation": "create",
        "payload": JSON.parse($("#create")[0].value)
    }
    $.ajax(ajaxSetting('', data)).done(function(response) {
        $("#response")[0].innerHTML = JSON.stringify(response, null, 4)
    })
})

$('#delete_btn').on('click', function(ev) {
    payload = JSON.parse($("#delete")[0].value)
    data = {
        "operation": "delete",
        "payload": JSON.parse($("#delete")[0].value)
    }
    $.ajax(ajaxSetting('', data)).done(function(response) {
        $("#response")[0].innerHTML = JSON.stringify(response, null, 4)
    })
})

$('#read_btn').on('click', function(ev) {
    payload = JSON.parse($("#read")[0].value)
    data = {
        "operation": "read",
        "payload": JSON.parse($("#read")[0].value)
    }
    $.ajax(ajaxSetting('', data)).done(function(response) {
        $("#response")[0].innerHTML = JSON.stringify(response, null, 4)
    })
})

$('#update_btn').on('click', function(ev) {
    payload = JSON.parse($("#update")[0].value)
    data = {
        "operation": "update",
        "payload": JSON.parse($("#update")[0].value)
    }
    $.ajax(ajaxSetting('', data)).done(function(response) {
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
