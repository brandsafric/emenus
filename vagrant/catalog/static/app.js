$(function () {
    var bindEvents = function () {
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

    var bindFormEvents = function () {

        var imageNode = $(".img_tn");

        var current;
        var imagesArr = [];
        var imgDefault = $('#img_tn_1').attr('src');


        // Grab the filenames and push to array.
        // We need to store an array of the images because a lot of the code for the manipulation of images is
        // client-side
        imageNode.map(function (index, item) {
            if ($(this).attr('data-fn')) {
                imagesArr.push($(this).attr('data-fn'));
            }
        });

        console.log(imagesArr);


        // Set the current based on the form.
        if ($("#newRestForm").length) {
            console.log('this is the new restaurant');
            current = 1;
        } else {
            // If this is edit restaurant, get the index of the selected img_thumbnail.
            console.log("This is the edit reataurant");
            current = $('.img_thumbnail.selected').attr('data-index');
            console.log(current);
        }


        $(".img_thumbnail").click(function (e) {
            selectImage();
        });

        // Delete image file
        $(".i_delete").click(function (e) {
            if ($(e.target).hasClass('icon_show')) {
                deleteImg();
            }
        });

        $(".btn-set").on("click", function () {
            console.log('Image has been set.');
            // Change the image on the form circle to be the selected image
            var newImg = $('#img_tn_' + current).attr('data-imgpath');
            console.log(newImg);
            // This gets set to null when the image is delete.
            if (!newImg) {
                console.log('Changeing newImg to NA.');
                newImg = $('#image_tn_1').attr('data-imgpath');

            }
            $('#rest_img').attr('src', '/static/' + newImg);

        });

        // Upload file change
        $("#upload").change(function (e) {
            console.log('Current: ') + current;
            var f = this.files[0];
            var sizeInMb = f.size / 1024;
            var sizeLimit = 1024 * 1; // if you want 1 MB
            if (sizeInMb > sizeLimit) {
                alert('Sorry the file exceeds the maximum size of 1 MB!');
            }
            else {

                if (checkDuplicate(f.name)) {
                    console.log('Diplicate file found.');
                    // $('#upload').val("");
                    alert("File is already uploaded!");
                } else {
                    console.log('No filename duplicates found.');
                    $(".file_container").css("display", "none");

                    var formData = new FormData();
                    formData.append('image', f, f.name);

                    $.ajax({
                        url: '/uploadImage',
                        data: formData,
                        processData: false,
                        contentType: false,
                        type: 'POST',
                        success: function (response) {
                            console.log(response);
                            // Reset the upload divs
                            $('#upload').val("");
                            $('.file_container').css("display", "block");
                            var returnedData = JSON.parse(response);

                            if ('status' in returnedData && returnedData.status == "OK") {
                                // Grab the index of the new element
                                var idx = returnedData.index;
                                // Grab the path of the file
                                var path = returnedData.path;
                                var HTMLimage = '<li class="img_thumbnail selected" id="img_thumbnail_%data%" data-index=' +
                                    '"%data%" ><img id="img_tn_%data%" class="img_tn img_tn_ul" data-imgpath=' +
                                    '"%path%" data-index="%data%" src="" alt="img"></li>';
                                var formattedHTML = HTMLimage.replace(/%data%/g, idx).replace(/%path%/g, path);
                                // Add the image thumbnail node
                                console.log('Adding: ' + formattedHTML);
                                $('.img_gallery').append(formattedHTML);
                                var node = $('.img_tn_ul').last();
                                var reader = new FileReader();

                                reader.readAsDataURL(f);


                                // Add click listener
                                $('#img_thumbnail_' + idx).click(function (e) {
                                    selectImage();
                                });

                                $("#btn-set").removeAttr("disabled");


                                $('#i_delete_' + idx).toggleClass('icon_show');

                                // Add the icon node
                                var HTMLicon = '<div class="icons_delete" id="icons_delete_%data%" data-index="%data%">' +
                                    '<i id="i_delete_%data%" data-index="%data%" data-tn="img_thumbnail_%data%" data-parent=' +
                                    '"icons_delete_%data%" class="fa fa-times-circle i_delete icon_show" aria-hidden=' +
                                    '"true"></i></div>'
                                var formattedIcon = HTMLicon.replace(/%data%/g, idx);
                                console.log(formattedIcon);
                                $('.image_container').append(formattedIcon);

                                // Add click listener
                                $('#i_delete_' + idx).click(function (e) {
                                    deleteImg();
                                });

                                // Set the value of #target to the idx of new uploaded image
                                $('#target').val(idx);

                                reader.onloadend = function () {
                                    node.attr("src", reader.result);
                                    imagesArr.push(f);
                                    if (current != idx) {
                                        oldImage = $('#img_thumbnail_' + current);
                                        oldIcon = $('#i_delete_' + current);
                                        console.log('Current is ' + current);
                                        toggleElements(oldImage, oldIcon);
                                        if (oldImage.hasClass('selected')) {
                                            console.log('toggling selected from previous selected image');
                                            oldImage.toggleClass('selected');
                                        }

                                        if (oldIcon.hasClass('icon_show')) {
                                            console.log('toggling icon_show from previous selected icon');
                                            oldIcon.toggleClass('icon_show');
                                        }
                                        current = idx;
                                        console.log('new current is ' + current.toString());
                                    }


                                    // Finally, check to see if we are at the max 5 images
                                    countImages();

                                };
                            }
                        },
                        error: function (error) {
                            console.log(error);
                        }
                    });

                }

            }
        });


        var checkDuplicate = function (filename) {
            // var imageNode = $(".img_tn");
            console.log('Checking duplicate: ' + filename);

            console.log(imagesArr);
            if (imagesArr.indexOf(filename) == -1) {
                console.log('filename not found. returning false.')
                return false;
            }

            console.log('filename found to already exist. Returning true');
            return true;
        };

        var countImages = function () {

            if (imagesArr.length) {
                if (imagesArr.length >= 5) {
                    console.log('No more images permitted until you delete one.');
                    $(".file_container").css('display', 'none');
                    $(".no_upload").css("display", "block");
                }
            }
        };

        var deleteImg = function () {
            console.log('delete click');

            //Grab the data-parent attribute which stores the ID of the parent
            var iconID = '#' + ($(event.target).attr("data-parent"));
            // Grab the index of the imagge
            var imgIndex = ($(event.target).attr("data-index"));
            // Grab the data-tn attribute which stores the ID of the img_thumbnail
            var imgID = '#' + ($(event.target).attr("data-tn"));
            var fn = ($(event.target).attr("data-fn"));
            var fullPath = ($(event.target).attr("data-imgpath"));
            // Grab the node objects
            var imgNode = $(imgID);
            var iNode = $(iconID);

            var data = {"image_index": imgIndex};

            $.ajax({
                url: '/deleteImage',
                contentType: 'application/json',
                data: JSON.stringify(data),
                dataType: 'json',
                type: 'POST',
                success: function (response) {
                    console.log(response);
                    // Remove the image from the page
                    $(iNode).remove();
                    $(imgNode).remove();
                    var idx = imagesArr.indexOf(fn);
                    if (idx > -1) {
                        imagesArr.splice(idx, 1);
                    }
                    console.log('Images can be added');
                    $(".file_container").css("display", "block");
                    $(".no_upload").css("display", "none");
                    // Check to see if the circld image is the one just deleted.
                    // If so, then switch it back to default image
                    console.log('The circle filename its checking is' + fn);
                    if (('#rest_img').src == fullPath || ('#rest_img').src == fn) {
                        // Set the circle to the default img
                        console.log('setting circle back to default.');
                        $('#rest_img').attr('src', imgDefault);
                        $("#btn-set").attr("disabled", "disabled");

                    }
                },
                error: function (error) {
                    console.log(error);
                    console.log("Error. Cannot Remove image from DOM.");
                }
            });
        };

        var selectImage = function () {
            var oldImage, oldIcon, newImage, newIcon;
            if ($(event.target).hasClass('img_thumbnail')) {
                // User clicks the thumbnail frame
                console.log('Clicked img_thumbnail.');
                if ($(event.target).hasClass('selected')) {
                    // do nothing
                } else {
                    // Let's toggle the old selection
                    oldImage = $('#img_thumbnail_' + current);
                    oldIcon = $('#i_delete_' + current);

                    toggleElements(oldImage, 'selected', 0);
                    toggleElements(oldIcon, 'icon_show', 0);

                    // Does not have selected, Going to toggle it.
                    $(event.target).toggleClass('selected');

                    current = $(event.target).attr('data-index');
                    console.log('current is now ' + current);
                    // Assign el to the target's associated icon
                    var el = $('#i_delete_' + current);
                    // Check if there is an icon associated with the thumbnail
                    if (el.hasClass('i_delete')) {
                        console.log('Toggling icon_show on target icon')
                        el.toggleClass('icon_show');
                    }
                    $('#target').children().val('');
                    // Enabled the submit button
                    $("#btn-set").removeAttr("disabled");
                }
            }
            // User clicks the image. Happens most of the time
            else {
                console.log('Clicked image..');
                if ($(event.target).parent().hasClass('selected')) {
                    // do nothing
                } else {
                    // Let's toggle the old selection
                    oldImage = $('#img_thumbnail_' + current);
                    oldIcon = $('#i_delete_' + current);

                    toggleElements(oldImage, 'selected', 0);
                    toggleElements(oldIcon, 'icon_show', 0);

                    // Assign the seleted variable to the data-index of the target
                    current = $(event.target).attr('data-index');
                    console.log('current is now ' + current);

                    newImage = $('#img_thumbnail_' + current);
                    newIcon = $('#i_delete_' + current);
                    //
                    toggleElements(newImage, 'selected', 1);
                    toggleElements(newIcon, 'icon_show', 1);

                    // Grab the filename and assign it to the target value.
                    var path = newImage.children().attr('data-index');
                    // console.log('setting value to ' + path);
                    $('#target').val(path);

                    // Set the submit button to enabled
                    console.log('Emabling button');

                    $("#btn-set").removeAttr("disabled");
                }
            }

        };

        var toggleElements = function (el, className, isNot) {
            if (isNot) {
                if (el.not(className)) {
                    el.toggleClass(className);
                }
            } else if (el.hasClass(className)) {
                el.toggleClass(className);
            }

        };

        // Main execution
        // Start off by counting the images
        countImages();


    };

    bindEvents();
    // Check to see if this is the newRestForm or editForm.
    if (($("#editRestForm").length) || ($("#newRestForm").length)) {
        // If so, bind form events.
        bindFormEvents();
    }


});
