<w3fu:stylesheet version="1.0"
	xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">
	
	<w3fu:template name="w3fu:b-development-menu">

		<div class="b-development-menu">
			<ul class="b-development-menu__list">
				<w3fu:for-each	select="document('b-development-menu.xml')/menu/item"> 
					<li class="b-development-menu__line">
						<a class="b-development-menu__link">
							<w3fu:attribute name="href">
								<w3fu:value-of select="." />
							</w3fu:attribute>
							<w3fu:value-of select="." />
						</a>
					</li>
				</w3fu:for-each>
			</ul>
			
			<ul class="b-development-menu__list">	
				<w3fu:for-each	select="document('b-development-menu.xml')/menu/item"> 
					<li class="b-development-menu__line">
						<a class="b-development-menu__link">
							<w3fu:attribute name="href">
								<w3fu:value-of select="." /><w3fu:text>?no-xslt</w3fu:text>
							</w3fu:attribute>
							<w3fu:value-of select="." /><w3fu:text>?no-xslt</w3fu:text>
						</a>
					</li>
				</w3fu:for-each>  
			</ul>
		</div>
	</w3fu:template>
</w3fu:stylesheet>