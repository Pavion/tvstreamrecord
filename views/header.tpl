<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
          "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <link rel="shortcut icon" href="images/favicon.ico?v=2" type="image/x-icon" /> 
    <meta charset="utf-8" />
    <title>tvstreamrecord {{version}}</title>
    <link rel="stylesheet" type="text/css" href="css/{{style}}" />
    <link rel="stylesheet" type="text/css" href="css/jquery-ui-timepicker-addon.min.css" />
    <link rel="stylesheet" type="text/css" href="css/dataTables.jqueryui.min.css"/>
    <link rel="stylesheet" type="text/css" href="css/select.jqueryui.min.css"/>
    <link rel="stylesheet" type="text/css" href="css/jqueryFileTree.css" />
    <link rel="stylesheet" type="text/css" href="css/slickswitch.css" />
    <link rel="stylesheet" type="text/css" href="css/tvstreamrecord.basic.css" type="text/css" />

    <script type="text/javascript" src="js/jquery-3.5.1.min.js"></script>
    <script type="text/javascript" src="js/jquery-ui.min.js"></script>
    <script type="text/javascript" src="js/jquery-ui-timepicker-addon.min.js"></script>
    <script type="text/javascript" src="js/jquery.slickswitch.js"></script>
    <script type="text/javascript" src="js/jquery.dataTables.min.js"></script>
    <script type="text/javascript" src="js/dataTables.jqueryui.min.js"></script>
%if not locale == 'default':
    <script type="text/javascript" src="js/i18n/jquery-ui-timepicker-{{locale}}.js"></script>	
    <script type="text/javascript" src="js/i18n/jquery.ui.datepicker-{{locale}}.js"></script>	
%end
    <script type="text/javascript" src="js/jqueryFileTree.js"></script>
    <script type="text/javascript" src="js/tvstreamrecord.basic.js?v=140"></script>
    <script type="text/javascript" src="js/preloader.js"></script>
</head><BODY>
<div id="datepicker_local" style="display: none;"></div>
<div id="timepicker_local" style="display: none;"></div>
<div id="mybody" class="ui-tabs-panel ui-widget-content ui-corner-bottom" language="{{language}}">
<div id="menus">
<div id="logo">
<a href="http://pavion.github.io/tvstreamrecord/"><img id="img_logo" alt="logo" src="images/tvstreamrecordlogo.png"></a> 
</div>
    <div id="loaderImage"></div>
<div id="tabs" class="ui-tabs ui-widget ui-widget-content ui-corner-all">
  <ul id="mainmenu" class="ui-tabs-nav ui-helper-reset ui-helper-clearfix ui-widget-header ui-corner-all">
    <li><a id="mobipic" class="ui-tabs-anchor" href="mobile"><img src="images/iphone-control-panel-px-png.png"></a></li>
    <li id="menu-0" class="ui-state-default ui-corner-top"><a class="ui-tabs-anchor" href="records">§Records§</a></li>
    <li id="menu-1" class="ui-state-default ui-corner-top"><a class="ui-tabs-anchor" href="list">§Channels§</a></li>
    <li id="menu-2" class="ui-state-default ui-corner-top"><a class="ui-tabs-anchor" href="epgchart">§EPG Chart§</a></li>
    <li id="menu-3" class="ui-state-default ui-corner-top"><a class="ui-tabs-anchor" href="epglist">§EPG List§</a></li>
    <li id="menu-4" class="ui-state-default ui-corner-top"><a class="ui-tabs-anchor" href="config">§Config§</a></li>
    <li id="menu-5" class="ui-state-default ui-corner-top"><a class="ui-tabs-anchor" href="log">§Log§</a></li>
    <li id="menu-6" class="ui-state-default ui-corner-top"><a class="ui-tabs-anchor" href="about">§About§</a></li>
%if logout:
    <li id="menu-7" class="ui-state-default ui-corner-top"><a class="ui-tabs-anchor" href="logoff">X</a></li>
%end    
  </ul>
</div>
%from datetime import datetime
%if datetime.now().month == 12:
<div style="float: right; margin: -6px -192px 0 0; z-index: 999;"><img src="images/mc.png"></div>
%end
</div>
