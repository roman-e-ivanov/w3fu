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
	
	this.regionItems = 0;
	this.itemIndex = -1;
	this.itemsLength = 0;
	
}

$.extend($.jx, {			

	prototype: {
		
		init: function () {
			(function (jx) {
				jx.regionList.appendTo(jx.popup.container);
				jx.element.unbind ('click.popUp');
				
				jx.element.bind ('click.json',function(){
					if (jx.element.val() != "") {jx.getJson();}
				});

				jx.element.bind('keydown.json',function(e){if (e.keyCode == 9) {jx.popup.hide(); return;}});
				jx.element.bind('keyup.json',function(e){
										
					if (e.keyCode == 40 || e.keyCode == 38 ) {
						
						if (jx.itemsLength) {
							
							if (e.keyCode == 40) { jx.itemIndex += 1; }
							else {jx.itemIndex -= 1;}
							
							if (jx.itemIndex > jx.itemsLength - 1) {jx.itemIndex = 0;}
							if (jx.itemIndex < 0) {jx.itemIndex = jx.itemsLength - 1;}
							
							
							var g = jx.regionItems.get(jx.itemIndex);
							jx.regionItems.css('border','none');
							$(g).css('border','1px solid black');
							jx.element.val($(g).text());
						}
					return;
					}
										
					jx.getJson();
												
				});
																		
			})(this);
		},
		
		getJson: function() {
			(function (jx) {
			if (jx.element.val() == "") {jx.popup.hide();}
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
			
					jx.show();					
			
				});
			}
			})(this);
		},
		
		show: function() {
			
			this.regionItems = this.regionList.find('li');
			this.itemIndex = -1;
			this.itemsLength = this.regionItems.length;
			this.popup.show();
		}		
	}
});
})(jQuery);