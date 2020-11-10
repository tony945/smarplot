setInterval(renew_data, 5000);

function renew_data() {
  $.ajax({
    url: '/realtime_data_refresh/',
    type : "GET",
    dataType: "json",
    success: function(data){
        $("#soil").html(`${data.soil}%`);
        $("#temp").html(`${data.temp}&#176 C`);
        $("#light").html(`${data.light}lm`);
    },
  });  
}

