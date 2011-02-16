<w3fu:stylesheet version="1.0" xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">
	
	<w3fu:template name="w3fu:user-not-login">
	
	<w3fu:if test="not(*/user)">	
	
		<div class="popup-user-login">
		<a class="dropdown-button"><span>Войти</span></a>		
		<div class="dropdown-content">
			<form method="post" action="/login" class="validate">
				<p>Логин:<input type="text" name="login" maxlength="32" class="val-required val-login" /></p> 
				<p>Пароль:<input type="text" name="password" maxlength="32" class="val-required val-password" /></p>
				<p><input type="submit" class="button" value="ОК" /></p>
			</form>
			<w3fu:apply-templates select="document('../conf/providers.xml')/*" />
			<iframe src="http://loginza.ru/api/widget?overlay=loginza&amp;token_url=http://w3fu.com" style="width:359px;height:300px;" scrolling="no" frameborder="no" />
			<a href="https://loginza.ru/api/widget?token_url=[RETURN_URL]" class="loginza">

    <img src="http://loginza.ru/img/providers/yandex.png" alt="Yandex" title="Yandex" />

    <img src="http://loginza.ru/img/providers/google.png" alt="Google" title="Google Accounts" />

    <img src="http://loginza.ru/img/providers/vkontakte.png" alt="Вконтакте" title="Вконтакте" />

    <img src="http://loginza.ru/img/providers/mailru.png" alt="Mail.ru" title="Mail.ru" />

    <img src="http://loginza.ru/img/providers/twitter.png" alt="Twitter" title="Twitter" />

    <img src="http://loginza.ru/img/providers/loginza.png" alt="Loginza" title="Loginza" />

    <img src="http://loginza.ru/img/providers/myopenid.png" alt="MyOpenID" title="MyOpenID" />

    <img src="http://loginza.ru/img/providers/openid.png" alt="OpenID" title="OpenID" />

    <img src="http://loginza.ru/img/providers/webmoney.png" alt="WebMoney" title="WebMoney" />

</a>
			</div>
		</div>
		
	</w3fu:if>
	</w3fu:template> 
	
	<w3fu:template name="w3fu:user-login">	
	
	<w3fu:if test="*/user">
		
			<w3fu:value-of select="*/user/login" />
			<form method="post" action="/login" class="exit-form">				
				<input type="hidden" name="method" value="delete" /> 
				<input type="submit" class="exit-button" value="Выход" />
			</form>
	
	</w3fu:if>
	
	</w3fu:template>
	
	<w3fu:template match="providers/provider">
		<div >
			<w3fu:value-of select="." />
		</div>
	</w3fu:template>

</w3fu:stylesheet>