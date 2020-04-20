function clear_pet_types(...pet_types) {
    for(var i = 0; i < pet_types.length; i++) {
        $('#pet_type_' + pet_types[i]).prop("checked", false);
    }
    $('#pet_type_filter_button').removeClass('has-filters');
}

function pet_types_dropdown_click(event, ...pet_types) {
    event.stopPropagation();
    // Are any of the pet_types checked?
    var anyChecked = false;
    for(var i = 0; i < pet_types.length; i++) {
        if($('#pet_type_' + pet_types[i]).prop("checked")) {
            anyChecked = true;
            break;
        }
    }
    // Change the display of the filter as appropriate
    if(anyChecked) {
        $('#pet_type_filter_button').addClass('has-filters');
    }else {
        $('#pet_type_filter_button').removeClass('has-filters');
    }
}

function clear_activities(...activities) {
    for(var i = 0; i < activities.length; i++) {
        $('#activity_' + activities[i]).prop("checked", false);
    }
    $('#activities_filter_button').removeClass('has-filters');
}

function activities_dropdown_click(event, ...activities) {
    event.stopPropagation();
    // Are any of the activities checked?
    var anyChecked = false;
    for(var i = 0; i < activities.length; i++) {
        if($('#activity_' + activities[i]).prop("checked")) {
            anyChecked = true;
            break;
        }
    }
    // Change the display of the filter as appropriate
    if(anyChecked) {
        $('#activities_filter_button').addClass('has-filters');
    }else {
        $('#activities_filter_button').removeClass('has-filters');
    }
}