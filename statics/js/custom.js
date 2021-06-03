// Submit Form Change Address User
// this is the id of the form

$("#form-user-address").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = '/customer/change_address/'

    $.ajax({
           type: "POST",
           url: url,
           data: form.serialize(), // serializes the form's elements.
           success: function(data)
           {
                showToastr(data);

           },
            error: function (data) {
                showToastr(data);
            },
         });


});

    // Cap nhat avatar
// $("#form-user-avatar").submit(function(e) {
//         e.preventDefault(); // avoid to execute the actual submit of the form.
//         var formData = new FormData($('#form-user-avatar')[0]);
//         formData.append('user_avatar', $('input[type=file]')[0].files[0]);
//         formData.append('x', $('input[type=hidden]')[0].val());
//         formData.append('y', $('input[type=hidden]')[0].val());
//         formData.append('width', $('input[type=hidden]')[0].val());
//         formData.append('height', $('input[type=hidden]')[0].val());
//         var url = '/customer/change_avatar/'
//
//         $.ajax({
//                type: "POST",
//                url: url,
//                data: formData,
//                 contentType: false,
//                 processData: false,
//                success: function(data)
//                {
//                     window.location.reload(true);
//
//                },
//                 error: function (data) {
//                     showToastr(data);
//                 },
//          })
//     });


$("#form-user-info").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = '/customer/change_info/'

    $.ajax({
           type: "POST",
           url: url,
           data: form.serialize(), // serializes the form's elements.
           success: function(data)
           {
               showToastr(data);
           },
            error: function (data) {
                showToastr(data);
            },
         });


});



// Add the following code if you want the name of the file appear on select
$(".custom-file-input").on("change", function() {
  var fileName = $(this).val().split("\\").pop();
  $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});


// -------------TOAST-----------------
function showToastr(data) {
    var i = -1,
        toastCount = 0,
        $toastlast,
        getMessage = function () {
            var msgs = ['Hello, some notification sample goes here',
                '<div><input class="form-control input-small" value="textbox"/>&nbsp;<a href="http://themeforest.net/item/metronic-responsive-admin-dashboard-template/4021469?ref=keenthemes" target="_blank">Check this out</a></div><div><button type="button" id="okBtn" class="btn blue">Close me</button><button type="button" id="surpriseBtn" class="btn default" style="margin: 0 8px 0 8px">Surprise me</button></div>',
                'Did you like this one ? :)',
                'Totally Awesome!!!',
                'Yeah, this is the Metronic!',
                'Explore the power of App. Purchase it now!'
            ];
            i++;
            if (i === msgs.length) {
                i = 0;
            }

            return msgs[i];
        };

    var shortCutFunction = data.tag;
    var msg = data.data;
    var title = data.title || '';

    var toastIndex = toastCount++;

    toastr.options = {
        closeButton: "checked",
        positionClass: 'toast-top-right',
        onclick: null,
        showDuration: 1000,
        hideDuration:1000,
        timeOut : 2000,
        extendedTimeOut : 1000
    };

    toastr.options.showEasing = "swing";
    toastr.options.hideEasing = "linear";
    toastr.options.showMethod = "fadeIn";
    toastr.options.hideMethod = "fadeOut";


    if (!msg) {
        msg = getMessage();
    }
    var $toast = toastr[shortCutFunction](msg, title); // Wire up an event handler to a button in the toast, if it exists

}
// -------------ENDTOAST-----------------

//--------CROP AVATAR---------
      /* SCRIPT TO OPEN THE MODAL WITH THE PREVIEW */
      $("#user_avatar").change(function () {
        if (this.files && this.files[0]) {
          var reader = new FileReader();
          reader.onload = function (e) {
            $("#image").attr("src", e.target.result);
            $("#modalCrop").modal("show");
          }
          reader.readAsDataURL(this.files[0]);
        }
      });

      /* SCRIPTS TO HANDLE THE CROPPER BOX */
      var $image = $("#image");
      var cropBoxData;
      var canvasData;
      $("#modalCrop").on("shown.bs.modal", function () {
        $image.cropper({
          viewMode: 1,
          aspectRatio: 1/1,
          minCropBoxWidth: 720,
          minCropBoxHeight: 720,
            cropBoxResizable: false,
          ready: function () {
            $image.cropper("setCanvasData", canvasData);
            $image.cropper("setCropBoxData", cropBoxData);
          }
        });
      }).on("hidden.bs.modal", function () {
        cropBoxData = $image.cropper("getCropBoxData");
        canvasData = $image.cropper("getCanvasData");
        $image.cropper("destroy");
      });

      $(".js-zoom-in").click(function () {
        $image.cropper("zoom", 0.1);
      });

      $(".js-zoom-out").click(function () {
        $image.cropper("zoom", -0.1);
      });

      /* SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER */
      $(".js-crop-and-upload").click(function () {
        var cropData = $image.cropper("getData");
        $("#id_x").val(cropData["x"]);
        $("#id_y").val(cropData["y"]);
        $("#id_height").val(cropData["height"]);
        $("#id_width").val(cropData["width"]);
        $("#form-user-avatar").submit();
        });


