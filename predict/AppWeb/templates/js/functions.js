

$(document).ready(function() {
  var path = "C:\\Users\\mouad\\PycharmProjects\\Dice\\models\\";
  var pyth_serv = "http://127.0.0.1:5000/"
    var array = [];
    $.getJSON('model_list.json', function (json) {
    for (var key in json) {
        if (json.hasOwnProperty(key)) {
            var item = json[key];
            array.push({
                name: item.name,
                type: item.type
            });            
        }
    }

        array.forEach((el) => {
          var o = new Option(el.name, el.name);
            $("#"+el.type+"-select").append(o)
        })

    });


    $("#linear-button").click(function() {
        var script_name = $("#linear-select").children("option:selected").val();             
            $.ajax({
               url : pyth_serv+"predict/"+script_name,
               headers: {  "Access-Control-Allow-Origin": "*",
                            "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept" },
               type : 'POST',
               success : function(response){
                  alert(response)
               },

               error : function(resultat, statut, erreur){
                 
               },

               complete : function(resultat, statut){

               }      
            });

        //Do stuff when clicked
    });
    $("#mlp-button").click(function() {
        //Do stuff when clicked
    });
    $("#convnet-button").click(function() {
        //Do stuff when clicked
    });
    $("#resnet-button").click(function()
    {
        //Do stuff when clicked
    });


    /*$("#linear-image").change(function () {
        //var reader = new FileReader();
        //reader.readAsDataURL($("#linear-image").files[0]);
        //console.log($("#linear-image").files[0]);

        bannerImage = document.getElementById('linear-image');
        imgData = getBase64Image(bannerImage);
        localStorage.setItem("imgData", imgData);


    });*/

    $('#linear-image').on('change', function() {
        readURL(this);
    });

    function storeTheImage() {
        var imgCanvas = document.getElementById('canvas-element'),
            imgContext = imgCanvas.getContext("2d");
      
        var img = document.getElementById('image-preview');
        // Make sure canvas is as big as the picture BUT make it half size to the file size is small enough
        imgCanvas.width = (img.width/4);
        imgCanvas.height = (img.height/4);

        // Draw image into canvas element
        imgContext.drawImage(img, 0, 0, (img.width/4), (img.height/4));

        // Get canvas contents as a data URL
        var imgAsDataURL = imgCanvas.toDataURL("image/png");
      
        // Save image into localStorage
        try {
            window.localStorage.setItem("imageStore", imgAsDataURL);
            $('.localstorage-output').html( window.localStorage.getItem('imageStore') );
        }
        catch (e) {
            console.log("Storage failed: " + e);
        }
    }

    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#image-preview').attr('src', e.target.result);
                storeTheImage(); 
            }
            reader.readAsDataURL(input.files[0]);
        }
    }*/


  //getHighlight();
})


function getBase64Image(img) {
    var canvas = document.createElement("canvas");
    canvas.width = img.width;
    canvas.height = img.height;

    var ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0);

    var dataURL = canvas.toDataURL("image/png");

    return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
}
