(function($) {
$.extend(
		$.fn, {
			display: function () {
				if (!$(this).length) {return;}			
				$(this).each (function() {
					
					var element = $(this).find('.display-element');
					var monitor = $(this).find('.display-monitor');
					var toggle =  $(this).find('.display-toggle');
										
					element.bind('keyup',function(){
						monitor.text($(this).attr('value'));
					});
					
					element.bind('blur',function(){
						monitor.find('span.password-nodisplay').text($(this).attr('value'));
					});
					
					toggle.bind('click',function(){
						monitor.toggleClass('nodisplay');
						monitor.toggleClass('display');
						
						if (toggle.text() == 'скрыть') {toggle.text('показать');}
						else {toggle.text('скрыть');}
					});
					
				});																		 
			}
		}
);

})(jQuery);