//--------END CROP AVATAR---------
$('.ui.dropdown')
  .dropdown()
;

//Show model add social
$("#btn_customer_social_add_social").click(function (){
    $('.ui.modal').modal('show')
})

// gán placeholder để người dùng biết cần nhập gì
$("#input_customer_social_social_id").change(function (e){
    var id = parseInt($(this).val())
    // Place holder
    switch (id) {
        case 1: //FB
            $("#input_customer_social_social_url").attr("placeholder", "Nhập liên kết Facebook (https://www.facebook.com/....)")
            $("#input_customer_social_social_url").attr('type','url');
            $("#input_customer_social_social_url").attr('maxlength','255');
            e.preventDefault();
            break
        case 2: //Zalo
            $("#input_customer_social_social_url").attr('placeholder',"Nhập số điện thoại Zalo");
            $("#input_customer_social_social_url").attr('type','text');
            $("#input_customer_social_social_url").attr('maxlength','10');
             e.preventDefault();
            break
        case 3: //TIKTOK
            $("#input_customer_social_social_url").attr("placeholder", "Nhập liên kết TikTok (https://www.tiktok.com/....)")
            $("#input_customer_social_social_url").attr('type','url');
            $("#input_customer_social_social_url").attr('maxlength','255');
            e.preventDefault();
            break
        case 4: //MOMO
            $("#input_customer_social_social_url").attr("placeholder", "Nhập số điện thoại MoMo")
            $("#input_customer_social_social_url").attr('type','text');
            $("#input_customer_social_social_url").attr('maxlength','9999999999');
            e.preventDefault();
            break
        case 5: //INSTAGRAM
            $("#input_customer_social_social_url").attr("placeholder", "Nhập tên người dùng Instagram (_trilong_)")
            $("#input_customer_social_social_url").attr('type','url');
            $("#input_customer_social_social_url").attr('maxlength','255');
            e.preventDefault();
            break
        case 7: //EMAIL
            $("#input_customer_social_social_url").attr("placeholder", "Nhập Email (xxx@gmail.com)")
            $("#input_customer_social_social_url").attr('type','url');
            $("#input_customer_social_social_url").attr('maxlength','255');
            e.preventDefault();
            break
        case 8: //TWITTER
            $("#input_customer_social_social_url").attr("placeholder", "Nhập liên kết Twitter (https://twitter.com/....)")
            $("#input_customer_social_social_url").attr('type','url');
            $("#input_customer_social_social_url").attr('maxlength','255');
            e.preventDefault();
            break
        case 10: //TELEGRAM
            $("#input_customer_social_social_url").attr("placeholder", "Nhập số điện thoại Telegram")
            $("#input_customer_social_social_url").attr('type','text');
            $("#input_customer_social_social_url").attr('maxlength','10');
            e.preventDefault();
            break
        case 12: //BLOGER
            $("#input_customer_social_social_url").attr("placeholder", "Nhập liên kết Blogspot (https://xxx.blogspot.com/....)")
            $("#input_customer_social_social_url").attr('type','url');
            $("#input_customer_social_social_url").attr('maxlength','255');
            e.preventDefault();
            break
        case 13: //LINKEDIN
            $("#input_customer_social_social_url").attr("placeholder", "Nhập liên kết LinkedIn (https://www.linkedin.com/in/....)")
            $("#input_customer_social_social_url").attr('type','url');
            $("#input_customer_social_social_url").attr('maxlength','255');
            e.preventDefault();
            break
    }
});

// submit form them social
$("#form_customer_social_add_social").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = '/customer/add_social/'

    $.ajax({
           type: "POST",
           url: url,
           data: form.serialize(), // serializes the form's elements.
           success: function(data)
           {
                showToastr(data);
                if (data.tag == "success"){
                    window.location.reload(true)
                }


           },
            error: function (data) {
                showToastr(data);
            },
         });


});

// submit form change url social

$('.btn-customer-social-change').click(function (e) {
    var id = $(this).data('id')
    e.preventDefault();

    var form = $('form#form-customer-social-'+id).serialize();
    console.log(form)
    var url = '/customer/change_social/'
    $.ajax({
        url: url,
        type: "POST",
        data: form ,
        success: function(data) {
           showToastr(data)
        },
        error:function (data){
            showToastr(data)
        }
    });
})

