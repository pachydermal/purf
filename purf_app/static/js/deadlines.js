/*
 * deadlines.js
 * Controls the deadline functionality on the home page
 *
 * Much like protosearch.js, this script is functional, but not
 * the nicest to read.
 *
 * Currently, reads the full list of deadlines directly from the HTML.
 * As we do not have an accurate list of deadlines for next year,
 * deadlines are approximate. Additionally, which deadline you are up
 * to currently does not save.
 */


var deadlines = (function () {

    // the methods that are publicly accessible.
    var public = {};

    // the starting deadline index is hardcoded to 2 for now.
    var index = 2;
    var done_message = "Go and celebrate! You're done!";

    // retrieves the next deadline from the list
    get_next_deadline = function () {
        index += 1;

        var data_div = $('.home-all-deadlines .home-deadline[data-index=' + index + ']');

        // if there is another deadline, get its data and add invisible HTML
        if (data_div.length) {
            var date = data_div.children(".date").text();
            var lead = data_div.children(".lead").text();

            $(".home-deadline.main").after(
                '<div class="home-deadline main vertical-center-inner" style="display:none">\
                 <p class="date">' + date + '</p>\
                 <p class="lead">' + lead + '</p>\
                 <button class="btn active">I\'m done</button>\
                 <a class="see-all">see all deadlines</a>\
                 </div>'
            );
        }
        // otherwise, all deadlines are complete, so display the 'celebrate' message
        else {
            $(".home-deadline.main").after(
                '<div class="home-deadline main vertical-center-inner" style="display:none">\
                 <p class="lead">' + done_message + '</p>\
                 <button class="btn celebrate">Celebrate</button>\
                 <a class="see-all">see all deadlines</a>\
                 </div>'
            );
        }

        // fade out and remove the old deadline, fade in the new deadline
        var old_deadline = $(".home-deadline.main:eq(0)");
        var new_deadline = $(".home-deadline.main:eq(1)")
        old_deadline.fadeOut(200);
        new_deadline.delay(200).slideDown(200);
        setTimeout(function(){old_deadline.remove()},200);
    }

    // INITIALIZATION
    init = function () {

        // bind onclick events to transition between showing all deadlines or the currrent deadline
        var current_deadline = ".home-deadline.main",
            all_deadlines = ".home-all-deadlines,.x-button";
        $(".x-button").click(function(){
            $(current_deadline).fadeIn(200);
            $(all_deadlines).fadeOut(200);
        });
        $(document).on( "click", ".home-deadline.main .see-all", function(){
            $(current_deadline).fadeOut(200);
            $(all_deadlines).fadeIn(200);
        });

        // bind click event to the "Done" button to get the next deadline
        $(document).on( "click", ".home-deadline.main .btn.active", function(){
            var button = $(".home-deadline.main .btn");
            button.removeClass("active").css({"border-color":"white","color":"white"}).text("Yay!");
            setTimeout(function(){get_next_deadline()},500);
        });

        // bind click event to the "celebrate" button to do a random CSS animation. Requires animate.css
        var animation_list = ["flip", "swing", "tada", "bounce", "rubberBand", "shake", "pulse", "wobble"]
        $(document).on( "click", ".home-deadline.main .btn.celebrate", function(){
            var random_animation = animation_list[Math.floor(Math.random() * animation_list.length)];
            var selection = $("p, h1, h3, a, button, input");
            selection.addClass("animated " + random_animation);
            setTimeout(function(){
                selection.removeClass(random_animation);
            },1000);
        });
    }

    // on document ready, initialize the function
    $(init())

    return public
}());
