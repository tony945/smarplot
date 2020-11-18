// 導覽列

$(function(){$("#realtime_panel").addClass("active");});



// 刷新即時資料
$(renew_data());
setInterval(renew_data, 5000);

function renew_data() {
    $.ajax({
        url: '/realtime_data_refresh/',
        type : "GET",
        dataType: "json",
        success: function(data){
            $("#soil").html(`${data.soil}%`);
            $("#temp").html(`${data.temp}&#176 C`);
            $("#light").html(`${data.light}lux`);
        },
    });  
}
// 澆花按鈕

$('#toggle_event_editing button').click(function () {
    if ($(this).hasClass('locked_active') || $(this).hasClass('unlocked_inactive')) {
        /* code to do when unlocking */
        $('#switch_status').html('開始澆花.');
    }
    else {
        /* code to do when locking */
        $('#switch_status').html('手動澆花關閉.');
    }

  /* reverse locking status 
     eq(0): for button whose index is 0
     eq(1): for button whose index is 1
   */
  $('#toggle_event_editing button').eq(0).toggleClass('locked_inactive locked_active btn-default btn-info');
  $('#toggle_event_editing button').eq(1).toggleClass('unlocked_inactive unlocked_active btn-info btn-default');
});

