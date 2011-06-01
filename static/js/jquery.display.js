(function($) {
$.extend(
		$.fn, {
			display: function () {
				if (!$(this).length) {return;}			
				$(this).each (function() {
					
					var element = $(this).find('.display-element');
					var monitor = $(this).find('.display-monitor');
					var toggle =  $(this).find('.display-toggle');
					
					element.bind('keyup', function(){ monitor.val(element.val());});
					monitor.bind('keyup', function(){ element.val(monitor.val());});
					
					toggle.bind('click',function(){
						
						if (toggle.text() == 'скрыть') {
							element.blur();
							toggle.text('показать');
							element.val(monitor.val()).attr('name','password').css('display','inline');
							monitor.css('display','none').removeАttr('name');							
						}
						else {
							monitor.blur();
							toggle.text('скрыть');
							monitor.val(element.val()).attr('name','password');
							element.css('display','none').removeAttr('name');
							monitor.css('display','inline');
						}
					});					
				});																		 
			}
		}
);

})(jQuery);