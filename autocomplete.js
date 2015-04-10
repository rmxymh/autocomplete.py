// This script depends on jQuery
function get_autocomplete_word_list(word)
{
    $.getJSON("/autocomplete.py/backend/autocomplete.py?keyword=" + word,
        function(data) {
            var item = [];
            for(i=0; i<data.length; ++i)
            {
                suggestion = '<li id="' + data[i]["key"] + '">' + data[i]["key"] + ": Count = " + data[i]["count"] + '</li>';
                item.push(suggestion);
            }
            
            $("#showarea").html(item);
        }
    );
}