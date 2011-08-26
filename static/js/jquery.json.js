(function($) {
$.extend(
		$.fn, {
			json : function () {
				if (!$(this).length) {return;}			
				$(this).each (function() {
					var jx = new $.jx(this);
					jx.init();
				});																		 
			}
		}
);

$.jx = function (element) {	
	
	this.element = $(element);
	this.popup = this.element.data('popup');
	this.regionList = $('<ul class="region-list"></ul>');
	
	

}

$.extend($.jx, {			

	prototype: {
		
		init: function () {
			(function (jx) {
				jx.regionList.appendTo(jx.popup.container);
				jx.element.unbind ('click.popUp');
				
				
				
				jx.element.bind('keyup.json',function(){
					if (jx.element.val() == "") {
						jx.popup.hide();
						
					}
					else { 
						
						
						
						
						$.getJSON('/place-suggest?pattern='+jx.element.val(), function(data){     
							
							
							
							jx.regionList.empty();
							$.each(data.found, function(i, found){
								
								var li = $('<li class="region-line"><a>'+found.name+'</a></li>');
								li.appendTo(jx.regionList);
								
								li.bind('click.json',function(){
									jx.element.val(found.name);
									jx.popup.hide();
									
									
									
									
								});
								
							
							
					
							});
					
						
							
							jx.popup.show();
							
					
						});
					}
		        				
					
				});
				
				
										
			})(this);
		}
	}
});
})(jQuery);