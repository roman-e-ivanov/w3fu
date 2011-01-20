<w3fu:stylesheet version="1.0"
	xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">
	
	<w3fu:output method="xml" indent="no" encoding="tttt"
		media-type="text/html" omit-xml-declaration="yes"
		doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" 
		doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" />
	
	<w3fu:include href="../icons/icon.html.xsl" />
	<w3fu:include href="../css/css.html.xsl" />
	<w3fu:include href="../js/js.html.xsl" />

	<w3fu:template name="w3fu:links">

		<w3fu:call-template name="w3fu:icon" />
		<w3fu:call-template name="w3fu:css" />
		<w3fu:call-template name="w3fu:js" />

	</w3fu:template>
	
	<w3fu:template name="w3fu:keywords">
		<w3fu:param name="keywords" select="''"/>
		<meta name="keywords">
			<w3fu:attribute name="content">
				<w3fu:value-of select="$keywords" />
			</w3fu:attribute>
        </meta>
	</w3fu:template>
	
	<w3fu:template name="w3fu:description">
		<w3fu:param name="description" select="''"/>
		<meta name="description">
			<w3fu:attribute name="content">
				<w3fu:value-of select="$description" />
			</w3fu:attribute>
        </meta>
	</w3fu:template>

</w3fu:stylesheet>