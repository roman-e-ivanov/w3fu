<w3fu:stylesheet version="1.0"
	xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">

	<w3fu:template name="w3fu:providers-js">
		<div class="popup">
		<a class="dropdown-button"><span>Выбрать OpenID</span></a>		
		<div class="dropdown-content">
				<w3fu:apply-templates select="document('../conf/providers.xml')/*" />
			</div>
		</div> 
	</w3fu:template>
		
	<w3fu:template match="providers/provider">
		<div >
			<w3fu:value-of select="." />
		</div>
	</w3fu:template>
	
</w3fu:stylesheet>