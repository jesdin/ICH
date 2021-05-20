// Uppy Uploader Script
var uppy = null
$(document).ready(function() {
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
  .use(Uppy.Tus, { endpoint: 'https://master.tus.io/files/' })

  uppy.on('complete', (result) => {
    console.log('Upload complete! We’ve uploaded these files:', result.successful)
    files = uppy.getFiles()
    if (files['length'] > 0) {
      // Preparing ajax request
      imageURL = files[0]["tus"]["uploadUrl"]
      imageName = files[0]["name"]
      $.ajax({
        type: 'GET',
        url: '/getimage',
        data: {
          image: imageURL,
          name: imageName,
          action: 'post'
        },
        success: function (json) {
          console.log(json)
        },
        error: function (xhr, errmsg, err) {
          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
      });
    }
  })
});
