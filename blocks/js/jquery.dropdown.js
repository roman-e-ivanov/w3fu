(function($) {
$.extend(
		$.fn, {
			dropDown : function (type) {
				if (!$(this).length) {return;}			
				$(this).each (function() {
					var dropdown = new $.dropdown(this, type);
					$(this).data('dropdown', dropdown);
					dropdown.init();
				});																		 
			}
		}
);

$.dropdown = function (container, type) {	
	
	this.container = $(container);
	this.content = $(this.container).find($.dropdown.elements.content);
	this.button = $(this.container).find($.dropdown.elements.button);
	this.display = false;
	this.beforeShow = this.afterShow = this.beforeHide = this.afterHide = function(){};
	
	if (type == 'fast-login') {
		
		this.beforeShow = function() {			
		
			var validator = this.content.find('form.fast-login').data('validator');
			validator.reset(validator.login);
			validator.reset(validator.password);
		}
		
		this.afterShow = function() {
			/*this.content.find('input').get(0).focus();*/
		}
		
	}
}

$.extend($.dropdown, {			
	elements: {
		button: ".dropdown-button",
		content: "div.dropdown-content"				
	},			
	
	prototype: {
		
		init: function () {
			(function (dropdown) {
				dropdown.container.css('z-index','9000');
				dropdown.button.bind('click',(function(){ 											 
					if (!dropdown.display) { dropdown.show(); }
					else { dropdown.hide(); }
				}));
				
				$(document).bind('mouseup', (function(e) {										
					if($(e.target).parents('.' + dropdown.container.attr('class')).length == 0) { dropdown.hide(); }
				}));				
			})(this);
		},
		show: function() {
			this.beforeShow();
			this.content.css('display','block');
		//	this.container.css('z-index','9000');						
			this.display = true;
			this.afterShow();
			
		},
		hide: function() {
			this.beforeHide();
			this.content.css('display','none');
		//	this.container.css('z-index','auto');			
			this.display = false;
			this.afterHide();
		}		
	}
}
);
})(jQuery);