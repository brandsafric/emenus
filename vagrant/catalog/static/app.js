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
                var filename = document.getElementById('upload').files[0].name;
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
                            $('.upload_container').css("visibility", "hidden");

                             if ($(".upload_container").addClass('animated bounceInUp')) {
                                 $('.upload_container').removeClass('animated bounceInUp');
                             };
                            var returnedData = JSON.parse(response);

                            if ('status' in returnedData && returnedData.status == "OK") {
                                console.log('status is ok');
                                // Grab the index of the new element
                                var index = ($(".img_gallery .img_tn").length - 1);
                                var HTMLimage = '<li class="img_thumbnail" id="img_thumbnail_%data%" data-index="%data%"><img id="img_%data%" class="img_tn img_tn_ul" data-index="%data%" src="" alt="img"></li>';
                                var formattedHTML = HTMLimage.replace(/%data%/g, index);
                                // Add the image thumbnail node
                                console.log('Going to add image thumbnail node (without src)');
                                console.log('Adding: ' + formattedHTML);
                                $('.img_gallery').append(formattedHTML);
                                console.log('Setting the image to be for the last img_tn_ul element');
                                var node = $('.img_tn_ul').last();
                                var reader  = new FileReader();
                                var idx;

                                reader.onloadend = function () {
                                    node.attr("src", reader.result);
                                    console.log('Image node has been added');
                                    console.log(index);
                                    console.log(node);
                                    var parent = $(node).parent().get(0);
                                    var bro_nodes = $(parent).siblings();
                                    console.log(bro_nodes);
                                    var dataIdx;
                                    bro_nodes.each(function() {
                                        console.log('Cycling through each thumbnail node.');
                                        console.log($(this));
                                        if ($(this).hasClass('selected')) {
                                            dataIdx = $(this).attr('data-index');
                                            $(this).toggleClass('selected');
                                            console.log('thumbnail has class selected. so toggling off');
                                            console.log($(this));
                                            console.log('data-index is ' + dataIdx);
                                            console.log('storing index as idx');
                                            // Toggle icon off
                                            var idx = dataIdx;
                                            var iconNode = $('#i_delete_' + idx);
                                            console.log('Matching icon node selected previously is...');
                                            console.log(iconNode);
                                            if (iconNode.hasClass('icon_show')) {
                                                    console.log('icon has icon-show. going to toggle off');
                                                    $(iconNode).toggleClass('icon_show');
                                            }
                                        }
                                    })
                                };

                                reader.readAsDataURL(file);

                                // Set the node as selected
                                $('#img_thumbnail_' + index).toggleClass('selected');

                                // Toggle selected for other elements

                                // Add click listener
                                $('#img_thumbnail_' + index).click(function(e) {
                                    imgClick();
                                });


                                $('#i_delete_' + index).toggleClass('icon_show');

                                // Add the icon node
                                var HTMLicon = '<div class="icons_delete" id="icons_delete_%data%" data-index="%data%"><i id="i_delete_%data%" data-index="%data%" data-tn="img_thumbnail_%data%" data-parent="icons_delete_%data%" class="fa fa-times-circle i_delete icon_show" aria-hidden="true"></i></div>'
                                var formattedIcon = HTMLicon.replace(/%data%/g, index);
                                console.log(formattedIcon);
                                $('.image_container').append(formattedIcon);

                                // Add click listener
                                $('#i_delete_' + index).click(function(e) {
                                   iconClick();
                                });

                                // Finally, check to see if we are at the max 5 images
                                countImages();
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
                    iconClick();
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
                        // es[3].value = '';
                        $('#upload').val("");
                    } catch(err) {
                        console.log('Error with clearing upload. ' + err);
                    }
                }
                else {
                    console.log('Going to run checkforduplicate.');
                    // Set the upload_container to visible.
                    // $(".no_upload").css("margin-top", "0");
                    if (checkDuplicate(f.name)) {
                        console.log('Diplicate file found.');
                        $('#upload').val("");
                        alert("File is already uploaded!");
                    } else {
                        console.log('No filename duplicates found.');
                        $(".upload_container").css("visibility", "visible");
                        $(".upload_container").addClass('animated bounceInUp');
                    }

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

            var checkDuplicate = function(filename) {
                var imageNode = $(".img_tn");
                console.log('Looking for a match of ' + filename);

                imageNode.each(function() {
                    var imgSrc = $(this).attr('src');
                    console.log('imgSrc is ' + imgSrc);
                    if (imgSrc.includes(filename)) {
                        console.log('Duplicate image found!');
                        return true;
                    }
                });
                console.log('returning false');

                return false;

            }

            var countImages = function() {
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
            }

            if (($("#editRestForm").length) || ($("#newRestForm").length)) {
                console.log('this is the edit/new restaurant');
                var el = $('#target').attr('data-index');
                $( "ul.img_gallery li.img_thumbnail:eq("+ el + ")" ).toggleClass( "selected" );

            }

            countImages();

            var iconClick = function() {
                console.log('delete click');

                //Grab the data-parent attribute which stores the ID of the parent
                var iconID = '#' + ($(event.target).attr("data-parent"));
                // Grab the index of the imagge
                var imgIndex = ($(event.target).attr("data-index"));
                // Grab the data-tn attribute which stores the ID of the img_thumbnail
                var imgID = '#' + ($(event.target).attr("data-tn"));
                // Grab the node objects
                var imgNode = $(imgID);
                var iNode = $(iconID);

                console.log(iNode);
                console.log(imgNode);
                // console.log(imgIndex);




                var data = {"image_index":imgIndex};
                console.log('Sending delete for index ' + imgIndex.toString());

                $.ajax({
                    url: '/deleteImage',
                    contentType: 'application/json',
                    data: JSON.stringify(data),
                    dataType : 'json',
                    type: 'POST',
                    success: function(response) {
                        console.log(response);
                        console.log("Success. Going to remove images from DOM.");
                        // Remove the image from the page
                        $(iNode).remove();
                        $(imgNode).remove();
                        // $(iNode).css('display', 'none');
                        // $(imgNode).css('display', 'none');
                        console.log('Images can be added');
                        $(".file_container").css("visibility", "visible");
                        $(".no_upload").css("visibility", "hidden");
                    },
                    error: function(error) {
                        console.log(error);
                        console.log("Error. Cannot Remove image from DOM.");
                    }
                });
            };

            var imgClick = function() {
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
                    console.log('Clicked image..');
                    console.log('parent is...');
                    console.log($(event.target).parent());
                    if ($(event.target).parent().hasClass('selected')) {
                        // do nothing
                        console.log('parent has class selected. Doing nothing.');
                    } else {
                        console.log('parent does not have class selected.');
                        console.log('going to toggle parent class of selected');
                        $(event.target).parent().toggleClass('selected');
                        var targetID = $(event.target).attr('data-index');
                        var el = $('#i_delete_' + targetID);
                        console.log('targetID is ' + targetID);
                        console.log('element is: ');
                        console.log(el);
                        if (!el.hasClass('i_delete')) {
                            console.log('element  does not have i_delete class');
                            var index = ($(".image_container .icons_delete").length - 1);
                            console.log(index);
                            console.log('#i_delete_' + index.toString());
                            el = $('#i_delete_' + index);
                            console.log('the last indexed icons_delete is');
                            console.log(el);
                            if (el.hasClass('icon_show')) {
                                el.toggleClass('icon_show');
                            }
                        } else {
                            console.log('Has class i_delete. going to toggle off');
                                console.log(el);
                            el.toggleClass('icon_show');
                        }
                        var iParent = el.parent().get(0);
                        console.log(iParent);
                        $(iParent).toggleClass('icon_show');
                        // el.toggleClass('icon_show')
                        var img_nodes = $(iParent).siblings();

                        img_nodes.each(function(index) {
                            // console.log($(this));

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
