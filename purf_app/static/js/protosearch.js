// TODO - Throttle searches when enter button is held down, or only search once

var search_prof = (function () {

    // the methods that are publicly accessible.
    // ENSURE THAT NO PRIVATE DATABASE VALUES CAN BE ACCESSED!!
    var public = {};
    var searchform, searchbox, searchbutton, searchresults, searchareas;

    // INITIALIZATION
    init = function () {
        searchform = $("#search-form");
        searchbox = $("#searchbox").first();
        searchbutton =  $("#searchbutton").first();
        searchresults = $("#search-results");

        // set trigger on enter
        searchbox.keyup(function(event){
            if(event.keyCode == 13){
                $("#id_of_button").click();
            }
        });

        // set trigger on button press
        searchform.submit(function(e) {
            // submit the form
            // $(this).ajaxSubmit();
            search();
            // return false to prevent normal browser submit and page navigation
            e.preventDefault();
            return false;
        });

    }

    // MAIN SEARCH FUNCTION
    search = function () {
        query = searchbox.val()
        querystring = ""
        query = query.trim().split(/[\s,]+/)
        $.each(query, function(key, value){
            querystring += "query=" + value + "&"
        })
        $(".checkbox :checkbox:checked").each(function(key, value){
            querystring += "research_areas=" + value.value + "&"
        })

        $.getJSON("api/v1/search/?" + querystring + "format=json", function(data) {
            searchresults.empty();
            var items = [];
            $.each( data.objects, function( key, val ) {
                items.push(
                        '<div class="row" style="padding: 10px 0; background:white; margin: 1px 0"> \
                          <div class="profile col-md-2"> \
                            <img src=' + val.image + ' height=100 /> \
                          </div> \
                          <div class="name col-md-5">\
                            <a href="profile/' + val.netid + '">'
                                + val.name +
                            '</a>\
                          </div> \
                        </div>'
                        );
            });

            searchresults.append(items.join(""))
        })
    }

    // on document ready, initialize the function
    $(init())

    return public
}());