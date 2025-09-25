(function($){
    $.fn.turn = function(options){
        // Minimal fake flipbook (you can replace with real Turn.js)
        $(this).css({"display":"flex","overflow-x":"scroll"});
        $(this).children().css({"min-width":"400px","margin":"10px"});
    }
})(jQuery);
