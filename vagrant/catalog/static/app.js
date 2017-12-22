$(function () {
        var bindEvents = function() {
            $("#appetizer-section").click(function () {
                $("#appetizer-row").slideToggle();
                if ($("#appetizer-toggle").hasClass("fa-chevron-up")) {
                    $("#appetizer-toggle").toggleClass("fa-chevron-up");
                    $("#appetizer-toggle").toggleClass("fa-chevron-down");
                } else {
                    $("#appetizer-toggle").toggleClass("fa-chevron-down");
                    $("#appetizer-toggle").toggleClass("fa-chevron-up");
                }
            });
            $("#entree-section").click(function () {
                $("#entree-row").slideToggle();
                if ($("#entree-toggle").hasClass("fa-chevron-up")) {
                    $("#entree-toggle").toggleClass("fa-chevron-up");
                    $("#entree-toggle").toggleClass("fa-chevron-down");
                } else {
                    $("#entree-toggle").toggleClass("fa-chevron-down");
                    $("#entree-toggle").toggleClass("fa-chevron-up");
                }
            });
            $("#dessert-section").click(function () {
                $("#dessert-row").slideToggle();
                if ($("#dessert-toggle").hasClass("fa-chevron-up")) {
                    $("#dessert-toggle").toggleClass("fa-chevron-up");
                    $("#dessert-toggle").toggleClass("fa-chevron-down");
                } else {
                    $("#dessert-toggle").toggleClass("fa-chevron-down");
                    $("#dessert-toggle").toggleClass("fa-chevron-up");
                }
            });
            $("#beverage-section").click(function () {
                $("#beverage-row").slideToggle();
                if ($("#beverage-toggle").hasClass("fa-chevron-up")) {
                    $("#beverage-toggle").toggleClass("fa-chevron-up");
                    $("#beverage-toggle").toggleClass("fa-chevron-down");
                } else {
                    $("#beverage-toggle").toggleClass("fa-chevron-down");
                    $("#beverage-toggle").toggleClass("fa-chevron-up");
                }
            });
            $("#icon-sort").click(function () {
                sortListDir();
            });


        };

        var bindForms = function() {

            $(".img_thumbnail").click(function (e) {
                // User clicks the thumbnail frame
                if ($(event.target).hasClass('img_thumbnail')) {
                    if ($(event.target).hasClass('selected')) {
                        // do nothing
                    } else {
                            $(event.target).toggleClass('selected');
                            // Check if the no_upload is showing
                            // if($(".no_upload").css('display') == 'block') {
                                // Slice the id string
                                var id = "i_delete_" + $(event.target).find('.img_tn').attr('id').slice(-1);
                                $('#' + id).toggleClass('icon_show');
                                var i_parent = $('#' + id).parent().get(0);
                                var img_nodes = $(i_parent).siblings();
                                img_nodes.each(function() {
                                    if ($(this).children().hasClass('icon_show')) {
                                        $(this).children().toggleClass('icon_show');
                                    }
                                })
                            // }
                            $(event.target).siblings(".selected").toggleClass("selected");
                            $('#target').children().val('');
                    }

                }
                // User clicks the image
                else {
                    if ($(event.target).parent().hasClass('selected')) {
                        // do nothing
                    } else {
                        $(event.target).parent().toggleClass('selected');
                        // if($(".no_upload").css('display') == 'block') {
                           // Slice the id string
                            var targetID = event.target.id.slice(-1);
                           var iName = "i_delete_" + targetID;
                           var el = $('#' + iName);
                           el.toggleClass('icon_show');
                            var iParent = el.parent().get(0);
                            var img_nodes = $(iParent).siblings();
                            img_nodes.each(function(index) {
                                if ($(this).children().hasClass('icon_show')) {
                                    $(this).children().toggleClass('icon_show');
                                }
                            })
                       // }
                        $(event.target).parent().siblings(".selected").toggleClass("selected");
                        var path = $(event.target).eq(0).attr('data-imgpath');
                        $('#target').val(path);
                        }
                }
            });


            $(".i_delete").click(function (e) {
                if ($(e.target).hasClass('icon_show')) {
                    console.log('delete click');

                    //Grab the data-parent attribute which stores the ID of the parent
                    var iconID = '#' + ($(this).attr("data-parent"));
                    // Grab the index of the imagge
                    var imgIndex = ($(this).attr("data-index"));
                    // Grab the data-tn attribute which stores the ID of the img_thumbnail
                    var imgID = '#' + ($(this).attr("data-tn"));
                    // Grab the node objects
                    var imgNode = $(imgID);
                    var iNode = $(iconID);

                    console.log(iNode);
                    console.log(imgNode);
                    console.log(imgIndex);

                    // var icon = $(event.target).parent().get(0);
                    // console.log(icon);
                    $(iNode).css('display', 'none');
                    $(imgNode).css('display', 'none');
                     console.log('Images can now be added');
                    $(".file_container").css("visibility", "visible");
                    $(".no_upload").css("visibility", "hidden");

                    var data = {"image_index":imgIndex};

                    $.ajax({
                        url: '/deleteImage',
                        contentType: 'application/json',
                        data: JSON.stringify(data),
                        dataType : 'json',
                        type: 'POST',
                        success: function(response) {
                            console.log(response);
                            // Remove the image from the page

                        },
                        error: function(error) {
                            console.log(error);
                        }
                    });
                }

            });

            $(".btn-set").on("click", function() {
                console.log('Image has been set.');
                // Change the image on the form circle to be the selected image.

            });

            $("#upload").change(function(e){
                console.log('File has changed.');
                console.log(e.target.value);
                console.log((e.target.value).slice(12));
                var f=this.files[0];
                var sizeInMb = f.size/1024;
                var sizeLimit= 1024*1; // if you want 1 MB
                console.log(sizeInMb);
                if (sizeInMb > sizeLimit) {
                    alert('Sorry the file exceeds the maximum size of 1 MB!');
                    // reset the input (code for all browser)
                    var es = document.forms[0].elements;
                    try {
                        es[3].value = '';
                    } catch(err) {
                        console.log('Error with clearing upload. ' + err);
                    }
                }
                else {
                    // Continue on...
                    // $(".upload_container").css("display", "block");
                    $(".no_upload").css("margin-top", "0");
                    $(".upload_container").css("visibility", "visible");
                    $(".upload_container").addClass('animated bounceInUp');

                }
                 });


            var imageItems = [];
            var imageNode = $(".img_tn");

            imageNode.each(function(index) {
                var src = $(this).attr('src');
                var imgPath = $(this).attr('data-imgpath');
                var usrPath = $(this).attr('data-usrpath');
                var filename = $(this).attr('data-filename');

                var userDir = src.replace(imgPath, '');

                console.log( index + ' : ' + src);
                console.log( index + ' : ' + imgPath);
                console.log( index + ' : ' + userDir);
                console.log( index + ' : ' + usrPath);
                console.log( index + ' : ' + filename);



            });



            if (($("#editRestForm").length) || ($("#newRestForm").length)) {
                console.log('this is the edit/new restaurant');
                var el = $('#target').attr('data-index');
                $( "ul.img_gallery li.img_thumbnail:eq("+ el + ")" ).toggleClass( "selected" );

            }

            //Check for image thumbnails on the image_gallery.
            if ($(".img_thumbnail").length) {
                console.log($(".img_thumbnail").length);
                var image_count = $(".img_thumbnail").length;


                if (image_count >= 5) {
                    console.log('No more images permitted until you delete one.');
                    // $(".btn-file").css("display", "none");
                    $(".no_upload").css("visibility", "visible");
                    $(".file_container").css('visibility', 'hidden');
                    $(".no_upload").css("margin-top", "-50px");
                }
            }


        };

        bindEvents();
        // Check to see if this is the newRestForm or editForm.
        if (($("#editRestForm").length) || ($("#newRestForm").length)) {
            // If ao, bind form events.
            bindForms();
        }




});
