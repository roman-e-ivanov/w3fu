$(document).ready(function(){
	
	$('<script type="text/javascript" src="/s/js/jquery.cookie.js" />').appendTo($('head'));
	
	$('.b-debug-noxslt__enable').bind('click', (function() {										
		$.cookie('no-xslt', '1', { expires: 7 });
		return false;
	}));
	
	$('.b-debug-noxslt__disable').bind('click', (function() {										
		$.cookie('no-xslt', null);
		return false;
	}));
	
	
/*	
    // получить cookie
    $('#getCookies').click(function() {
        alert($.cookie(COOKIE_NAME));
        return false;
     });

    
*/		
});