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

            $(".img_thumbnail").click(function (e) {
                console.log('click');
                console.log(e.target);
                // $(event.target).hasClass('textbox')
                if ($(event.target).hasClass('img_thumbnail')) {
                    console.log('it is thumbnail');
                    $(event.target).toggleClass('selected');
                    $(event.target).siblings(".selected").toggleClass("selected");
                      // var myUL = $(this).siblings(".selected").toggleClass("showme");
                    var src = $(event.target).firstElementChild;
                    console.log($(event.target));
                   console.log($(event.target)[0]);
                    console.log(src);
                    $('#target').child().val(src);
                }
                else {
                    console.log('it is image');
                    console.log($(event.target));
                    $(event.target).parent().toggleClass('selected');
                    // $(this)[0].addClass('yellow_border');
                    $(event.target).parent().siblings(".selected").toggleClass("selected");
                    var src = $(event.target)[0].src;
                    console.log(src);
                    $('#target').val(src);

                }
                // e.target.addClass('yellow_border');
            });
            $("#image_select").change(function (e) {
                var option = $('option:selected', this).attr('status');
                var datasrc = ($('option:selected').attr('data-imagesrc'));
                var image = $('#img_thumbnail').attr('src');
                $('#img_thumbnail').attr('src', datasrc);
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
                }
                 });
        };
        $( "select" )
          .change(function () {
            var self = this;
            console.log(self);
            var strOption = self.options[self.selectedIndex].value;
            console.log(self.options[self.selectedIndex]);
            // console.log(self.options("data-imgsrc"));
            // console.log(self.attr('data-imgsrc'));
            // str = $( "select option:selected" ).value();
            // console.log(value)
            // $( "div" ).text( str );
              console.log(strOption);
          });

        $("#image_select > option").each(function() {
            console.log(this.text);
            console.log(this.getAttribute('data-imagesrc'));
            var path = this.getAttribute('data-imagesrc');
            this.style.backgroundImage = "url(" + path + ")";
            console.log(this.style);
        });



        bindEvents();



});
