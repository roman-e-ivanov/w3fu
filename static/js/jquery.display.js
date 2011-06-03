(function($) {
$.extend(
		$.fn, {
			display: function () {
				if (!$(this).length) {return;}			
				$(this).each (function() {
					
					var validator = $(this).data('validator');
					var element = $(this).find('.display-element');
					var monitor = $(this).find('.display-monitor');
					var toggleDisplay =  $(this).find('.toggle-display');
					var toggleHide =  $(this).find('.toggle-hide');
					
					element.bind('keyup', function(){ monitor.val(element.val());});
					monitor.bind('keyup', function(){ element.val(monitor.val());});
					
					toggleDisplay.bind('click',function(){
						
						toggleHide.css('display','inline');
						toggleDisplay.css('display','none');
						
						monitor.val(element.val()).attr('name','password');
						element.css('display','none').removeAttr('name');
						monitor.css('display','inline');
						validator.validatePassword(monitor);
					});
					
					toggleHide.bind('click',function(){
						
						validator.validatePassword(element);
						
						toggleHide.css('display','none');
						toggleDisplay.css('display','inline');
						
						element.val(monitor.val()).attr('name','password').css('display','inline');
						monitor.css('display','none').removeАttr('name');						
					});
				});																		 
			}
		}
);

})(jQuery);