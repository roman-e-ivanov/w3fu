(function($) {
$.extend(
		$.fn, {
			display: function (button, display) {
				if (!$(this).length) {return;}			
				$(this).each (function() {
					
					$(this).bind('keyup',function(){
						display.text($(this).attr('value'));
					});
					
					$(this).bind('blur',function(){
						display.text($(this).attr('value'));
					});
					
					button.bind('click',function(){
						display.toggleClass('password-nodisplay');
						display.toggleClass('password-display');
						
						if (button.text() == 'скрыть') {button.text('показать');}
						else {button.text('скрыть');}
					});
					
				});																		 
			}
		}
);

})(jQuery);