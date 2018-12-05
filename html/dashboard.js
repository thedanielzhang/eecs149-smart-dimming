var slider_changed = function() {
    var new_dim_level = 255 - slider.getValue();
    //send it over bluetooth
    console.log(new_dim_level);
}

var slider = $('#light-slide').slider().on('slide', slider_changed).data('slider');

$('input#ambient-tracking-check').change(function() {
    if ($('input#ambient-tracking-check').is(':checked')) {
        console.log('ambient light checked');
    } else {
        console.log('ambient light unchecked');
    }
});

$('input#motion-tracking-check').change(function() {
    if ($('input#motion-tracking-check').is(':checked')) {
        console.log('motion tracking checked');
    } else {
        console.log('motion tracking unchecked');
    }
});



$(function() {
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


    //we will probably actually use django templating for this
    let searchParams = new URLSearchParams(window.location.search);
    let light = searchParams.has('light') ? searchParams.get('light') : 0;

    $('#light-'+light).addClass('active');
});
