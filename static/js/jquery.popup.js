(function($) {
	$.extend(
			$.fn, {
				popUp : function (filter, x, y) {
					if (!$(this).length) {return;}			
					$(this).each (function() {
						var popup = new $.popup(this, filter, x, y);
						$(this).data('popup', popup);
						popup.init(filter);
					});																		 
				}
			}
	);

	$.popup = function (button, filter, x, y) {	
		
		this.button = $(button);
		this.x = x || 0; this.y = y || 0;
		
		if (filter == 'id') { this.container = $('#'+ $(this.button).attr('id') + 'popup'); }
		else { this.container = $('.'+ $(this.button).attr('class') + 'popup'); }
		
		this.display = false;
		this.beforeShow = this.afterShow = this.beforeHide = this.afterHide = function(){};
		
	}

	$.extend($.popup, {			
	/*	elements: {
			button: ".dropdown-button",
			container: "div.dropdown-container"				
		},			
		*/
		prototype: {
			
			init: function (filter) {
				(function (popup) {
					popup.container.css('z-index','9000');
					
					popup.button.bind('click.popUp',(function(){ 											 
						if (!popup.display) { popup.show(); }
						else { popup.hide(); }
					}));
					
					if (filter == 'id') {
						$(document).bind('mouseup', (function(e) {										
							
							var f = $(e.target).is('#'+ popup.button.attr('id')); 
							if (!f) {
								if($(e.target).parents('#' + popup.container.attr('id')).length == 0) { popup.hide(); }
							}
						}));
					}
					else {
						$(document).bind('mouseup', (function(e) {										
							
							var f = $(e.target).is('.'+ popup.button.attr('class')); 
							if (!f) {
								if($(e.target).parents('.' + popup.container.attr('class')).length == 0) { popup.hide(); }
							}
						}));
					}
									
				})(this);
			},
			show: function() {
				this.beforeShow();
				
				var body = $('.container_16').offset(); var x = this.button.offset();
				this.container.css('left',x.left - body.left + this.x).css('top',x.top - body.top + this.button.height() + this.y).css('display','inline');
									
				this.display = true;
				this.afterShow();
				
			},
			hide: function() {
				this.beforeHide();
				this.container.css('display','none');
					
				this.display = false;
				this.afterHide();
			}		
		}
	});
	})(jQuery);