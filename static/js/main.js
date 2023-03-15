$('#single').on('click', function(ev) {
    console.log('clicked')
    const formData = new FormData(document.getElementById('single-form'));
    console.log(ev.target)
    $('#single')[0].disabled=true
    fetch('/single', {
        method: 'POST',
        body: formData
    }).then(response => response.blob())
    .then(imageBlob => {
        // Then create a local URL for that image and print it 
        const imageObjectURL = URL.createObjectURL(imageBlob);
        console.log(imageObjectURL);
        document.querySelector("#result").src = imageObjectURL;
        $('#single')[0].disabled=false
    }).catch(error => {
        $('#error')[0].innerHTML = 'Something went wrong: ' + error + '.'
        console.error('There was an error!', error);
        $('#single')[0].disabled=false
    });
})

$('#grid').on('click', function(ev) {
    console.log('clicked')
    const formData = new FormData(document.getElementById('grid-form'));
    $('#grid')[0].disabled=true
    fetch('/grid', {
        method: 'POST',
        body: formData
    }).then(response => response.blob())
    .then(imageBlob => {
        // Then create a local URL for that image and print it 
        const imageObjectURL = URL.createObjectURL(imageBlob);
        console.log(imageObjectURL);
        document.querySelector("#result").src = imageObjectURL;
        $('#grid')[0].disabled=false
    }).catch(error => {
        $('#error')[0].innerHTML = 'Something went wrong: ' + error + '.'
        console.error('There was an error!', error);
        $('#grid')[0].disabled=false
    });

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


$('#file').on('change',function(){
    //get the file name
    var fileName = $(this).val().replace('C:\\fakepath\\', " ");
    //replace the "Choose a file" label
    $(this).next('.custom-file-label').html(fileName);
})

$('#file1').on('change',function(){
    //get the file name
    var fileName = $(this).val().replace('C:\\fakepath\\', " ");
    //replace the "Choose a file" label
    $(this).next('.custom-file-label').html(fileName);
})

$('#file2').on('change',function(){
    //get the file name
    var fileName = $(this).val().replace('C:\\fakepath\\', " ");
    //replace the "Choose a file" label
    $(this).next('.custom-file-label').html(fileName);
})

$('#file3').on('change',function(){
    //get the file name
    var fileName = $(this).val().replace('C:\\fakepath\\', " ");
    //replace the "Choose a file" label
    $(this).next('.custom-file-label').html(fileName);
})

$('#file4').on('change',function(){
    //get the file name
    var fileName = $(this).val().replace('C:\\fakepath\\', " ");
    //replace the "Choose a file" label
    $(this).next('.custom-file-label').html(fileName);
})