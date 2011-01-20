(function($) {
$.extend(
		$.fn, {
			dropDown : function () {
				if (!$(this).length) {return;}			
				$(this).each (function() {
					var dropdown = new $.dropdown(this);
					$(this).data('dropdown', dropdown);
					dropdown.init();
				});																		 
			}
		}
);

$.dropdown = function (container) {	
	this.container = $(container);
	this.content = this.container.find($.dropdown.elements.content);
	this.button = this.container.find($.dropdown.elements.button);
	this.display = false;	
}

$.extend($.dropdown, {			
	elements: {
		button: ".dropdown-button",
		content: "div.dropdown-content"				
	},			
	
	prototype: {
		
		init: function () {
			(function (dropdown) {
				
				dropdown.button.click(function(){ 							
					if (!dropdown.display) { dropdown.show(); }
					else { dropdown.hide(); }
				});
				
				$(document).mouseup(function(e) {										
					if($(e.target).parents('.' + dropdown.container.attr('class')).length == 0) { dropdown.hide(); }
				});				
			})(this);
		},
		show: function() {
			this.content.css('display','block');
			this.container.css('z-index','9000');						
			this.display = true;
		},
		hide: function() {
			this.content.css('display','none');
			this.container.css('z-index','auto');
			this.display = false;
		}		
	}
}
);
})(jQuery);