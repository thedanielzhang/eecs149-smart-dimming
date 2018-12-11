$(function() {
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
            console.log('clicked');
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
        var can_send = true;
        var debounce_timer = null;
        var slider_changed = function() {
            clearTimeout(debounce_timer);
            debounce_timer = setTimeout(function() {
                var new_dim_level = 255-slider.getValue();
                socket.send(JSON.stringify({'dim_level':new_dim_level}));
            }, 50);
            if (can_send) {
                can_send = false;
                setTimeout(function() {
                    can_send = true;
                }, 100);
                var new_dim_level = 255 - slider.getValue();
                //send it over bluetooth
                console.log(new_dim_level);
                socket.send(JSON.stringify({"dim_level":new_dim_level}));
            }
        }

        $('#light-'+light).addClass('active');

        if ($('#light-slide').length) {
            var slider = $('#light-slide').slider().on('change', slider_changed).data('slider')
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
        scheduler.config.details_on_create = true;
        var days_of_week = ["SUN", "MON", "TUES", "WED", "THURS", "FRI", "SAT"];
        scheduler.init('scheduler_here', new Date(0),"week");
        scheduler.attachEvent('onBeforeLightBox', function(id) {
            console.log('event created')
            var ev = scheduler.getEvent(id);
            ev.text = "Min: 0%\nMax: 100%";
            return true;
        });
        var upload_event = function(ev) {
            var start_day = days_of_week[ev.start_date.getDay()];
            var start_hour = ev.start_date.getHours();
            var start_min = ev.start_date.getMinutes();
            var min_regex = /Min:\s*\d+/;
            var min_matches = ev.text.match(min_regex);
            var min = 0;
            if (min_matches == undefined || min_matches.length == 0) {
                console.log("bad min format!");
            } else {
                min = parseInt(min_matches[0].substring(4));
            }

            var max_regex = /Max:\s*\d+/;
            var max_matches = ev.text.match(max_regex);
            var max = 0;
            if (max_matches == undefined || max_matches.length == 0) {
                console.log("bad min format!");
            } else {
                max = parseInt(max_matches[0].substring(4));
            }

            var end_day = days_of_week[ev.end_date.getDay()];
            var end_hour = ev.end_date.getHours()
            var end_min = ev.end_date.getMinutes()
            let new_id = light + ':' + start_day + ':' + start_hour + ':' + start_min + '-' + end_day + ':' + end_hour + ':' + end_min
            scheduler.changeEventId(ev.id, new_id);
            var start = {
                "max_setting": max,
                "min_setting": min,
                "day": start_day,
                "hour": start_hour,
                "minute": start_min,
                "schedule_id": light + ':' + start_day + ':' + start_hour + ':' + start_min + '-' + end_day + ':' + end_hour + ':' + end_min
            };

            var end = {
                "max_setting": -1,
                "min_setting": -1,
                "day": end_day,
                "hour": end_hour,
                "minute": end_min,
                "schedule_id": light + ':' + start_day + ':' + start_hour + ':' + start_min + '-' + end_day + ':' + end_hour + ':' + end_min
            }
            console.log(start);
            console.log(end);
            $.ajax({
                type: "POST",
                url: '/create/' + light + '/',
                data: [start, end],
                contentType: "application/json",
                success: function(data, textStatus, jqXHR){console.log("sent calendar")},
                dataType: "json"
            });
        }
        scheduler.attachEvent('onEventAdded', function(id, ev) {
            console.log("new event!");
            console.log(ev);
            upload_event(ev);

        });
        var delete_event = function(id) {
            console.log('deleting event');
            console.log(id)
            $.ajax({
                type: "DELETE",
                url: '/delete/' + id + '/',
                dataType: 'json',
                success: function(data, textStatus, jqXHR) { console.log("deleted a calendar")}
            });
        }
        scheduler.attachEvent('onEventChanged', function(id, ev) {
            console.log("event changed");
            console.log(ev);
            delete_event(id);
            upload_event(ev);
        });
        scheduler.attachEvent('onEventDeleted', function(id, ev) {
            console.log("event deleted");
            console.log(ev);
            delete_event(id);
        });
        $.ajax({
            type: "GET",
            url: '/schedule/' + light + '/',
            dataType: 'json',
            success: function(data, textStatus, jqXHR) {
                var events = [];
                data.forEach(function(event) {
                    event["id"] = event["schedule_id"];
                    events.push(event);
                });

                scheduler.parse(events, "json");
            }
        });
    }

});
