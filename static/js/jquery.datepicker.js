(function($) {
$.extend(
		$.fn, {
			datePicker : function () {			
				if (!$(this).length) {return;}			
				$(this).each (function() {
					var datepicker = new $.datepicker(this);
					datepicker.init();					
				});																		 
			}
		}
);

$.datepicker = function(dropDownContainer) {
	this.dropDownContainer = $(dropDownContainer);
	this.inputDay = this.dropDownContainer.find($.datepicker.elements.inputDay);
	this.inputMonth = this.dropDownContainer.find($.datepicker.elements.inputMonth);
	this.inputYear = this.dropDownContainer.find($.datepicker.elements.inputYear);
	this.tableCalendar = this.dropDownContainer.find($.datepicker.elements.tableCalendar);
	this.calendarCells = this.tableCalendar.find('td');
	this.weeksCells = this.tableCalendar.find($.datepicker.elements.weeksCells);
	this.selectMonth = this.dropDownContainer.find($.datepicker.elements.selectMonth);
	this.selectYear = this.dropDownContainer.find($.datepicker.elements.selectYear);
	this.selectYearOptions = this.selectYear.find('option');
	this.nextMonth = this.dropDownContainer.find($.datepicker.elements.nextMonth);
	this.prevMonth = this.dropDownContainer.find($.datepicker.elements.prevMonth);
	
	this.today = new Date();
	this.begin = new Date(2010,0,1);
	this.end = new Date(2020,11,31,23,59,59,999);
	this.selected = 0;

}

$.extend($.datepicker, {			
	elements: {
		inputDay: "input.datepicker-day",
		inputMonth: "input.datepicker-month",
		inputYear: "input.datepicker-year",
		tableCalendar: "table.datepicker-calendar",
		selectMonth: "select.datepicker-control-month",
		selectYear: "select.datepicker-control-year",
		weeksCells: "th.week",
		nextMonth: ".datepicker-next",
		prevMonth: ".datepicker-prev"		
	},
	classes: {
		today: "datepicker-today",
		holiday: "datepicker-holiday",
		anotherday: "datepicker-anotherday",
		workingday: "datepicker-workingday"				
	},
	
	prototype: {
		
		init: function () {
			(function (datepicker) {
				
				datepicker.inputDay.attr('readonly','readonly');
				datepicker.inputMonth.attr('readonly','readonly');
				datepicker.inputYear.attr('readonly','readonly');
				
				datepicker.showDate(new Date());				
				
				datepicker.selectMonth.each(function(){			
					$(this).change(function(){
						datepicker.showMonth(this.selectedIndex, datepicker.selectYear[0].options[datepicker.selectYear[0].selectedIndex].text);
						datepicker.selected = new Date(datepicker.selectYear[0].options[datepicker.selectYear[0].selectedIndex].text, this.selectedIndex, 1, 12);
					});					
					$(this).keyup(function(){
						datepicker.showMonth(this.selectedIndex, datepicker.selectYear[0].options[datepicker.selectYear[0].selectedIndex].text);
						datepicker.selected = new Date(datepicker.selectYear[0].options[datepicker.selectYear[0].selectedIndex].text, this.selectedIndex, 1, 12);
					});
				});
				
				datepicker.selectYear.each(function(){
					$(this).change(function(){
						datepicker.showMonth(datepicker.selectMonth[0].selectedIndex, this.options[this.selectedIndex].text);
						datepicker.selected = new Date(this.options[this.selectedIndex].text, datepicker.selectMonth[0].selectedIndex, 1, 12);
					});
					
					$(this).keyup(function(){
						datepicker.showMonth(datepicker.selectMonth[0].selectedIndex, this.options[this.selectedIndex].text);
						datepicker.selected = new Date(this.options[this.selectedIndex].text, datepicker.selectMonth[0].selectedIndex, 1, 12);

					});
				});

				datepicker.nextMonth.each(function(){
					$(this).click(function(){datepicker.nextTime();});
				});
				
				datepicker.prevMonth.each(function(){
					$(this).click(function(){datepicker.prevTime();});
				});
				
				datepicker.tableCalendar.click(function(e){ 

					datepicker.showDate($(e.target).data('date'));
					datepicker.dropDownContainer.data('dropdown').hide();
				});				
				datepicker.selected = datepicker.today;
				datepicker.showControlDate(datepicker.today);
				datepicker.showMonth(datepicker.today.getMonth(), datepicker.today.getFullYear());
							
			})(this);
		},

		format: function(number) {if (number < 10) { return '0' + number; } return number;},
		
		showDate: function (date) {
			this.inputDay[0].value = this.format(date.getDate());
			this.inputMonth[0].value = this.format(date.getMonth() + 1);				
			this.inputYear[0].value = date.getFullYear();
		},
		showControlDate: function (date) {
			(function (datepicker) {
				datepicker.selectMonth[0].selectedIndex = date.getMonth();
				var i = 0;
				datepicker.selectYearOptions.each(function(){
					if (this.text == date.getFullYear()) {
						datepicker.selectYear[0].selectedIndex = i;
						return true;
					}
					else {i += 1;}
				});
				return false;
			})(this);
		},
		nextTime: function (){
			var d = new Date(this.selected.getFullYear(),this.selected.getMonth() + 1, 12);
			if ( d.getTime() <= this.end.getTime()) {
				this.selected = d;
				this.showControlDate(d);
				this.showMonth(d.getMonth(),d.getFullYear());				
			}
		},
		prevTime: function (){
			var d = new Date(this.selected.getFullYear(),this.selected.getMonth() - 1, 12);
			if ( d.getTime() >= this.begin.getTime()) {
				this.selected = d;
				this.showControlDate(d);
				this.showMonth(d.getMonth(),d.getFullYear());				
			}
		},
		showMonth: function (month, year) {
			
			(function (datepicker) {	
				var today = new Date(datepicker.today.getFullYear(),datepicker.today.getMonth(),datepicker.today.getDate(),12); 
				var startMonth = new Date(year, month, 1, 12);
				var dayShift = 6;
				
				if (startMonth.getDay()) {dayShift = startMonth.getDay() - 1;}
				var startDay = startMonth.getTime() -(dayShift * 86400000);
				
				var i = 0; var weekCount = 0;
				datepicker.calendarCells.each(function(){
					
					d = new Date (startDay + (i * 86400000)); $(this).data('date',d);
					$(this).removeAttr('class');
					
					if (d.getDay() == 4) {
						var startYear = new Date(d.getFullYear(), 0, 1, 12);
						$(datepicker.weeksCells[weekCount]).html(Math.floor((d.getTime() - startYear.getTime())/604800000) + 1);
						weekCount += 1;
					}						
					if (d.getMonth() != month) {
						$(this).addClass($.datepicker.classes.anotherday);
						$(this).html(d.getDate());
					}
					else { 						
						if (d.getTime() == today.getTime()) {
							$(this).addClass($.datepicker.classes.today);
						}
						else {
							if ((d.getDay() == 6) || (!d.getDay())) {
								$(this).addClass($.datepicker.classes.holiday);
							}
							else {$(this).addClass($.datepicker.classes.workingday);}
						}
						
						$(this).html(d.getDate()); 
					}
					
					i += 1;
					
				});
			})(this);
		}
	}
}
);
})(jQuery);