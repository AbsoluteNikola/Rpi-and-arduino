console.log('load main.js');

window.temperatureChart = new function buildTemperature() {
    var ctx = document.getElementById('temperatureChart');
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                    label: "№1",
                    data: [],
                    borderColor: 'rgb(0, 105, 217)',
                    fill: false
                },
                {
                    label: "№2",
                    data: [],
                    borderColor: 'rgb(255, 169, 0)',
                    fill: false
                }
            ]
        },
        options: {
            title: {
                display: true,
                text: 'Температура'
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
    console.log('temperatureChart was built');
    return chart;
}

window.humidityChart = new function buildHumidity() {
    var ctx = document.getElementById('humidityChart');
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: "",
                data: [],
                borderColor: 'rgb(0, 105, 217)',
                backgroundColor: 'rgba(0, 105, 217, 0.2)'
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Влажность'
            }
        }
    });
    console.log('humidityChart was built');
    return chart;
}


window.CO2Chart = new function buildCO2() {
    var ctx = document.getElementById('CO2Chart');
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: "",
                data: [],
                borderColor: 'rgb(0, 105, 217)',
                backgroundColor: 'rgba(0, 105, 217, 0.2)'
            }]
        },
        options: {
            title: {
                display: true,
                text: 'CO2'
            }
        }
    });
    console.log('CO2Chart was built');
    return chart;
}

window.pressureChart = new function buildPressure() {
    var ctx = document.getElementById('pressureChart');
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: "№1",
                data: [],
                borderColor: 'rgb(0, 105, 217)',
                backgroundColor: 'rgba(0, 105, 217, 0.2)'
            },
            {
            	label: "№2",
                data: [],
                borderColor: 'rgb(255, 169, 0)',
                fill: false
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Давление'
            },
            scales: {
                yAxes: [{
                    ticks: {
                        min: 900
                    }
                }]
            }
        }
    });
    console.log('pressureChart was built')
    return chart;
}


function addData(data) {
    $("#pressure1Val").text(`${data.pressure[0]}`);
    $("#pressure2Val").text(`${data.pressure[1]}`);
    $("#temperature1Val").text(`${data.temperature[0]}`);
    $("#temperature2Val").text(`${data.temperature[1]}`);
    $("#humidityVal").text(`${data.humidity}`);
    $("#CO2Val").text(`${data.CO2}`);
    $("#voltageSystem").text(`${data.voltageSystem}`);
    $("#voltageHeater").text(`${data.voltageHeater}`);
    $("#gyroX").text(`${data.gyro.x}`);
    $("#gyroY").text(`${data.gyro.y}`);
    $("#acmtrZ").text(`${data.gyro.z}`);
    $("#acmtrX").text(`${data.gyro.x}`);
    $("#acmtrY").text(`${data.gyro.y}`);
    $("#acmtrZ").text(`${data.gyro.z}`);

    if (window.alertFire && data.fire == true && fire_el.getAttribute('active') == 'false') {
        window.alertFire = false;
        alert('ПОЖАР!');
    }
    for (var sensor in data) {
        if (sensor == 'fire' || sensor == 'voltageSystem' || sensor == 'voltageHeater' || sensor == 'gyro')
            continue;
        var chart = window[sensor + 'Chart'];

        if (!(data[sensor] instanceof Array))
            data[sensor] = [data[sensor]];
        var d = new Date();

        chart.data.labels.push(`${d.getMinutes()}:${d.getSeconds()}`);

        //delete first point if size > 60
        if (chart.data.labels.length > 60) {
            chart.data.labels.shift();
            for (var i = 0; i < chart.data.datasets.length; i++) {
                chart.data.datasets[i].data.shift();
            }
        }
        // add new points
        for (var i = 0; i < data[sensor].length; i++) {
            if (data[sensor][i] === -1.0 && chart.data.datasets[i].label !== 'Error') {
                chart.data.datasets[i].oldLabel = chart.data.datasets[i].label;
                chart.data.datasets[i].oldColor = chart.data.datasets[i].borderColor;
                console.log(chart.data.datasets[i].oldLabel, chart.data.datasets[i].oldColor);
                //chart.data.datasets[i].oldBackgroundColor = chart.data.datasets[i].backgroundColor; 
                chart.data.datasets[i].borderColor = 'rgb(255, 0, 0)';
                //chart.data.datasets[i].backgroundColor = 'rgba(255, 0, 0, 1)'
                chart.data.datasets[i].label = 'Error';
                continue;
            } else if (chart.data.datasets[i].label ==='Error' && data[sensor][i] !== -1.0) {
                chart.data.datasets[i].label = chart.data.datasets[i].oldLabel;
                chart.data.datasets[i].borderColor = chart.data.datasets[i].oldColor;
            } else if (chart.data.datasets[i].label === 'Error' && data[sensor][i] === -1.0) {
                continue;
            }
            chart.data.datasets[i].data[chart.data.labels.length - 1] = data[sensor][i];
        }
        chart.update();

    }
}

