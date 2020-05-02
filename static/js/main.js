var Spot = {
    allowedExtensions: ['jpg', 'jpeg', 'png'],

    setup: function() {
        // Implement custom file inputs to display uploaded file
        $('.file-input input[type=file]').change(function() {
            let f = $(this).prop('files')[0];
            let file = f.name;
            let fileParts = file.split('.');
            let extension = fileParts[fileParts.length - 1].toLowerCase();
            
            let correctFileFormat = true;
            
            if(!Spot.allowedExtensions.includes(extension)) {
                correctFileFormat = false;
                file = 'Invalid extension: ' + extension;
            } else if (f.size > 5242880) {
                correctFileFormat = false;
                file = 'Max File Size: 5MB';
            } else if(file.length > 20) {
                file = file.substring(0, 17) + '...';
            }
            $(this).siblings('.file-name').text(file);

            if (correctFileFormat) {
                Spot.getSignedRequest(f);
            }

        })
    },

    redirect: function(url) {
        window.location.href = url;
    },

    getSignedRequest: function(file){
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/sign_s3?file_name="+file.name+"&file_type="+file.type);
        xhr.onreadystatechange = function(){
          if(xhr.readyState === 4){
            if(xhr.status === 200){
              var response = JSON.parse(xhr.responseText);
              Spot.uploadFile(file, response.data, response.url);
            }
            else{
              alert("Could not get signed URL.");
            }
          }
        };
        xhr.send();
    },

    uploadFile: function(file, s3Data, url){
        var xhr = new XMLHttpRequest();
        xhr.open("POST", s3Data.url);
      
        var postData = new FormData();
        for (key in s3Data.fields){
          postData.append(key, s3Data.fields[key]);
        }
        postData.append('file', file);
      
        xhr.onreadystatechange = function() {
          if (xhr.readyState === 4){
            if (xhr.status === 200 || xhr.status === 204){
              document.getElementById("pet_image_url").value = url;
            } else{
              alert("Could not upload file.");
            }
         }
        };
        xhr.send(postData);
      }

}

$(document).ready(Spot.setup);