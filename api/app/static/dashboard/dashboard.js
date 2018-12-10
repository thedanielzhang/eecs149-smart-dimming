$(function() {
    //we will probably actually use django templating for this
    let searchParams = new URLSearchParams(window.location.search);
    if (searchParams.has('mac')) {
        let mac = searchParams.get('mac');
        $('#mac-'+mac).addClass('active');
        let name_socket = new WebSocket('ws://' + window.location.host + '/lights/config/');
        name_socket.onopen = function(event) {
            console.log("connected!");
        };
        name_socket.onmessage = function(event) {
            console.log('message!');
            let event_data = JSON.parse(event.data);
            if ('name_set' in event_data && event_data['name_set']) {
                let light = ('id' in event_data ? event_data['id'] : 0)
                window.location.assign("?id="+light)
            }
        };
        $('#lightNameSubmit').click(function() {
            $(this).button('loading')
            let name = $('#lightNameInput').val();
            name_socket.send(JSON.stringify({'name':name,'mac':mac}));
        });
        $('#lightNameFlash').click(function() {
            var turn_on = false;
            if ($(this).html() == "Flash On") {
                turn_on = true;
                $(this).html('Flash Off');
            } else {
                turn_on = false;
                $(this).html('Flash On');
            }
            name_socket.send(JSON.stringify({'mac':mac,'flash':turn_on}));
        });
    } else {
        let light = searchParams.has('light') ? searchParams.get('light') : 0;
        let socket = new WebSocket('ws://' + window.location.host + '/lights/' + light + '/');
        socket.onopen = function(event) {
            console.log("connected!");
        };
        socket.onmessage = function(event) {
            console.log("received " + event.data);
         }
        //let light_url = '/lights/' + light + '/';
        var slider_changed = function() {
            var new_dim_level = 255 - slider.getValue();
            //send it over bluetooth
            console.log(new_dim_level);
            socket.send(JSON.stringify({"dim_level":new_dim_level}));
        }
        $('#light-'+light).addClass('active');
        if ($('#light-slide').length) {
            var slider = $('#light-slide').slider().on('slide', slider_changed).data('slider')
        }
        $('input#ambient-tracking-check').change(function() {
            let light_tracking_enabled = ($('input#ambient-tracking-check').is(':checked'));
             socket.send(JSON.stringify({"light_tracking":light_tracking_enabled}));
        });

        $('input#motion-tracking-check').change(function() {
            let motion_tracking_enabled = ($('input#motion-tracking-check').is(':checked'));
            socket.send(JSON.stringify({"motion_tracking": motion_tracking_enabled}));
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
    }

});
