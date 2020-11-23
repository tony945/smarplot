$(function () {
    
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    $('#btnPassword').on('click',
        function (e) {
            e.preventDefault();
            $.ajax({
                url: 'password/',
                type: "POST",
                headers:{
                    "X-CSRFToken": csrftoken
                },
                data: $('#passwordForm').serialize(),
                dataType: "json",
                success: function(data) {
                    if (data==0) {
                        window.alert("Password changed");
                        window.location.href = "/user_panel/";    
                    }
                    else if (data==1)
                        $("#passwordModal .alert").css("visibility","visible").html('<em>Password incorrect!!</em>');
                    else
                    $("#passwordModal .alert").css("visibility","visible").html('<em>New password does not match!!</em>');
                },
                error: function() {
                    window.alert("Something went wrong");
                }
            });
        }
    );

    $('#btnEmail').on('click',
        function (e) {
            e.preventDefault();
            $.ajax({
                url: 'email/',
                type: "POST",
                headers:{
                        "X-CSRFToken": csrftoken
                },
                data: $('#emailForm').serialize(),
                success: function(data) {
                    if (data==1) {
                        window.alert("Email changed");
                        window.location.href = "/user_panel/";    
                    }
                    else
                        $("#emailModal .alert").css("visibility","visible").html('<em>Email already exist</em>')
                },
                error: function() {
                    window.alert("Something went wrong");
                }
            });
        }
    );

    $('#btnPlantname').on('click',
        function (e) {
            e.preventDefault();
            $("#plantnameModal").modal('hide');
            $.ajax({
                url: 'plantname/',
                type: "POST",
                headers:{
                    "X-CSRFToken": csrftoken
                },
                data: $('#plantnameForm').serialize(),
                success: function() {              
                    window.alert("Plant name changed");
                    window.location.href = "/user_panel/";
                },
                error: function() {
                    window.alert("Something went wrong");
                }
            });
        }
    );

    $('#btnPlantReset').click(
        function (e) {
            e.preventDefault();
            $.ajax({
                url: 'reset/',
                type: "POST",
                headers:{
                    "X-CSRFToken": csrftoken
                },
                success: function() {              
                    window.location.href = "/register_plant/";
                },
                error: function() {
                    window.alert("Something went wrong");
                }
            });
        }
    );
})