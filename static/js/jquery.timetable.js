(function($) {
$.extend(
		$.fn, {
			timeTable: function () {
				if (!$(this).length) {return;}			
				$(this).each (function() {
				
					var dates = $(this).find('.dates')
					
					for (i = 0; i < 7; i++) {
						dates.after('<tr><th>'+i+'</th><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr>');
						
					}
				/*	
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
					*/
				});																		 
			}
		}
);

})(jQuery);