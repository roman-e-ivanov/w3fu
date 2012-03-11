/* popUp JQery Plugin - w3fu
 * 
 * Плагин всплывающего слоя. Подразумевает наличие элемента управления всплытием (button),
 * и всплывающего слоя (container).
 * 
 * Пример использования: $('.f2').popUp('.container_16','class', 20, 20);
 * 
 */
(function($) {
	$.extend(
			$.fn, {
				/*
				 * Главная функция плагина
				 * parent - предок контейнера, оносительно которого отсчитываются координаты, указывается в jquery-формате
				 * filter (class/id) - способ поиска контейнера, по классу / ид
				 * x,y - смещение всплывающего слоя относительно элемента управления
				 */
				popUp : function (parent, filter, x, y) {
					if (!$(this).length) {return;}			
					$(this).each (function() {
						 // button + все входные параметры передаются в конструктор
						var popup = new $.popup(this, parent, filter, x, y);
						//эземпляр "всплывателя" сохраняем в button, для извлечения и использования в других плагинах
						$(this).data('popup', popup);
						popup.init(filter);
					});																		 
				}
			}
	);

	$.popup = function (button, parent, filter, x, y) {	
		
		//вычисляем координаты предка
		this.parentPosition = $(parent).offset();
		//элемент управления
		this.button = $(button);
		//x,y, если не заданы, то равны 0
		this.x = x || 0; this.y = y || 0;
		//если фильтр == id, то ищем контейнер по id
		if (filter == 'id') { this.container = $('#'+ $(this.button).attr('id') + 'popup'); }
		//иначе контейнер ищется по классу
		else { this.container = $('.'+ $(this.button).attr('class') + 'popup'); }
		//начальное состояние - всплывающий слой скрыт
		this.display = false;
		//функции, отрабатываемы до/после отображения/скрытия слоя - пустые
		this.beforeShow = this.afterShow = this.beforeHide = this.afterHide = function(){};
		
	}

	$.extend($.popup, {			
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
				
				var x = this.button.offset();
				this.container.css('left',x.left - this.parentPosition.left + this.x).css('top',x.top - this.parentPosition.top + this.button.height() + this.y).css('display','inline');
									
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