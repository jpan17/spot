var RegisterFormValidator = {
    setup: function() {
        $("#register-form").submit(function(e) {
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
        }else if(email.length > 128) {
            errorMsg = "Email must be less than 128 characters long.";
        }else if(!RegisterFormValidator.isValidEmail(email)) {
            errorMsg = "Email must be valid (e.g. something@example.com).";
        }else if(!RegisterFormValidator.isValidPhoneNumber(phoneNum)) {
            errorMsg = "Phone number must be of the form ###-###-#### or ##########.";
        }else if(!isOwnerChecked && !isSitterChecked) {
            errorMsg = "Please select a user type (owner or sitter).";
        }else if(password.length <= 7) {
            errorMsg = "Password must be at least 8 characters long."
        }else if(!password.match(/[a-z]/) || !password.match(/[A-Z]/) || !password.match(/[0-9]/)){
            errorMsg = "Password must contain a lowercase and uppercase letter, and a number."
        }else if(password != confirmPassword) {
            errorMsg = "Passwords must match.";
        }
        
        return errorMsg;
    },

    isValidEmail: function(email) {
        let re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if(email.match(re))
            return true;
        return false;
    },

    isValidPhoneNumber: function(phone_num) {
        if(!phone_num.match(/^[0-9]{10}$/))
            if(!phone_num.match(/^[0-9]{3}-[0-9]{3}-[0-9]{4}$/))
                return false;
        return true;
    }
}

$(document).ready(RegisterFormValidator.setup);