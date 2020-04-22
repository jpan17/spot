var Spot = {
    setup: function() {
        // Implement custom file inputs to display uploaded file
        $('.file-input input[type=file]').change(function() {
            var file = $(this).prop('files')[0].name;
            if(file.length > 20) file = file.substring(0, 17) + '...';
            $(this).siblings('.file-name').text(file);
        })
    },

    redirect: function(url) {
        window.location.href = url;
    }
}

$(document).ready(Spot.setup);