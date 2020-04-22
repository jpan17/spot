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

        if(!LoginFormValidator.isValidEmail(email)) {
            errorMsg = "Email must be of the form something@example.com";
        }else if(password.length==0) {
            errorMsg = "User must input password";
        }
        
        return errorMsg;
    },

    isValidEmail: function(email) {
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    },
}

$(document).ready(LoginFormValidator.setup);