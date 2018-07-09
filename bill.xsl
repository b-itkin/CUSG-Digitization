<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" 
xmlns:xsl="http://www3.org/1999/XSL/Transform">

<xsl:template match="/billStatus/bill/">
<html>
<head>
  <title><xsl:value-of select="canonicalname"/></title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <style>
  body {
    background-color: rgba(201, 76, 76,.4);
  }
  </style>
</head>

<body>
<div class="container" class="{{billNum}}">
<div class="row">
<div class="col-xs-12">
<h1 id="title"><xsl:value-of select="canonicalname"/></h1>
</div>
</div>
<div class="row">
<div class="col-xs-6" class="billinfo">
<p><h3>Bill Text</h3></p>
<p class="billtext"><xsl:value-of select="billText"/></p>
</div>
<div class="col-xs-6" class="billinfo">
<h2 text-align="center">Bill History and Summary</h2>
<p><h3>History</h3></p><div class="billhistory"><xsl:value-of select="summaries/history"/></div>
<p><h3>Summary</h3></p><div class="billsummary"><xsl:value-of select="summaries/summary"/></div>
</div>
</div>
<hr>
<div class="row">
<div class="col-xs-12" class="billinfo">
<p><h2>Misc. Bill Info</h2>
<p> Introduced Date: <span text-align="right" class="introduceddate"> <xsl:value-of select="introducedDate"/></span></p>
<p>Legislation number: {{billNum}}</p>
<br>
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
