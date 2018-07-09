<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" 
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
<html>
<head>
  <title><xsl:value-of select="billStatus/bill/canonicalname"/></title>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"/>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <style>
  body {
    background-color: rgba(201, 76, 76,.4);
  }
  </style>
</head>

<body>
<div class="container">
<div class="row">
<div class="col-xs-12">
<h1 id="title"><xsl:value-of select="billStatus/bill/canonicalname"/></h1>
</div>
</div>
<div class="row">
<div class="col-xs-6">
<p><h3>Bill Text</h3></p>
<p class="billtext"><xsl:value-of select="billStatus/bill/billText"/></p>
</div>
<div class="col-xs-6">
<h2 text-align="center">Bill History and Summary</h2>
<p><h3>History</h3></p><div><xsl:value-of select="billStatus/bill/summaries/history"/></div>
<p><h3>Summary</h3></p><div><xsl:value-of select="billStatus/bill/summaries/summary"/></div>
</div>
</div>
<hr/>
<div class="row">
<div class="col-xs-12">
<p><h2>Misc. Bill Info</h2></p>
<p> Introduced Date: <span text-align="right" class="introduceddate"> <xsl:value-of select="billStatus/bill/introducedDate"/></span></p>
<p>Legislation number: <xsl:value-of select="billStatus/bill/canonicalname"/></p>
<p><a>
<xsl:attribute name="href">
<xsl:value-of select="billStatus/bill/canonicalname"></xsl:value-of>
<xsl:text>.pdf</xsl:text>
</xsl:attribute>
PDF link
</a></p>
<br></br>
<h3>Sponsors and Authors</h3>
<div class="sponsors"></div>
<h3>Actions</h3>
<div class="actions"></div>
</div>
</div>

</div>



</body>
</html>
</xsl:template>
</xsl:stylesheet>
