(function($) {
$.extend(
		$.fn, {
			display: function () {
				if (!$(this).length) {return;}			
				$(this).each (function() {
					
					var element = $(this).find('.display-element');
					var monitor = $(this).find('.display-monitor');
					var toggle =  $(this).find('.display-toggle');
					
					element.bind('keyup',function(){monitor.text($(this).attr('value'));});
					
					element.bind('blur',function(){monitor.text($(this).attr('value'));});
					
					toggle.bind('click',function(){
						
						if (toggle.text() == '(скрыть)') {
							toggle.text('(показать)');
							element.val(monitor.val()).css('display','block').attr('name','password').keyup();
							monitor.css('display','none').removeАttr('name');
						}
						else {
							toggle.text('(скрыть)');
							element.css('display','none').removeAttr('name');
							monitor.val(element.val()).css('display','block').attr('name','password').keyup();
						}
					});					
				});																		 
			}
		}
);

})(jQuery);