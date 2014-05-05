// TODO - Throttle searches when enter button is held down, or only search once

// finds queries within the url.
(function($) {
    $.QueryString = function(a) {
        a = typeof a !== 'undefined' ? a : window.location.search.substr(1).split('&');
        if (a == "") return {};
        var b = {};
        for (var i = 0; i < a.length; ++i)
        {
            var p=a[i].split('=');
            if (p.length != 2) continue;
            if (typeof b[p[0]] === 'undefined') {
                b[p[0]] = [];
            }
            b[p[0]].push(decodeURIComponent(p[1].replace(/\+/g, " ")));
        }
        return b;
    }
})(jQuery);

// search and highlight text on the page
// http://teeohhem.com/2011/02/20/search-for-and-highlight-text-on-a-page-with-jquery/
function searchAndHighlight(searchTerm, selector, removePreviousHighlights) {
    if(searchTerm) {
        //var wholeWordOnly = new RegExp("\\g"+searchTerm+"\\g","ig"); //matches whole word only
        //var anyCharacter = new RegExp("\\g["+searchTerm+"]\\g","ig"); //matches any word with any of search chars characters
        var selector = selector || "body",                             //use body as selector if none provided
            searchTermRegEx = new RegExp("("+searchTerm+")","gi"),
            matches = 0,
            helper = {};
        helper.doHighlight = function(node, searchTerm){
            if(node.nodeType === 3) {
                if(node.nodeValue.match(searchTermRegEx)){
                    matches++;
                    var tempNode = document.createElement('span');
                    tempNode.innerHTML = node.nodeValue.replace(searchTermRegEx, '<span class="highlighted">$1</span>');
                    node.parentNode.insertBefore(tempNode, node );
                    node.parentNode.removeChild(node);
                }
            }
            else if(node.nodeType === 1 && node.childNodes && !/(style|script)/i.test(node.tagName)) {
                $.each(node.childNodes, function(i,v){
                    helper.doHighlight(node.childNodes[i], searchTerm);
                });
            }
        };
        if(removePreviousHighlights) {
            $('.'+highlightClass).removeClass(highlightClass);     //Remove old search highlights
        }

        $.each($(selector).children(), function(index,val){
            helper.doHighlight(this, searchTerm);
        });
        return matches;
    }
    return false;
}

// ACTUAL SEARCH STUFF BEGINS HERE

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

        searchbox.focus();

        // check if homepage or searchpage
        if ($('#home-container').length) {
            // if homepage
            searchform.submit(function(e) {
                window.location = "search/?" + build_search_query()
                // return false to prevent normal browser submit and page navigation
                e.preventDefault();
                return false;
            });
        } else {
            // if searchpage
            // set trigger on button press
            searchform.submit(function(e) {
                // submit the form
                // $(this).ajaxSubmit();

                // search occurs on history state change
                var querystring = build_search_query();
                History.pushState(null, null, "?" + querystring);

                // return false to prevent normal browser submit and page navigation
                e.preventDefault();
                return false;
            });

            // search again when the back button is pressed
            if (History.enabled) {
                State = History.getState();
                // set initial state to first page that was loaded
                History.pushState({urlPath: window.location.pathname}, $("title").text(), State.urlPath);
            } else {
                return false;
            }

            History.Adapter.bind(window,'statechange',function(){
                stateless_search();
            });

            stateless_search();
        }
    }

    stateless_search = function () {
        var query = $.QueryString()["query"];
        if (typeof query !== 'undefined' && query.length > 0) {
            searchbox.val(query.join(" "));
            search();
        }
    }

    get_queries = function () {
        return searchbox.val().trim().split(/[\s,\&;]+/)
    }

    build_search_query = function () {
        var querystring = ""
        $.each(get_queries(), function(key, value){
            querystring += "query=" + value + "&"
        })
        $(".checkbox :checkbox:checked").each(function(key, value){
            querystring += "research_areas__icontains=" + value.value + "&"
        })
        return querystring
    }

    // MAIN SEARCH FUNCTION
    search = function () {
        var querystring = build_search_query();

        $.getJSON("../api/v1/search/?" + querystring + "format=json", function(data) {
            searchresults.empty();
            var items = [];

            $.each( data.objects, function( key, val ) {
                var research_areas = val.research_areas.split(';').join("</p><p>");
                var research_topics = val.research_topics.split(';').join("</p><p>");
                items.push(
                        '<a href="../profile/' + val.netid + '">\
                        <div class="row search-result"> \
                          <div class="profile col-md-1 search-thumbnail-container"> \
                            <img class="search-thumbnail" src=' + val.image + '/> \
                          </div> \
                          <div class="name col-md-2">\
                            <p class="search-name">'
                                + val.name +
                            '</p>\
                            <p class="search-department">' + val.department + '</p>\
                          </div> \
                          <div class="search-research-areas col-md-4">\
                            <p>' + research_areas + '</p> \
                          </div> \
                          <div class="search-research-topics col-md-4">\
                            <p>' + research_topics + '</p> \
                          </div> \
                        </div> \
                        </a>'
                        );
            });

            searchresults.append(items.join(""))

            var queries = get_queries();
            for (var i = 0; i < queries.length; i++) {
                searchAndHighlight(queries[i], "#search-results")
            }
        })
    }

    // on document ready, initialize the function
    $(init())

    return public
}());
