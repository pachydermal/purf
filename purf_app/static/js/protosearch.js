/*
 * Protosearch.js
 * Contains search functionality needed by all pages of the website
 *
 * Named such because it is a PROTOtype SEARCH script made without
 * code maintainability in mind. It's perfectly functional, but not
 * the nicest to read.
 *
 * This file is loaded on every page because it contains a function
 * necessary to search from the navbar
 */

// finds queries within the url.
// http://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
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
            $('.'+"highlighted").removeClass("highlighted");     //Remove old search highlights
        }

        $.each($(selector).children(), function(index,val){
            helper.doHighlight(this, searchTerm);
        });
        return matches;
    }
    return false;
}

/*
 * Some notes on History.js:
 * History.js allows the dynamic search page to change the url on search
 * have normal foward/back button functionality. However, this comes at
 * the price of some somewhat unconventional code organization:
 *
 * History.js keeps track of a history queue. Pushing on a new queue or
 * accessing elements of the queue (by pressing forward/back) triggers
 * an event. This event can be treated as a 'page reload' in a sense.
 * Thus in this case, every time a state change is detected, it will
 * perform a search using the new/old query.
 */

var search_prof = (function () {

    // the methods that are publicly accessible.
    var public = {};

    // stored variables for convenience
    var searchform, searchbox, searchbutton, searchresults, searchloading;
    var user_department;

    // INITIALIZATION
    init = function () {

        // get the user's department
        user_department = $('meta[name=user_department]').attr("content");

        // Bind on click of the button at the top of search results to change the css
        // of all the search results, so that they display the full results
        $("h3").click(function(){
            $(".search-result").toggleClass("two");
        })

        // Get the HTML elements
        searchform = $("#search-form");
        searchbox = $("#searchbox").first();
        searchbutton =  $("#searchbutton").first();
        searchresults = $("#search-results");
        searchloading = $("#search-loading");

        if ($('#search-results').length) {
            // for the search page

            // allow the user to type a query immediately
            searchbox.focus();

            // make search button do a search call
            searchform.submit(function(e) {
                // submit the form
                // $(this).ajaxSubmit();

                var querystring = build_search_query();
                History.pushState(null, null, "?" + querystring);

                // return false to prevent normal browser submit and page navigation
                e.preventDefault();
                return false;
            });

            // Binds an action to when History.js detects a history state change. Requires History.js
            // this searches every time there is a state change
            // a state is pushed on search and when the back/forward buttons are pressed
            History.Adapter.bind(window,'statechange',function(){
                search();
            });

            // search on first page load.
            initial_search();
        } else {
            // for all non-search pages
            // make search button send you to the appropriate search page
            searchform.submit(function(e) {
                window.location = "/search/?" + build_search_query()
                // return false to prevent normal browser submit and page navigation
                e.preventDefault();
                return false;
            });
        }

        // for the home page
        if ($('#home-container').length) {
            // allow the user to type a query immediately
            searchbox.focus();
        }

        // Load the autocomplete functionality. Requires Typeahead.js
        // Bloodhound is the data-loading side of Typeahead.js
        // It can take local and remote databases, but in this case only uses a remote one.
        var professorAutocomplete = new Bloodhound({
            datumTokenizer: function (d) {
                return Bloodhound.tokenizers.whitespace(d.value);
            },
            queryTokenizer: Bloodhound.tokenizers.whitespace,
            remote: {
                url: '/api/v1/search/?%QUERYformat=json',
                replace: function (url, query) {
                    var querystring = ""
                    $.each(get_queries(), function(key, value){
                        querystring += "query=" + value + "&"
                    })
                    $(".checkbox :checkbox:checked").each(function(key, value){
                        querystring += "research_areas=" + value.value + "&"
                    })
                    return "/api/v1/search/?" +  querystring + "format=json"
                },
                filter: function (data) {
                    return $.map(data.objects, function (professor) {
                        return {
                            name: professor.name,
                            department: professor.department,
                            link: "/profile/" + professor.netid,
                        };
                    });
                }
            }
        });
        professorAutocomplete.initialize();
        // typeahead is the UI side of Typeahead.js
        // 'highlight' bolds the matching portions of the results.
        // 'display' attribute is blank, because in this case, clicking on a link results in going
        // directly to the professor page. By clearing the textbox, it makes it clear that selecting
        // an option will not search, but instead going to the page.
        searchbox.typeahead({
            highlight: true,
          },
          {
            displayKey: "",
            templates: {
            suggestion: function(item){ return item.name + ' <span class="department">' + item.department.split(";").join("\/") + "</span>"},
          },
          source: professorAutocomplete.ttAdapter(),
        });
        // when you select an option, go directly to the webpage of the professor
        searchbox.on('typeahead:selected', function(e, item) {
            window.location = item.link;
        });
        searchbox.on('typeahead:cursorchanged', function(e, item, dataset){
            return;
        });

    }

    // deconstructs the url to initialize the searchbox and research_areas checkboxes
    // then performs a search
    initial_search = function () {
        var query = $.QueryString()["query"];
        if (typeof query !== 'undefined' && query.length > 0) {
            searchbox.val(query.join(" "));
        }
        var areas = $.QueryString()["research_areas"];
        if (typeof areas !== 'undefined') {
            for ( var i = 0; i < areas.length; i ++ ) {
                $(".checkbox:contains(" + areas[i] + ") input").prop('checked', true);
            }
        }
        if ((typeof query !== 'undefined' && query.length > 0) ||
            (typeof research_areas !== 'undefined' && areas.length > 0)) {
            search();
        }
    }

    // gets the queries from the searchbox
    get_queries = function () {
        return searchbox.val().trim().split(/[\s,\&;]+/)
    }

    // creates the api url
    build_search_url = function () {
        return "/api/v1/search/?" + build_search_query() + "format=json"
    }

    // creates the url query string by checking the value of the checkboxes and searchbox
    build_search_query = function () {
        var querystring = ""
        $.each(get_queries(), function(key, value){
            querystring += "query=" + value + "&"
        })
        $(".checkbox :checkbox:checked").each(function(key, value){
            querystring += "research_areas=" + value.value + "&"
        })
        return querystring
    }

    // performs a new search - clears the previous search results
    search = function () {
        searchresults.empty();

        add_results(build_search_url());
    }

    // gets data from the passed in url, appends results to the search results area
    add_results = function (query_url) {

        // close the autocomplete panel if it's open
        searchbox.typeahead('close');

        // spin the loading spinner
        // (as of this writing, appears with a delay of .2 seconds)
        searchloading.addClass("loading");

        $.getJSON(query_url, function(data) {
            // on successful query:

            // remove the 'load more' button from the bottom of the page
            $('#search-load-more').remove();

            // hide the loading spinner
            searchloading.removeClass("loading");

            // what to display if there is nothing
            if (!data.objects.length) {
                searchresults.append('<div align="center">\
                                    <h4 align="center">No Results Found</h4>\
                                    <p>Hint: Try using more search queries, or partial words.</p>\
                                    </div>');
            } else {
                var items = [];
                $.each( data.objects, function( key, val ) {
                    // Make departments go in fancy label spans
                    // if the department matches the user_department, it is highlighted
                    var department_html = ""
                    if (val.department) {
                        var departments = val.department.split(";")
                        for (var i = 0; i < departments.length; i++) {
                            department_html += '<span class="label ';
                            department_html += departments[i] == user_department ? 'label-warning' : 'label-default';
                            department_html += '">' + departments[i] + '</span> ';
                        }
                    }

                    // Add line breaks and remove the semicolons in research areas/topics
                    var research_areas = val.research_areas.split(';').join("</p><p>");
                    var research_topics = val.research_topics.split(';').join("</p><p>");

                    // Format the result and add to the list
                    items.push(
                            '<a href="/profile/' + val.netid + '">\
                            <div class="row search-result"> \
                              <div class="profile col-sm-1 search-thumbnail-container"> \
                                <img class="search-thumbnail" src=' + val.image + '/> \
                              </div> \
                              <div class="name col-sm-2">\
                                <p class="search-name">'
                                    + val.name +
                                '</p>\
                                <p class="search-department">' + department_html + '</p>\
                              </div> \
                              <div class="search-research-areas col-sm-4">\
                                <p>' + research_areas + '</p> \
                              </div> \
                              <div class="search-research-topics col-sm-4">\
                                <p>' + research_topics + '</p> \
                              </div> \
                            </div> \
                            </a>'
                            );
                });

                searchresults.append(items.join(""));

                // put an kitten image placeholder for images that fail to load.
                $('img').error(function(){
                    $(this).attr('src','http://placekitten.com/200/201?image=' + Math.floor(Math.random() * 17));
                });

                // highlight the query text in the results
                var queries = get_queries();
                for (var i = 0; i < queries.length; i++) {
                    // clear highlights the first time
                    if ( i == 0 ) searchAndHighlight(queries[i], "#search-results", true);
                    searchAndHighlight(queries[i], "#search-results", false);
                }

                // show a button if there are more results
                if (data.meta.next) {
                    searchresults.append('<div id="search-load-more" class="row">\
                                            <div id="search-load-more-btn" class="col-sm-4 col-sm-offset-4 btn btn-warning">Load more results</div>\
                                          </div>');
                }
                $('#search-load-more-btn').click(function(){
                    add_results(data.meta.next);
                });
            }
        });
    }

    // on document ready, initialize the search module
    $(init())

    return public
}());
