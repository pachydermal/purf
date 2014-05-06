
var deadlines = (function () {

    // the methods that are publicly accessible.
    var public = {};

    // hard coded values
    var index = 2;
    var done_message = "Go and celebrate! You're done!";

    get_next_deadline = function () {
        index += 1;

        var data_div = $('.home-all-deadlines .home-deadline[data-index=' + index + ']');

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
        else {
            $(".home-deadline.main").after(
                '<div class="home-deadline main vertical-center-inner" style="display:none">\
                 <p class="lead">' + done_message + '</p>\
                 <button class="btn celebrate">Celebrate</button>\
                 <a class="see-all">see all deadlines</a>\
                 </div>'
            );
        }

        var old_deadline = $(".home-deadline.main:eq(0)");
        var new_deadline = $(".home-deadline.main:eq(1)")
        old_deadline.fadeOut(200);
        new_deadline.delay(200).slideDown(200);
        setTimeout(function(){old_deadline.remove()},200);
    }

    // INITIALIZATION
    init = function () {
        var group_a = ".home-deadline.main",
            group_b = ".home-all-deadlines,.x-button";
        $(".x-button").click(function(){
            $(group_a).fadeIn(200);
            $(group_b).fadeOut(200);
        });
        $(document).on( "click", ".home-deadline.main .see-all", function(){
            $(group_a).fadeOut(200);
            $(group_b).fadeIn(200);
        });

        $(document).on( "click", ".home-deadline.main .btn.active", function(){
            var button = $(".home-deadline.main .btn");
            button.removeClass("active").css({"border-color":"white","color":"white"}).text("Yay!");
            setTimeout(function(){get_next_deadline()},500);
        });

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
