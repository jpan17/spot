var SpotFilters = {
    setup: function() {
        SpotFilters.update_activities_button();
        SpotFilters.update_pet_types_button();
    },

    clear_zip_code: function() {
        $('#zip_code').val('')
    },

    // Uncheck all pet_types
    clear_pet_types: function() {
        $('#pet_type_filter_button [id^="pet_type_"]:checked').prop("checked", false);
        $('#pet_type_filter_button').removeClass('has-filters');
    },

    // Register click on pet_types_dropdown (including each of the checkboxes)
    pet_types_dropdown_click: function(event) {
        event.stopPropagation();
        SpotFilters.update_pet_types_button();
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
    },

    // Register click on activities dropdown (including each of the checkboxes)
    activities_dropdown_click: function(event) {
        event.stopPropagation();
        SpotFilters.update_activities_button();
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

$(document).ready(SpotFilters.setup);