var RegisterFormValidator = {
    setup: function() {
        $("#login-form").submit(function(e) {
            var errorMsg = RegisterFormValidator.validateForm();
            if(errorMsg.length > 0) {
                $("#validate_error").text(errorMsg);
                e.preventDefault();
            }
        });
    },

    validateForm: function() {
        var fullName = $("#full_name").val();
        var email = $("#email").val();
        var phoneNum = $("#phone_number").val();
        var isOwnerChecked = $("#is_owner").prop("checked");
        var isSitterChecked = $("#is_sitter").prop("checked");
        var password = $("#password").val();
        var confirmPassword = $("#confirm_password").val();
        var errorMsg = "";

        if(fullName.length === 0 || fullName.length > 64) {
            errorMsg = "Name must be between 1 and 64 characters long.";
        }else if(!RegisterFormValidator.isValidEmail(email)) {
            errorMsg = "Email must be of the form something@example.com";
        }else if(!RegisterFormValidator.isValidPhoneNumber(phoneNum)) {
            errorMsg = "Phone number must be of the form XXX-XXX-XXXX and X's must consist only of numbers";
        }else if(!isOwnerChecked && !isSitterChecked) {
            errorMsg = "Owner type must be selected";
        }else if(password != confirmPassword) {
            errorMsg = "Passwords must match";
        }
        
        return errorMsg;
    },

    isValidEmail: function(email) {
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    },

    isValidPhoneNumber: function(phone_num) {
        if(!phone_num.match(/^[0-9]{3}(-[0-9]{3})(-[0-9]{4})?$/))
            return false;
        return true;
    }
}

$(document).ready(RegisterFormValidator.setup);