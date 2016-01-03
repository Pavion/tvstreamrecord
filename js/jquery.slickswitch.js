/**
* jQuery SlickSwitch
*
* For documentation, see http://michaelgolus.com/projects/slickswitch/
*
* Copyright (c) 2011 Matt and Michael Golus
* Copyright (c) 2015 Luke Kirby
*
* Dual licensed under the MIT and GPL licenses:
* http://www.opensource.org/licenses/mit-license.php
* http://www.gnu.org/licenses/gpl.html
*
* Version: 1.1.1
*/

(function ($) {

    $.fn.slickswitch = function (method) {
        if (methods[method]) {
        	return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || !method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Method ' + method + ' does not exist');
        }
    };
	
    var methods = {
        init: function (options) {
		
            var settings = $.extend( {
                cssPrefix: 'ss-',
                animationDuration: 200,
                toggled: function (e) { },
                toggledOn: function (e) { },
                toggledOff: function (e) { }
            }, options);

            return this.each(function () {
                var self = $(this);
                var div = $('<a>');
                
				// Check if SlickSwitch is already initialised on this element
				if (self.hasClass(settings.cssPrefix + 'loaded')) {
					return;
				}
				
                self.bind('ss-toggle', function () {
					var elem = self[0];
                    if (elem.checked) {
                        elem.checked = false;
                        self.removeAttr("checked");
                        settings.toggledOff(self);
                    } else {
                        elem.checked = true;
                        self.attr("checked","checked");
                        settings.toggledOn(self);
                    }
                    settings.toggled(self);
                    self.trigger('ss-update');
                });

                self.bind('ss-toggleOn', function () {
                    self[0].checked = true;
                    settings.toggledOn(self);
                    settings.toggled(self);
                    self.trigger('ss-update');
                });

                self.bind('ss-toggleOff', function () {
                    self[0].checked = false;
                    settings.toggledOff(self);
                    settings.toggled(self);
                    self.trigger('ss-update');
                });

                self.bind('ss-update', function (o, disableAnimation) {
				
					// Hide or show the slider. Uses setTimeout to ensure hide() and show() are fired properly
					if ( self[0].checked ) {
						setTimeout(function() {
							$('span', div).eq(0).show(disableAnimation ? 0 : settings.animationDuration || 500);
							$('span', div).eq(1).animate({ left: div.width() - $('span', div).eq(1).outerWidth(true) + 'px' }, 
															disableAnimation ? 0 : settings.animationDuration || 500);
						}, 10);
                    } else {
						setTimeout(function() {
							$('span', div).eq(0).hide(disableAnimation ? 0 : 100);
							$('span', div).eq(1).animate({ left: '0px' }, disableAnimation ? 0 : 100);
						}, 10);
                    }

                });

				// Use native DOM method to create span element instead of using $('<span>').addClass('...')
				var switchElemSlider = document.createElement("span");
				switchElemSlider.className = settings.cssPrefix + 'on';
					
				var switchElemRound = document.createElement("span");
				switchElemRound.className = settings.cssPrefix + 'slider';
				
				self.after(	
					div.attr('class', self.attr('class'))
						.append(switchElemSlider)
						.append(switchElemRound)
						.on("click", function() {
							self.trigger('ss-toggle');
							return false;
						})
				);
				
				self.addClass(settings.cssPrefix + 'loaded');

                self.trigger('ss-update', true);
                self.hide();
            });
        },
        toggle: function () {
            $(this).trigger('ss-toggle');
        },
        toggleOn: function () {
            $(this).trigger('ss-toggleOn');
        },
        toggleOff: function () {
            $(this).trigger('ss-toggleOff');
        }
    };
})(jQuery);

