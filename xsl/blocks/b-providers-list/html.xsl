<w3fu:stylesheet version="1.0"
	xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">
	
	<w3fu:template name="w3fu:b-providers-list">
		<div class="b-providers-list">
			<ul class="b-providers-list__list">
				<w3fu:for-each	select="*/providers/i"> 
					<li class="b-providers-list__line">
						<a class="i-link b-providers-list__link">
							<w3fu:attribute name="href">
								<w3fu:value-of select="nav/@main" />
							</w3fu:attribute>
							<w3fu:value-of select="doc/@name" />
						</a>
					</li>
				</w3fu:for-each>
			</ul>
		</div>
	</w3fu:template>
</w3fu:stylesheet>