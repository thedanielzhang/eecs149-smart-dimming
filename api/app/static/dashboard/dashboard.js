$(function() {
    //we will probably actually use django templating for this
    let searchParams = new URLSearchParams(window.location.search);
    let light = searchParams.has('light') ? searchParams.get('light') : 0;
    let light_url = '/lights/' + light + '/';
    /*
    var socket = new WebSocket("ws://www.example.com/socketserver");

    socket.onopen = function(event) {
        console.log("socket connected!");
    }
    */

    var slider_changed = function() {
        var new_dim_level = 255 - slider.getValue();
        //send it over bluetooth
        console.log(new_dim_level);
        //socket.send(JSON.stringify({"dim_level":new_dim_level}));
        $.ajax({
            url: light_url,
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify({"lightSetting": new_dim_level})
        });
    }

    var slider = $('#light-slide').slider().on('slide', slider_changed).data('slider')

    $.get(light_url, function(info) {
        //console.log(data)
        //let info = JSON.parse(data);
        if ("lightSetting" in info) {
            let new_level = 255 - (info["lightSetting"][0] & 0xFF);
            slider.setValue(new_level, false, false);
        }
        if ("light_tracking_enabled" in info && info["light_tracking_enabled"]) {
            //check the box
        }
        if ("motion_tracking_enabled" in info && info["motion_tracking_enabled"]) {
            //check the box
        }
    });

    //slider.on('slide', slider_changed);

    $('input#ambient-tracking-check').change(function() {
        let light_tracking_enabled = ($('input#ambient-tracking-check').is(':checked'));
        $.ajax({
            url: light_url,
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify({"light_tracking_enabled": light_tracking_enabled})
        });
    });

    $('input#motion-tracking-check').change(function() {
        let motion_tracking_enabled = ($('input#motion-tracking-check').is(':checked'));
        $.ajax({
            url: light_url,
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify({"light_tracking_enabled": light_tracking_enabled})
        });
    });

    scheduler.config.day_date = "%l";
    scheduler.init('scheduler_here', new Date(0),"week");
    scheduler.attachEvent('onEventAdded', function(id, ev) {
        console.log("new event!");
        console.log(ev);
    });
    scheduler.attachEvent('onEventChanged', function(id, ev) {
        console.log("event changed");
        console.log(ev);
    });
    scheduler.attachEvent('onEventDeleted', function(id, ev) {
        console.log("event deleted");
        console.log(ev);
    });

    let events = [
        {id:1, text:"Min: 20%\nMax: 80%", start_date:"12/29/1969 14:00",end_date:"12/29/1969 17:00"},
        {id:2, text:"Min: 0%\nMax: 20%", start_date:"12/29/1969 22:00",end_date:"12/30/1969 06:00"},
        {id:3, text:"Min: 20%\nMax: 80%", start_date:"01/01/1970 14:00",end_date:"01/01/1970 17:00"},
    ]/*{{ events|safe }}*/;
    scheduler.parse(events, "json");

    $('#light-'+light).addClass('active');
});
