var ListingFormValidator = {
    setup: function() {
        $("#listing_form").submit(function(e) {
            var errorMsg = ListingFormValidator.validateForm();
            if(errorMsg.length > 0) {
                $("#validate_error").text(errorMsg);
                e.preventDefault();
            }else {
                if(!$('input#address_input').hasClass('ready-to-submit')) {
                    $("#validate_error").text('Please input a valid address.');
                    e.preventDefault();
                }
            }
        });
    },

    /* TODO: CHECK THAT START DATETIME IS BEFORE END DATETIME! */
    validateForm: function() {
        var petName = $("#pet_name").val();
        var startDate = $("#start_date").val();
        var startTime = $("#start_time").val();
        var endDate = $("#end_date").val();
        var endTime = $("#end_time").val();
        var hasPetType = $("input[name='pet_type']:checked").length > 0;
        var hasActivity = $("input[type='checkbox']:checked").length > 0;
        var extraInfo = $("#extra_info").val();
        var errorMsg = "";

        if(petName.length === 0 || petName.length > 64) {
            errorMsg = "Pet name must be between 1 and 64 characters long."
        }else if(!ListingFormValidator.isValidDate(startDate)) {
            errorMsg = "Start Date must be of the format MM/DD/YYYY with valid month, date, and 4-digit year."
        }else if(!ListingFormValidator.isValidTime(startTime)) {
            errorMsg = "Start Time must be of the format HH:MM with HH from 0-23 and MM from 0-59."
        }else if(!ListingFormValidator.isValidDate(endDate)) {
            errorMsg = "End Date must be of the format MM/DD/YYYY with valid month, date, and 4-digit year (2000 - 3000)."
        }else if(!ListingFormValidator.isValidTime(endTime)) {
            errorMsg = "End Time must be of the format HH:MM with HH from 0-23 and MM from 0-59."
        }else if(ListingFormValidator.datetimePrecedesErrorStr(startDate, startTime, endDate, endTime).length > 0) {
            errorMsg = "Start Date/Time must be before End Date/Time (" + ListingFormValidator.datetimePrecedesErrorStr(startDate, startTime, endDate, endTime) + ")."
        }else if(!hasPetType) {
            errorMsg = "Please select a pet type."
        }else if(!hasActivity) {
            errorMsg = "Please select at least one activity."
        }else if(extraInfo.length > 1000) {
            errorMsg = "Description is " + extraInfo.length + " characters long (max: 1000)."
        }
        
        return errorMsg;
    },

    // Checks if HH:MM or H:MM and hours are between 0-23 and minutes are between 0-59
    isValidTime: function(str) {
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
    },

    // Checks for MM/DD/YYYY with 1 or 2 digits each for MM, DD, 4 digits for YYYY,
    // and checks that month, day, and year are in valid ranges
    isValidDate: function(str) {
        if(!str.match(/^[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{4}$/))
            return false;
        var parts = str.split("/");
        var m = parseInt(parts[0])
        var d = parseInt(parts[1])
        var y = parseInt(parts[2])

        if(m < 1 || m > 12) 
            return false;
        if(d < 1 || d > ListingFormValidator.daysInMonth(m - 1, y))
            return false;
        if(y < 2000 || y > 3000)
            return false;

        return true;
    },

    // Number of days in month m in year y, where m is zero indexed
    daysInMonth: function(m, y) {
        switch (m) {
            case 1 :
                return (y % 4 == 0 && y % 100) || y % 400 == 0 ? 29 : 28;
            case 8 : case 3 : case 5 : case 10 :
                return 30;
            default :
                return 31;
        }
    },

    // Checks whether the combination of startDate and startTime comes before endDate and endTime
    // Format for dates is MM/DD/YYYY and times are HH:MM
    // Returns empty string if valid, returns applicable message otherwise
    datetimePrecedesErrorStr: function(startDate, startTime, endDate, endTime) {
        var startDateVals = startDate.split("/");
        var startTimeVals = startTime.split(":");
        var endDateVals = endDate.split("/");
        var endTimeVals = endTime.split(":");

        var month1 = parseInt(startDateVals[0]);
        var day1 = parseInt(startDateVals[1]);
        var year1 = parseInt(startDateVals[2]);
        var hour1 = parseInt(startTimeVals[0]);
        var minute1 = parseInt(startTimeVals[1]);
        var month2 = parseInt(endDateVals[0]);
        var day2 = parseInt(endDateVals[1]);
        var year2 = parseInt(endDateVals[2]);
        var hour2 = parseInt(endTimeVals[0]);
        var minute2 = parseInt(endTimeVals[1]);

        if(year1 > year2) return "Start year is after End year";
        if(year2 > year1) return "";
        if(month1 > month2) return "Start month is after End month";
        if(month2 > month1) return "";
        if(day1 > day2) return "Start day is after End day";
        if(day2 > day1) return "";
        if(hour1 > hour2) return "Start hour is after End hour";
        if(hour2 > hour1) return "";
        if(minute1 >= minute2) return "Start time equals End time";
        return "";
    }
}

var SpotAlgolia = {
    autocomplete: null,
    acElement: null,
    acSelector: '#address_input',

    setup: function() {
        SpotAlgolia.acElement = document.querySelector(SpotAlgolia.acSelector);
        SpotAlgolia.autocomplete = places({
            appId: 'plO1SV8YCUC3',
            apiKey: '168cb9867faff5823a430526b0c935df',
            container: SpotAlgolia.acElement,
            useDeviceLocation: true
        });

        // Clear anything that isn't suggested and add ready-to-submit class when a suggestion is chosen
        SpotAlgolia.autocomplete.on('change', function(e) {
            $(SpotAlgolia.acSelector).removeClass("not-validated");
            $(SpotAlgolia.acSelector).addClass("ready-to-submit");
            $("input#zip_code").val(e.suggestion.postcode);
            $("input#lat").val(e.suggestion.latlng.lat);
            $("input#lng").val(e.suggestion.latlng.lng);
            $("input#address_id").val(e.suggestion.hit.objectID);
        });

        $(SpotAlgolia.acElement).on('input', function(e) {
            $(SpotAlgolia.acSelector).addClass("not-validated");
            $(SpotAlgolia.acSelector).removeClass("ready-to-submit");
        })
        $(SpotAlgolia.acElement).change(function(e) {
            if($(this).hasClass("not-validated")) {
                SpotAlgolia.autocomplete.setVal("");
                $(SpotAlgolia.acSelector).removeClass("ready-to-submit");
            }
        });
    }
}

$(document).ready(ListingFormValidator.setup);
$(document).ready(SpotAlgolia.setup);