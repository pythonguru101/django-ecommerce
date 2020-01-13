(function($) {
    var StickyNode = function StickyNode(options) {
        var node    = $(this),
            offset  = node.offset(),
            maxDown = $(document).height() - node.height() - offset.top;
        
        var scrollProc = function scrollProc(evt) {
            var scrollTop = $(window).scrollTop();
            if (scrollTop >= offset.top) {
                if (scrollTop < maxDown) {
                    node.css({
                        'position': 'fixed',
                        'z-index': 9999,
                        'top': 0
                    });
                }
            } else {
                node.css({
                    'position': '',
                    'z-index': '',
                    'top': ''
                });
            }
        }
        scrollProc();
        $(window).scroll(scrollProc);
        return node;
    }
    $.fn.StickyNode = StickyNode;
    return StickyNode;
})(jQuery);