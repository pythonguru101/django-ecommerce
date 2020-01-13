;(function($) {
    var plural = PowerBall.Numeral.plural,
        cash   = PowerBall.Numeral.cash;
    
    
    var serializeForm = function(form) {
        var data   = $(form).serializeArray(),
            result = {};

        $.each(data, function(i, item) { 
            result[item.name] = item.value
        });
        return result
    }

    PowerBall.Cart = (function() {

        function _hold () {
            $('[data-cart-type="button"],[data-cart-type="button"] input')
                .attr('disabled', true)
                .addClass('disabled');
        }

        function _release () {
            $('[data-cart-type="button"],[data-cart-type="button"] input')
                .attr('disabled', null)
                .removeClass('loading disabled');
        }

        function _updateView (cart) {

            $('[data-cart-type="cart"]').show();
            $('[data-cart-type="goods_count"]').html(plural(cart.goods_total, 'товар,товара,товаров', true));
            $('[data-cart-type="sub_total_price"]').html(cash(cart.price_total))

            var productListIds = $.map(cart.products, function(item, i) {
                return parseInt(item.product.id, 10);
            });

            var productListNodeIds = $('[data-cart-type="product"]').map(function(i, item) {
                return parseInt($(this).attr('data-cart-id'), 10);
            });
            
            $.each(productListNodeIds, function(i, item) {
                if ($.inArray(item, productListIds) === -1) {
                    $('[data-cart-id="' + item + '"]').remove();
                }
            });

            $.each(cart.products, function(i, item) {
                var productNode = $('[data-cart-id="' + item.product.id + '"]');
                productNode.find('[data-cart-type="product_quantity"]')
                    .html(item.quantity);
                productNode.find('[data-cart-type="product_price"]')
                    .html(cash(item.price_total));
            });
            
            var addPrice = 0;
            $(':selected[data-cart-price]').each(function(i, pr) {
                addPrice += parseInt($(pr).attr('data-cart-price'), 10);
            });
            $('[data-cart-type="price_total"]').html(cash(cart.price_total + addPrice))
        }
        
        function _fetch () {
            $.ajax({
                url: '/shop/cart/',
                contentType: 'application/json',
                dataType: 'json',
                type: 'GET', 
                beforeSend: function() {
                    _hold();
                },
                error: function(xhr, status, error) {
                    _release();
                },
                success: function(data, status, xhr) {
                    _updateView(data.cart);
                    _release();
                }
            });
        }

        function _put (data) {
            $.ajax({
                url: '/shop/cart/',
                type: 'POST', 
                dataType: 'json',
                data: data,
                beforeSend: function() {
                    _hold();
                    $('[data-cart-type="button"][data-cart-id="' + data.product + '"],[data-cart-type="button"][data-cart-id="' + data.product + '"] input')
                        .addClass('loading')
                },
                error: function(xhr, status, error) {
                    _release();
                },
                success: function(data, status, xhr) {
                    if (data.cart.goods_total === 0) {
                        document.location = '/';
                    } else {
                        _updateView(data.cart);
                        _release();
                    }
                }
            });
        }

        var _dataTypes = {
                'add'           : 'form[data-cart-action="add"]',
                'remove'        : 'form[data-cart-action="remove"]',
                'removeProduct' : 'form[data-cart-action="remove_product"]'
            },
            _actions = {
                add           : _put,
                remove        : _put,
                removeProduct : _put
            };


        var Cart = function() {

            var self = this;
            $.each(_dataTypes, function(action, selector) {
                $(selector).bind('submit', function() {
                    var data = serializeForm($(this));
                    _actions[action].call(self, data);
                    return false;
                });
            });


            var changeShippingType = function(node) {
                var optionals = $('[data-cart-optional]')
                var selected = node.find('option:selected'),
                    require  = selected.attr('data-cart-require'),
                    help     = selected.attr('data-cart-help');
                    
                $('[data-cart-type="help"]').html(help);
                optionals.hide();
                if (typeof require !== 'undefined') {
                    var optSelectors = $.map(require.split(','), function(item) {
                        return item;
                    });
                    $.each(optSelectors, function(i, item) {
                        optionals.filter('[data-cart-type="' + item + '"]').show();
                    })
                }
                _fetch();
            }
            
            var shippingTypeNode = $('[data-cart-type="shipping_type"]');
            if (shippingTypeNode.length) {
                shippingTypeNode.bind('change', function(evt) {
                    changeShippingType($(this));
                });
                changeShippingType(shippingTypeNode);
            }
        }
        
        $.extend(Cart.prototype, {});
        return Cart;
        
    })();
    
}(jQuery));