function getInfo() {
    $.ajax({
            url: 'getInfo'
        })
        .done(addData)
}

function getAudioList() {
    $.get('/getAudioList')
        .done(
            function (data){
                $('#audioSelect').html("")
                $.each(data, function(value, key) {
                    console.log(value, key);
                    $('#audioSelect').append($('<option>', {value: key, text:key}));
                });
            }
        );
}

function getFilesList() {
    $.get('/getFilesList')
        .done(
            function (data){
                $('#filesSelect').html("")
                $.each(data, function(value, key) {
                    console.log(value, key);
                    $('#filesSelect').append($('<option>', {value: key, text:key}));
                })
                setDownloadFileLink();
            }
        );
}

function setDownloadFileLink() {
    var file = $('#filesSelect option:selected').text();
    var link = "";
    if(file.endsWith('.db')) {
        link = `/getDB/${file}`;
    } else {
        link = `/getFile/${file}`;
    }
    console.log(`change link ${link}`);
    $('#downloadFile').attr("href", link);
}

function setAudioLink() {
    var audio = $('#audioSelect option:selected').text();
    player = document.getElementById("player");
    player.src = `/getAudio/${audio}`;
}

function checkLogin() {
    console.log({ password: $('#password')[0].value });
    $.post({
        url: 'checkLogin',
        data: { password: $('#password')[0].value },
    }).done(function () {
        alert('password is ok')
    })
}

function startDevice(device) {
    console.log(`${device}`);
    $.post({
        url: '/startDevice',
        data: { sensor: device },
        success: function(result) {
            if (result == 'Error')
                return;
            d = document.getElementById(device);
            d.checked = result;
            console.log(`${device}:${d.checked}`);
        }
    })
}

audio = {
    context: new AudioContext(),
}
alertFire = true;

function startRecord() {
    navigator.mediaDevices.getUserMedia({ audio: true, video: false })
        .then(function(stream) {
            $('#recordButton').removeClass('btn-primary').addClass('btn-danger');
            $('#recordButton').text("стоп")
            $('#recordButton').attr("onclick", "stopRecord()");
            audio.curStream = stream;
            audio.input = audio.context.createMediaStreamSource(stream);
            audio.recorder = new Recorder(audio.input);
            audio.recorder.record();
            console.log('start recording');
        });
    setTimeout(stopRecord, 100000);
}


function stopRecord() {
    if (!audio.recorder.recording)
        return;
    audio.recorder.stop();
    audio.curStream.getAudioTracks()[0].stop();
    audio.recorder.exportWAV(function(blob) {
        audio.file = blob;
        document.getElementById("player").src = URL.createObjectURL(blob);
        console.log('stop recording')
        $('#recordButton').removeClass('btn-danger').addClass('btn-primary');
        $('#recordButton').text("запись")
        $('#recordButton').attr("onclick", "startRecord()");
        $('#sendButton').removeClass('btn-danger').addClass('btn-primary');
    });
}

function sendRecord() {
    form = new FormData();
    form.append('audio', audio.file);
    $.post({
            url: '/putAudio',
            data: form,
            cache: false,
            processData: false,
            contentType: false
        }).done(function() {
            console.log("send successfully");
            $('#sendButton').removeClass('btn-danger').addClass('btn-primary');
        })
        .fail(function() {
            $('#sendButton').removeClass('btn-primary').addClass('btn-danger');
        });
}

function sendFile() {
    form = new FormData();
    form.append('file', audio.file);
    form.append('')
    $.post({
            url: '/putAudio',
            data: form,
            cache: false,
            processData: false,
            contentType: false
        }).done(function() {
            console.log("send successfully");
            $('#sendButton').removeClass('btn-danger').addClass('btn-primary');
        })
        .fail(function() {
            $('#sendButton').removeClass('btn-primary').addClass('btn-danger');
        });
}

function loadImg() {
	var name = "/state.jpg?" + String(Math.random());
    $("#cameraLoader")
    	.attr('src', name)
        .attr('onload', function() {
        	$("#camera").attr('src', name);
        });
}

// timer = setInterval(
//     function() {
//         getInfo();
//         loadImg();
//     }, 1000);

fireTimer = setInterval(
    function() {
        window.alertFire = true;
    }, 5000);