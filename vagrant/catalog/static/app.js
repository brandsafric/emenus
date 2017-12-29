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
                imgClick();
            });

            // Upload image file
            $(".btn-file").click(function (e) {
                var file = document.getElementById('upload').files[0]; //Files[0] = 1st file
                var filename = document.getElementById('upload').files[0].name; //Should be 'picture.jpg'
                console.log('image');
                var formData = new FormData();
                formData.append('image', file, filename);

                $.ajax({
                        url: '/uploadImage',
                        data: formData,
                        processData: false,
                        contentType: false,
                        type: 'POST',
                        success: function(response) {
                            // console.log(response);
                            // Reset the upload divs
                            $('#upload').val("");
                            // $(".no_upload").css("margin-top", "0");
                            $(".upload_container").css("visibility", "hidden");
                            var returnedData = JSON.parse(response);

                            if ('status' in returnedData && returnedData.status == "OK") {
                                console.log('status is ok');
                                // Grab the index of the new element
                                var index = ($(".img_gallery .img_tn").length);
                                var HTMLimage = '<li class="img_thumbnail" id="img_thumbnail_%data%"><img id="img_thumbnail%data%" class="img_tn img_tn_ul" src="" alt="img"></li>';
                                var formattedHTML = HTMLimage.replace('%data%', index).replace('%data%', index);
                                // Add the image thumbnail node
                                $('.img_gallery').append(formattedHTML);
                                var node = $('.img_tn_ul');
                                var reader  = new FileReader();

                                reader.onloadend = function () {
                                    node.attr("src", reader.result);
                                    console.log('Image node has been added');
                                };

                                reader.readAsDataURL(file);

                                // Set the node as selected
                                $('#img_thubnail_' + index).toggleClass('selected');

                                // Add click listener
                                $('#img_thubnail_' + index).click(function(e) {
                                    imgClick();
                                });
                                $('#i_delete_' + index).toggleClass('icon_show');

                                // Add the icon node
                                var HTMLicon = '<div class="icons_delete" id="icons_delete_%data%"><i id="i_delete_%data%" data-index="%data%" data-tn="img_thumbnail_%data%" data-parent="icons_delete_%data%" class="fa fa-times-circle i_delete icon_show" aria-hidden="true"></i></div>'
                                var formattedIcon = HTMLicon.replace('%data%', index).replace('%data%', index).replace('%data%', index).replace('%data%', index).replace('%data%', index).replace('%data%', index);
                                console.log(formattedIcon);
                                $('.image_container').append(formattedIcon);
                            }
                        },
                        error: function(error) {
                            console.log(error);
                        }
                    });
            });

            // Delete image file
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

                    $(iNode).css('display', 'none');
                    $(imgNode).css('display', 'none');
                     console.log('Images can be added');
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

            // Upload file change
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
                    // Set the upload_container to visible.
                    // $(".no_upload").css("margin-top", "0");
                    $(".upload_container").css("visibility", "visible");
                    $(".upload_container").addClass('animated bounceInUp');

                }
                 });

            var imageItems = [];
            var imageNode = $(".img_tn");
            var selected = $('#target').val();
            console.log(selected);

            imageNode.each(function(index) {
                var parent = $(this).parent().get(0);
                $(this).parent().parent().attr('id');
                var src = $(this).attr('src');
                var imgPath = $(this).attr('data-imgpath');

                console.log( index + ' : ' + src);
                console.log( index + ' : ' + imgPath);

                if (imgPath == selected && ($("#editRestForm").length)) {
                    console.log('match');
                    console.log('edit restaurant form')
                    console.log(imgPath);
                    console.log(parent);
                    $(parent).toggleClass('selected');
                    // console.log(parent.attr('id'));
                    // var parent = self.parent().get(0);
                    // parent.toggleClass('selected');
                }


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

            var imgClick = function() {
                console.log('image has been clicked');
                // User clicks the thumbnail frame
                if ($(event.target).hasClass('img_thumbnail')) {
                    console.log('Clicked img_thumbnail.');
                    if ($(event.target).hasClass('selected')) {
                        console.log('It has class selected. Doing nothing.');
                        // do nothing
                    } else {
                            $(event.target).toggleClass('selected');
                            console.log('It does not have class selected.');
                            // Check if the no_upload is showing
                            // if($(".no_upload").css('display') == 'block') {
                                // Slice the id string
                            var targetID= $(event.target).attr('data-index');
                            var el = $('#i_delete_' + targetID);
                            if (!el.hasClass('i_delete')) {
                                console.log('there is no element');
                                var index = ($(".image_container .icons_delete").length);
                                console.log(index);
                                el = $('#i_delete_' + index);
                                console.log('further item down is');
                                console.log(el);
                                if (el.hasClass('icon_show')) {
                                  el.toggleClass('icon_show');
                                }
                                else {
                                    el.toggleClass('icon_show');
                                }

                            } else {
                            el.toggleClass('icon_show');
                        }
                    var i_parent = el.parent().get(0);
                    var img_nodes = $(i_parent).siblings();

                    img_nodes.each(function() {
                        if ($(this).children().hasClass('icon_show')) {
                            $(this).children().toggleClass('icon_show');
                        }
                    });

                    $(event.target).siblings(".selected").toggleClass("selected");
                    $('#target').children().val('');

                    }
                }
                // User clicks the image. Happens most of the time
                else {
                    console.log('Clicked img.');
                    if ($(event.target).parent().hasClass('selected')) {
                        // do nothing
                        console.log('parent has class selected. Doing nothing.');
                    } else {
                        console.log('parent does  not have class selected.');
                        $(event.target).parent().toggleClass('selected');
                        var targetID = $(event.target).attr('data-index');
                        var el = $('#i_delete_' + targetID);
                        console.log(el);
                        if (!el.hasClass('i_delete')) {
                            console.log('there is no element');
                            var index = ($(".image_container .icons_delete").length);
                            console.log(index);
                            el = $('#i_delete_' + index);
                            console.log('further item down is');
                            console.log(el);

                            if (el.hasClass('icon_show')) {
                              el.toggleClass('icon_show');
                            }
                        } else {
                            el.toggleClass('icon_show');
                        }
                        var iParent = el.parent().get(0);
                        console.log(iParent);
                        var img_nodes = $(iParent).siblings();

                        img_nodes.each(function(index) {
                            console.log($(this));

                            if ($(this).children().hasClass('icon_show')) {
                                $(this).children().toggleClass('icon_show');
                                }
                        })

                        $(event.target).parent().siblings(".selected").toggleClass("selected");
                        var path = $(event.target).eq(0).attr('data-imgpath');
                        $('#target').val(path);
                        }
                }

            };
        };

        bindEvents();
        // Check to see if this is the newRestForm or editForm.
        if (($("#editRestForm").length) || ($("#newRestForm").length)) {
            // If ao, bind form events.
            bindForms();
        }




});
