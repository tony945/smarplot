




$(function () {
    
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $('#btnPassword').click(
        function () {
            oldPassword = $("#oldPassword")
            newPassword = $("#newPassword")
            confirmPassword = $("#confirmPassword")

            $.ajax({
                url: 'password/',
                type: "POST",
                data: JSON.stringify({
                                     "oldPassword": oldPassword,
                                     "newPassword": newPassword,
                                     "confirmPassword": confirmPassword, 
                                     }),
                contentType: "application/json; charset=utf-8",                     
                dataType: "json",
            });
        }
    );

    $('#btnEmail').on('click',
        function () {
            email = $("#newEmail").value

            $.ajax({
                url: 'email/',
                type: "POST",
                headers:{
                        "X-CSRFToken": csrftoken
                },
                data: JSON.stringify({
                                     "email": email,
                                     }),
                contentType: "application/json; charset=utf-8",  
                dataType: "json",
            });
        }
    );

    $('#btnPlantname').click(
        function () {
            plantname = $("#newPlantname")

            $.ajax({
                url: 'plantname/',
                type: "POST",
                data: JSON.stringify({
                                     "plantname": plantname,
                                     }),
                contentType: "application/json; charset=utf-8",  
            });
        }
    );

    $('#btnPlantReset').click(
        function () {

            $.ajax({
                url: 'reset/',
                type: "POST",
            });
        }
    );
})