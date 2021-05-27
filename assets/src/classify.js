var uppy = null
$(document).ready(function() {
  $("#images").hide()
  $("#loading").hide()
  $("#uploaded").hide()
  $("#result-area").hide()

// Uppy Uploader Script (Initialize uppy uploader)
  uppy = Uppy.Core({
    debug: true,
    autoProceed: true,
    restrictions: {
      maxFileSize: 1000000,
      maxNumberOfFiles: 1,
      minNumberOfFiles: 1,
      allowedFileTypes: ['.dcm']
    }
  })
  .use(Uppy.Dashboard, {
    trigger: '.UppyModalOpenerBtn',
    inline: true,
    target: '#drag-drop-area',
    replaceTargetContent: true,
    showProgressDetails: true,
    height: screen.height/4,
    width: screen.width-20,
    metaFields: [
      { id: 'name', name: 'Name', placeholder: 'file name' },
      { id: 'caption', name: 'Caption', placeholder: 'describe what the image is about' }
    ],
    browserBackButtonClose: true
  })
  .use(Uppy.Tus, { endpoint: 'https://master.tus.io/files/' }) // for uploading image

  // on upload complete task
  uppy.on('complete', (result) => {
    // console.log('Upload complete! We’ve uploaded these files:', result.successful)
    
    // get uploaded files
    files = uppy.getFiles()
    if (files['length'] > 0) {
      // Preparing ajax request
      imageURL = files[0]["tus"]["uploadUrl"]
      imageName = files[0]["name"]

      // display File Uploaded successfully text and hide file uploader
      $('#message').text('File ' + imageName + ' Uploaded Successfully');
      $("#uploaded").show()
      $("#drag-drop-area").hide()
      $("#loading").show()

      // ajax request
      $.ajax({
        type: 'GET',
        url: '/getimage',
        data: {
          image: imageURL,
          name: imageName,
          action: 'post'
        },
        success: function (json) {
          $("#loading").hide()
          console.log("predictions", json["prediction"])

          // image path
          path = json["path"]
          path = "/static/" + path.slice(7,path.length)

          // display images
          $("#original").attr("src", path + '.png');
          $("#windowed").attr("src", path + '_windowed.png');
          $("#images").show()

          // get prediction and display message
          p = json["prediction"]
          p = p.replace(/\D/g,'')
          p = p.slice(0,-2)
          if(parseInt(p[0])==0) {
            $('#result').text("ICH Not Detected");
          } else {
            ICHtype = ""
            for (i=1; i<p.length; i++) {
              if(parseInt(p[i])) {
                if (i == 1) {
                  ICHtype += "Epidural "
                } else if(i == 2) {
                  ICHtype += "Intraparenchymal "
                } else if(i == 3) {
                  ICHtype += "Intraventricular "
                } else if(i == 4) {
                  ICHtype += "Subarachnoid "
                } else if(i == 5) {
                  ICHtype += "Subdural "
                }
              }
              console.log(ICHtype, p[i]);
            }
            if(ICHtype.length > 0){
              $('#result').text("ICH Detected");
              $('#result-type').text("Type: " + ICHtype);

            } else {
              $('#result').text("ICH NOT Detected");
              $('#result-type').hide();
            }
          }
    
          $("#result-area").show()
        },
        error: function (xhr, errmsg, err) {
          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
      });
    }
  })
});
