$(document).ready(function(){
	$('<script type="text/javascript" src="/s/js/jquery.valform.js" />').appendTo($('head'));
	$('<script type="text/javascript" src="/s/js/jquery.dropdown.js" />').appendTo($('head'));
	$('<script type="text/javascript" src="/s/js/jquery.popup.js" />').appendTo($('head'));
	$('<script type="text/javascript" src="/s/js/jquery.datepicker.js" />').appendTo($('head'));
	$('<script type="text/javascript" src="/s/js/jquery.display.js" />').appendTo($('head'));
	$('<script type="text/javascript" src="/s/js/jquery.timetable.js" />').appendTo($('head'));
	$('<script type="text/javascript" src="/s/js/jquery.json.js" />').appendTo($('head'));
	$('<script type="text/javascript" src="/s/js/jquery.cookie.js" />').appendTo($('head'));
	
	/*login & reg forms*/
//	$("form.login").valForm('default');	
	$("form.login").display();
	$("form.login").find(".toggle-display").css('display','inline');

	/*fast login form*/
	$("form.fast-login").valForm('default');	
	$("div.fast-login").dropDown('fast-login');
	$("div.fast-login").find("a").css('display','none');
	$("div.fast-login").find("span.dropdown-button").css('display','inline');
	
	/*firm create form*/
	$("form.firm-create").valForm('default');
	$('.f2').popUp('.container_16','class', 20, 20);
	$('.f3').popUp('.container_16','class', 20, 20);
	
/*	
 *  ХЗ ,что такое
 	$("div.fast-firm").find("span.dropdown-button").toggleClass('nodisplay');
	$("div.fast-firm").find("span.dropdown-button").toggleClass('display');
	$("div.fast-firm").find("a").toggleClass('nodisplay');
	$("div.fast-firm").find("a").toggleClass('display');
/*	
	/*region select form*/
	$('#f4').popUp('.container_16','id', 20, 20);
	$('#f4').json();
	
	
	
	$("div.popup1").dropDown('date');
	$("div.popup1").datePicker();
	
	
	
	$("table.timetable").timeTable();
/*	$("div.popup2").dropDown();
	$("div.popup2").datePicker();
*/
		  	
});
//----------------------------------------------------------------------------
function onLoad() {
	

	
}
//----------------------------------------------------------------------------