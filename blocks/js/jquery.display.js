(function($) {
$.extend(
		$.fn, {
			display: function () {
				if (!$(this).length) {return;}			
				$(this).each (function() {
					
					var display = new $.display(this);
					//$(this).data('validator', val);
					display.init();
				}); 
			}
		}
);
$.display = function (block) {
	
	this.block = block;
	//var validator = $(this).data('validator');
	this.element = $(this.block).find('.js-element');
	this.monitor = $(this.block).find('.js-monitor');
	this.toggleDisplay =  $(this.block).find('.js-toggle-display');
	this.toggleHide =  $(this.block).find('.js-toggle-hide');
	
}
$.extend($.display, {
				prototype: {
					init: function () {
						(function (display) {
							
							display.toggleDisplay.bind('click',function(){
								
								display.toggleHide.css('display','inline');
								display.toggleDisplay.css('display','none');
								
								display.monitor.val(display.element.val()).attr('name','password');
								display.element.css('display','none').removeAttr('name');
								display.monitor.css('display','inline');
							});
							
							display.toggleHide.bind('click',function(){
								
								display.toggleHide.css('display','none');
								display.toggleDisplay.css('display','inline');
										
								display.element.val(display.monitor.val()).attr('name','password').css('display','inline');
								display.monitor.css('display','none').removeАttr('name');
							});
							
						})(this);
					}
				}
			}
);
})(jQuery);