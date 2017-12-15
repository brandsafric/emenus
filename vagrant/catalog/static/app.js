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
            $("#image_select").change(function (e) {
                var option = $('option:selected', this).attr('status');
                console.log($('option:selected'));
                console.log($('option:selected').attr('data-imagesrc'));
                console.log(option);
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

        // $('#image_select1').ddslick({
        //     onSelected: function(selectedData){
        //         console.log(selectedData.selectedData.value);
        //         // console.log(selectedData.value);
        //         var element = $('#image_select');
        //         console.log(element);
        //         // console.log(element.value);
        //         // var x = document.getElementById("image_select").value;
        //         // console.log(x);
        //         // var x = document.getElementById("image_select").name;
        //         // console.log(x);
        //
        //         // $('#image_select').value = selectedData.selectedData.value;
        //         // console.log($('#image_select'));
        //         // console.log($('#image_select').value);
        //         //callback function: do something with selectedData;
        //     }
        // });

        // console.log('here');

        // var sortListDir = function() {
        //   var list, i, switching, b, shouldSwitch, dir, switchcount = 0, t;
        //   console.log('click');
        //   list = document.getElementById("restaurant-list");
        //   switching = true;
        //   //Set the sorting direction to ascending:
        //   dir = "asc";
        //   //Make a loop that will continue until no switching has been done:
        //   while (switching) {
        //     //start by saying: no switching is done:
        //     switching = false;
        //     // b = list.getElementsByTagName("LI");
        //     b = list.getElementsByClassName("restaurant-card");
        //     console.log(b);
        //     //Loop through all list-items:
        //     for (i = 0; i < (b.length - 1); i++) {
        //       //start by saying there should be no switching:
        //       t = b[i].firstElementChild.nextElementSibling;
        //       shouldSwitch = false;
        //       /*check if the next item should switch place with the current item,
        //       based on the sorting direction (asc or desc):*/
        //       if (dir == "asc") {
        //         if (b[i].firstElementChild.nextElementSibling.innerText.toLowerCase() > b[i + 1].firstElementChild.nextElementSibling.innerText.toLowerCase()) {
        //           /*if next item is alphabetically lower than current item,
        //           mark as a switch and break the loop:*/
        //           console.log('1');
        //           shouldSwitch= true;
        //         }
        //       } else if (dir == "desc") {
        //         if (b[i].firstElementChild.nextElementSibling.innerText.toLowerCase() < b[i + 1].firstElementChild.nextElementSibling.innerText.toLowerCase()) {
        //           /*if next item is alphabetically higher than current item,
        //           mark as a switch and break the loop:*/
        //           shouldSwitch= true;
        //         }
        //       }
        //     }
        //     if (shouldSwitch) {
        //       console.log('switch');
        //       /*If a switch has been marked, make the switch
        //       and mark that a switch has been done:*/
        //       console.log(i);
        //       console.log(b[i].parentNode);
        //       console.log(b[i - 1]);
        //       console.log(b[i]);
        //
        //       b[i].parentNode.insertBefore(b[i - 1], b[i]);
        //
        //       // b[i].parentNode.parentNode.insertBefore(b[i + 1].parentNode, b[i].parentNode);
        //       switching = true;
        //       //Each time a switch is done, increase switchcount by 1:
        //       switchcount ++;
        //     } else {
        //       /*If no switching has been done AND the direction is "asc",
        //       set the direction to "desc" and run the while loop again.*/
        //       if (switchcount == 0 && dir == "asc") {
        //         dir = "desc";
        //         switching = true;
        //       }
        //     }
        //   }
        // };


        bindEvents();



});
