$(document).ready(setup);

function setup() {
    update_activities_button();
    update_pet_types_button();
}

function clear_zip_code() {
    $('#zip_code').val('')
}

// Uncheck all pet_types
function clear_pet_types() {
    $('#pet_type_filter_button [id^="pet_type_"]:checked').prop("checked", false);
    $('#pet_type_filter_button').removeClass('has-filters');
}

// Register click on pet_types_dropdown (including each of the checkboxes)
function pet_types_dropdown_click(event) {
    event.stopPropagation();
    update_pet_types_button();
}   

// Add class if and only if any checked pet_types
function update_pet_types_button() {
    if($('#pet_type_filter_button [id^="pet_type_"]:checked').length === 0) {
        $('#pet_type_filter_button').removeClass('has-filters');
    }else {
        $('#pet_type_filter_button').addClass('has-filters');
    }
}

// Uncheck all activities
function clear_activities() {
    $('#activities_filter_button [id^="activity_"]:checked').prop("checked", false);
    $('#activities_filter_button').removeClass('has-filters');
}

// Register click on activities dropdown (including each of the checkboxes)
function activities_dropdown_click(event) {
    event.stopPropagation();
    update_activities_button();
}

// Add class if and only if any checked activities
function update_activities_button() {
    if($('#activities_filter_button [id^="activity_"]:checked').length === 0) {
        $('#activities_filter_button').removeClass('has-filters');
    }else {
        $('#activities_filter_button').addClass('has-filters');
    }
}

// Clear all filters
function clear_all_filters() {
    clear_pet_types();
    clear_activities();
    clear_zip_code();
}