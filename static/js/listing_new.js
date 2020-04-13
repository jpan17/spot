window.onload = function() {
    this.setup();
};

function setup() {
    $("#listing_form").submit(function(e) {
        var errorMsg = validateForm();
        if(errorMsg.length > 0) {
            $("#validate_error").text(errorMsg);
            e.preventDefault();
        }
    });
}

/* TODO: CHECK THAT START DATETIME IS BEFORE END DATETIME! */
function validateForm() {
    var petName = $("#pet_name").val();
    var startDate = $("#start_date").val();
    var startTime = $("#start_time").val();
    var endDate = $("#end_date").val();
    var endTime = $("#end_time").val();
    var hasPetType = $("input[name='pet_type']:checked").length > 0;
    var hasActivity = $("input[type='checkbox']:checked").length > 0;
    var zipCode = $("#zip_code").val();
    var errorMsg = "";

    if(petName.length == 0 || petName.length > 64) {
        errorMsg = "Pet name must be between 1 and 64 characters long."
    }else if(!isValidDate(startDate)) {
        errorMsg = "Start Date must be of the format MM/DD/YYYY with valid month, date, and 4-digit year."
    }else if(!isValidTime(startTime)) {
        errorMsg = "Start Time must be of the format HH:MM with HH from 0-23 and MM from 0-59."
    }else if(!isValidDate(endDate)) {
        errorMsg = "End Date must be of the format MM/DD/YYYY with valid month, date, and 4-digit year."
    }else if(!isValidTime(endTime)) {
        errorMsg = "End Time must be of the format HH:MM with HH from 0-23 and MM from 0-59."
    }else if(!hasPetType) {
        errorMsg = "Please select a pet type."
    }else if(!hasActivity) {
        errorMsg = "Please select at least one activity."
    }else if(!isValidZipCode(zipCode)) {
        errorMsg = "Please enter a valid zip code (either ##### or #####-####)."
    }

    return errorMsg;
}

// Checks if a string is of the format ##### or #####-#### (valid zip code)
function isValidZipCode(str) {
    if(!str.match(/^[0-9]{5}(-[0-9]{4})?$/))
        return false;
    return true;
}

// Checks if HH:MM or H:MM and hours are between 0-23 and minutes are between 0-59
function isValidTime(str) {
    if(!str.match(/^[0-9]{1,2}:[0-9]{2}$/))
        return false;
    var parts = str.split(":");
    var h = parseInt(parts[0]);
    var m = parseInt(parts[1]);

    if(h > 23)
        return false;
    if(m > 59)
        return false;
    return true;
}

// Checks for MM/DD/YYYY with 1 or 2 digits each for MM, DD, 4 digits for YYYY,
// and checks that month, day, and year are in valid ranges
function isValidDate(str) {
    if(!str.match(/^[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{4}$/))
        return false;
    var parts = str.split("/");
    var m = parseInt(parts[0])
    var d = parseInt(parts[1])
    var y = parseInt(parts[2])

    if(m < 1 || m > 12) 
        return false;
    if(d < 1 || d > daysInMonth(m - 1, y))
        return false;
    if(y < 2020 || y > 3000)
        return false;

    return true;
}

// Number of days in month m in year y, where m is zero indexed
function daysInMonth(m, y) {
    switch (m) {
        case 1 :
            return (y % 4 == 0 && y % 100) || y % 400 == 0 ? 29 : 28;
        case 8 : case 3 : case 5 : case 10 :
            return 30;
        default :
            return 31;
    }
}