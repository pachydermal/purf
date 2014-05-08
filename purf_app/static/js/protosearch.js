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
            $('.'+"highlighted").removeClass("highlighted");     //Remove old search highlights
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
    var searchform, searchbox, searchbutton, searchresults, searchloading;

    // INITIALIZATION
    init = function () {

        $("h3").click(function(){
            $(".search-result").toggleClass("two");
        })

        searchform = $("#search-form");
        searchbox = $("#searchbox").first();
        searchbutton =  $("#searchbutton").first();
        searchresults = $("#search-results");
        searchloading = $("#search-loading");

        // check if search page
        if ($('#search-results').length) {
            searchbox.focus();
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
            History.Adapter.bind(window,'statechange',function(){
                stateless_search();
            });

            // search on first page load. This is a big cheat.
            // Once search is finalized, then we have to write a server-side
            // version of this.
            stateless_search();
        } else {
            // if homepage
            searchform.submit(function(e) {
                window.location = "/search/?" + build_search_query()
                // return false to prevent normal browser submit and page navigation
                e.preventDefault();
                return false;
            });
        }

        if ($('#home-container').length) {
            searchbox.focus();
        }

        // autocomplete
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

        searchbox.on('typeahead:selected', function(e, item) {
            window.location = item.link;
        });
        searchbox.on('typeahead:cursorchanged', function(e, item, dataset){
            return;
        });

    }

    stateless_search = function () {
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

    get_queries = function () {
        return searchbox.val().trim().split(/[\s,\&;]+/)
    }

    build_search_url = function () {
        return "/api/v1/search/?" + build_search_query() + "format=json"
    }

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

    // MAIN SEARCH FUNCTION
    search = function () {
        searchresults.empty();

        add_results(build_search_url());
    }

    add_results = function (query_url) {

        searchbox.typeahead('close');

        searchloading.addClass("loading");

        $.getJSON(query_url, function(data) {

            $('#search-load-more').remove();

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
                    var department_html = ""
                    if (val.department) {
                        var departments = val.department.split(";")
                        for (var i = 0; i < departments.length; i++) {
                            department_html += '<span class="label ';
                            department_html += departments[i] == "COS" ? 'label-warning' : 'label-default';
                            department_html += '">' + departments[i] + '</span>';
                        }
                    }
                    var research_areas = val.research_areas.split(';').join("</p><p>");
                    var research_topics = val.research_topics.split(';').join("</p><p>");
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

                // put an image placeholder for images that fail to load.
                $('img').error(function(){
                    $(this).attr('src','http://placekitten.com/200/201?image=' + Math.floor(Math.random() * 17));
                });

                var queries = get_queries();
                for (var i = 0; i < queries.length; i++) {
                    searchAndHighlight(queries[i], "#search-results", true)
                }

                // show button if there are more results
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

    // on document ready, initialize the function
    $(init())

    return public
}());
