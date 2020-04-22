var LoginFormValidator = {
    setup: function() {
        $("#login-form").submit(function(e) {
            var errorMsg = LoginFormValidator.validateForm();
            if(errorMsg.length > 0) {
                $("#validate_error").text(errorMsg);
                e.preventDefault();
            }
        });
    },

    validateForm: function() {
        var email = $("#email").val();
        var password = $("#password").val();
        var errorMsg = "";

        if(!LoginFormValidator.isValidEmail(email)) {
            errorMsg = "Email must be valid (e.g. something@example.com).";
        }else if(password.length === 0) {
            errorMsg = "Please input a password";
        }
        
        return errorMsg;
    },

    isValidEmail: function(email) {
        let re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if(email.match(re))
            return true;
        return false;
    }
}

$(document).ready(LoginFormValidator.setup);