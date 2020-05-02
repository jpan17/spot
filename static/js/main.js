var Spot = {
    allowedExtensions: ['jpg', 'jpeg', 'png'],

    setup: function() {
        // Implement custom file inputs to display uploaded file
        $('.file-input input[type=file]').change(function() {
            let f = $(this).prop('files')[0];
            let file = f.name;
            let fileParts = file.split('.');
            let extension = fileParts[fileParts.length - 1].toLowerCase();
            if(!Spot.allowedExtensions.includes(extension)) {
                file = 'Invalid extension: ' + extension;
            } else if (f.size > 5242880) {
                file = 'Max File Size: 5MB';
            } else if(file.length > 20) {
                file = file.substring(0, 17) + '...';
            }
            $(this).siblings('.file-name').text(file);

        })
    },

    redirect: function(url) {
        window.location.href = url;
    }
}

$(document).ready(Spot.setup);