$(document).ready(function(){
	
	$("form.fast-login").valForm('fast-login');	
	$("div.fast-login").dropDown('fast-login');
	$("input:password").display($(".password-toggle"), $("span.password-nodisplay"));
	
/*	$("div.popup1").dropDown();
	$("div.popup1").datePicker();
	$("div.popup2").dropDown();
	$("div.popup2").datePicker();
*/
	var d = new Date(2010,1,29);
	
//	alert(d.getDate() +'/'+ d.getMonth() +'/'+ d.getFullYear());
	
	//alert ($("select.datepicker-month").selectedIndex);
	var p = {
			type:'DELETE',
			url:'test.json'
	};
	
	$("input:button.b-ajax").click(function(){
		/*$.getJSON('test.json', function(data){     
			$.each(data, function(index, entry){
				m += entry;
			});
			alert(data['data1']);
			
        });  */         
	$.ajax(p);
	});
	  	
});
//----------------------------------------------------------------------------
function onLoad() {
	
	window.document.write(navigator.appName +" "+navigator.appVersion);
	
}
//----------------------------------------------------------------------------