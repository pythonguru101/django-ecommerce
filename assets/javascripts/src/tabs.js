;(function($) {
    
    PowerBall.Tabs = (function() {

        var Tabs = function(node) {
            var self = this;
            this._node = $(node);
            this._tabs = this._node.find('.tabs__tab');
            this._containers = this._node.find('.tabs__content');

            this._tabs.each(function(i, item) {
                var tab    = $(item),
                    button = tab.find('.tab__button'),
                    id     = parseInt(tab.attr('data-tab-id'), 10);

                button.bind('click', function(evt) {
                    self._tabs.removeClass('tabs__tab_s');
                    tab.addClass('tabs__tab_s');
                    
                    
                    self._containers
                        .hide()
                        .map(function(j, c) {
                                var cid = parseInt($(c).attr('data-tab-id'), 10)
                                return cid === id ? c : null
                            })
                        .show();
                    
                    return false;
                });
            })
        }
        return Tabs;
    }());

    $.fn.PowerBallTabs = function() {
        var _tabs = [];
        this.each(function(i, item) {
            _tabs.push(new PowerBall.Tabs(item));
        });
    }
}(jQuery));