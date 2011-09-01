$(document).ready(function(){
	$('<script type="text/javascript" src="/s/js/jquery.valform.js" /><script type="text/javascript" src="/s/js/jquery.dropdown.js" /><script type="text/javascript" src="/s/js/jquery.datepicker.js" /><script type="text/javascript" src="/s/js/jquery.display.js" /><script type="text/javascript" src="/s/js/jquery.timetable.js" /><script type="text/javascript" src="/s/js/jquery.json.js" />').appendTo($('head'));
	
	/*login & reg forms*/
	$("form.login").valForm('default');	
	$("form.login").display();
	$("form.login").find(".toggle-display").css('display','inline');

	/*fast login form*/
	$("form.fast-login").valForm('default');	
	$("div.fast-login").dropDown('fast-login');
	$("div.fast-login").find("a").css('display','none');
	$("div.fast-login").find("span.dropdown-button").css('display','inline');
	
	/*firm create form*/
	$("form.firm-create").valForm('default');
	$('.f2').popUp('class');
	$('.f3').popUp('class');
	$("div.fast-firm").find("span.dropdown-button").toggleClass('nodisplay');
	$("div.fast-firm").find("span.dropdown-button").toggleClass('display');
	$("div.fast-firm").find("a").toggleClass('nodisplay');
	$("div.fast-firm").find("a").toggleClass('display');
	
	/*region select form*/
	$('#f4').popUp('id',0,20);
	$('#f4').json();
	
	
	
	$("div.popup1").dropDown('date');
	$("div.popup1").datePicker();
	
	
	
	$("table.timetable").timeTable();
/*	$("div.popup2").dropDown();
	$("div.popup2").datePicker();
*/
	

/*
	var p = {
			type:'DELETE',
			url:'test.json'
	};
	
	$("#f4").bind('click', (function(){
		$.getJSON('/place-sugg7st?pattern=са', function(data){     
				
				var s = "";
			$.each(data.found, function(i, found){
				
				s = s + found.name + '_';
			
			});
			
			
			alert(s);
			
        })
        
        .error(function() { alert("error"); })
        
		
		alert(9);
	//$.ajax(p);
	}));
*/	
	
	  	
});
//----------------------------------------------------------------------------
function onLoad() {
	
	window.document.write(navigator.appName +" "+navigator.appVersion);
	
}
//----------------------------------------------------------------------------