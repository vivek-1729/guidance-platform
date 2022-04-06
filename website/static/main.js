//JS script for the login/signup modal
$(document).ready(function(){
    const path = window.location.pathname;
    const url = window.location.hostname + path;
    const user_id = JSON.parse(document.getElementById('user_id').textContent);
    if(user_id == null) {
        if(path.includes("signup")) {
        $('#signupModal').modal('show');
        }
        else {
            $("#loginModal").modal('show');
        }
    }
    $('#signupFromLogin').click(function() {
        $('#loginModal').modal('hide');
        location.href += "signup"
    })
});

