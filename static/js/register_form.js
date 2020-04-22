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

    /* TODO: CHECK THAT START DATETIME IS BEFORE END DATETIME! */
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
            errorMsg = "Phone number must be of the form XXX-XXX-XXXX or XXXXXXXXXX";
        }
        
        return errorMsg;
    },

    isValidEmail: function(str) {
        return true;
    },

    isValidPhoneNumber: function(str) {
        return true;
    }
}

$(document).ready(RegisterFormValidator.setup);