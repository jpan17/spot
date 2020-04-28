var SpotFilters = {
    autoLoad: false, // Determines whether to automatically send AJAX on update of form, or only on submit

    setup: function() {
        SpotFilters.update_activities_button();
        SpotFilters.update_pet_types_button();

        if(SpotFilters.autoLoad) {
            $("input#zip_code").on("input", function(e) {
                SpotLoader.loadListings();
            })
        }

        $("#filter-form").submit(function(e) {
            e.preventDefault();
            SpotLoader.loadListings();
        })
    },

    clear_zip_code: function() {
        $('#zip_code').val('')
    },

    // Uncheck all pet_types
    clear_pet_types: function() {
        $('#pet_type_filter_button [id^="pet_type_"]:checked').prop("checked", false);
        $('#pet_type_filter_button').removeClass('has-filters');
        if(SpotFilters.autoLoad) SpotLoader.loadListings();
    },

    // Register click on pet_types_dropdown (including each of the checkboxes)
    pet_types_dropdown_click: function(event) {
        event.stopPropagation();
        SpotFilters.update_pet_types_button();
        if(SpotFilters.autoLoad) SpotLoader.loadListings();
    },

    // Add class if and only if any checked pet_types
    update_pet_types_button: function() {
        if($('#pet_type_filter_button [id^="pet_type_"]:checked').length === 0) {
            $('#pet_type_filter_button').removeClass('has-filters');
        }else {
            $('#pet_type_filter_button').addClass('has-filters');
        }
    },

    // Uncheck all activities
    clear_activities: function() {
        $('#activities_filter_button [id^="activity_"]:checked').prop("checked", false);
        $('#activities_filter_button').removeClass('has-filters');
        if(SpotFilters.autoLoad) SpotLoader.loadListings();
    },

    // Register click on activities dropdown (including each of the checkboxes)
    activities_dropdown_click: function(event) {
        event.stopPropagation();
        SpotFilters.update_activities_button();
        if(SpotFilters.autoLoad) SpotLoader.loadListings();
    },

    // Add class if and only if any checked activities
    update_activities_button: function() {
        if($('#activities_filter_button [id^="activity_"]:checked').length === 0) {
            $('#activities_filter_button').removeClass('has-filters');
        }else {
            $('#activities_filter_button').addClass('has-filters');
        }
    },

    // Clear all filters
    clear_all_filters: function() {
        SpotFilters.clear_pet_types();
        SpotFilters.clear_activities();
        SpotFilters.clear_zip_code();
    }
}

var SpotLoader = {
    request: null,

    setup: function() {
        SpotLoader.loadListings();
    },

    loadListings: function() {
        // Construct the appropriate URL
        var zipCode = encodeURI($("input#zip_code").val());
        var url = "/api/listings?";
        url += "zip_code=" + zipCode;
        $("input[id^=\"pet_type_\"]:checked").each(function() {
            url += "&" + $(this).attr("id") + "=true";
        });
        $("input[id^=\"activity_\"]:checked").each(function() {
            url += "&" + $(this).attr("id") + "=true";
        });

        if(SpotLoader.request != null) {
            SpotLoader.request.abort();
        }

        request = $.ajax({
            type: "GET",
            url: url,
            success: function(response) {
                $('#listing-table').replaceWith(response);
            }
        })
    }
};

$(document).ready(SpotFilters.setup);
$(document).ready(SpotLoader.setup);