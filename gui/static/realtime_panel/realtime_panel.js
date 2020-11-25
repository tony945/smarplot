// 導覽列

$(function () { $("#realtime_panel").addClass("active"); });



// 刷新即時資料
$(renew_data());
setInterval(renew_data, 5000);

function renew_data() {
    $.ajax({
        url: '/realtime_data_refresh/',
        type: "GET",
        dataType: "json",
        success: function (data) {
            $("#soil").html(`${data.soil}%`);
            $("#temp").html(`${data.temp}&#176 C`);
            $("#light").html(`${data.light}lux`);
            $("#air").html(`${data.air}%`);
        },
    });
}



// 自動澆花按鈕
$(function () {
    $('#toggle_event_editing1 button').click(function () {
        if ($(this).hasClass('locked_active') || $(this).hasClass('unlocked_inactive')) {
            /* code to do when unlocking */
            status = 1
        }
        else {
            /* code to do when locking */
            status = 0
        }

        let csrftoken = $("[name=csrfmiddlewaretoken]").val();

        $.ajax({
            url: '/realtime_panel/autowater/',
            type: "POST",
            headers: {
                "X-CSRFToken": csrftoken
            },
            data: { "status": status },
            dataType: "json",

        });
        /* reverse locking status 
           eq(0): for button whose index is 0
           eq(1): for button whose index is 1
         */
        $('#toggle_event_editing1 button').eq(0).toggleClass('locked_inactive locked_active btn-default btn-info');
        $('#toggle_event_editing1 button').eq(1).toggleClass('unlocked_inactive unlocked_active btn-info btn-default');
    });
})


// 光源按鈕
$(function () {
    $('#toggle_event_editing2 button').click(function () {
        if ($(this).hasClass('locked_active') || $(this).hasClass('unlocked_inactive')) {
            /* code to do when unlocking */
            status = 1
        }
        else {
            /* code to do when locking */
            status = 0
        }

        let csrftoken = $("[name=csrfmiddlewaretoken]").val();

        $.ajax({
            url: '/realtime_panel/light/',
            type: "POST",
            headers: {
                "X-CSRFToken": csrftoken
            },
            data: { "status": status },
            dataType: "json",

        });

        /* reverse locking status 
           eq(0): for button whose index is 0
           eq(1): for button whose index is 1
         */
        $('#toggle_event_editing2 button').eq(0).toggleClass('locked_inactive locked_active btn-default btn-info');
        $('#toggle_event_editing2 button').eq(1).toggleClass('unlocked_inactive unlocked_active btn-info btn-default');
    });
})

// 手動澆花按鈕
$(function () {
    $('#toggle_event_editing3 button').click(function () {
        if ($(this).hasClass('locked_active') || $(this).hasClass('unlocked_inactive')) {
            /* code to do when unlocking */
            $('#switch_status').html('開始澆花.');
            status = 1
        }
        else {
            /* code to do when locking */
            $('#switch_status').html('手動澆花關閉.');
            status = 0
        }

        let csrftoken = $("[name=csrfmiddlewaretoken]").val();

        $.ajax({
            url: '/realtime_panel/manualwater/',
            type: "POST",
            headers: {
                "X-CSRFToken": csrftoken
            },
            data: { "status": status },
            dataType: "json",

        });

        /* reverse locking status 
           eq(0): for button whose index is 0
           eq(1): for button whose index is 1
         */
        $('#toggle_event_editing3 button').eq(0).toggleClass('locked_inactive locked_active btn-default btn-info');
        $('#toggle_event_editing3 button').eq(1).toggleClass('unlocked_inactive unlocked_active btn-info btn-default');
    });
})


