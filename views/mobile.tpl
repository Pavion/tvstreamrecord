<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>tvstreamrecord Mobile</title>
    <link rel="shortcut icon" href="images/favicon.ico?v=3" type="image/x-icon" /> 
    <link rel="apple-touch-icon" href="images/apple-touch-icon.png">
	
    <script src="js/jquery-3.5.1.min.js"></script>
	<script src="js/jquery.mobile-1.4.5.min.js"></script>

    <script type="text/javascript" src="js/jquery.mousewheel.min.js"></script>
    <script type="text/javascript" src="js/jqm-datebox.core.min.js"></script>
    <script type="text/javascript" src="js/jqm-datebox.mode.flipbox.min.js"></script>
<!--    <script type="text/javascript" src="js/jqm-datebox.mode.durationflipbox.min.js"></script>-->
	<script type="text/javascript" src="js/tvstreamrecord.mobile.js"></script>

	<link rel="stylesheet" type="text/css" href="css/jquery.mobile-1.4.3.min.css" />
    <link rel="stylesheet" type="text/css" href="css/jqm-datebox.min.css" />
	<link rel="stylesheet" type="text/css" href="css/tvstreamrecord.mobile.css" />
    
</head>
<body>
    <div id="delta_before_epg" delta="{{deltab}}"></div>
    <div id="delta_after_epg" delta="{{deltaa}}"></div>
    <data id="locale" loc="{{locale}}"></data>
    <!-- Main page -->
    <div data-role="page" id="hdr" class="tsr-mobile jqm-home">
        
        <!-- Main header -->
        <div data-role="header" class="jqm-header" id="header1">
        <a href="http://pavion.github.io/tvstreamrecord/" data-role="none" id="logo"><h2><img src="images/tvstreamrecordlogo.png" alt="tvstreamrecord Mobile"></h2></a>
%from datetime import datetime
%if datetime.now().month == 12:
<div style="margin: -60px 0 0 150px; z-index: 999;"><img src="images/mc.png"></div>
%end
            <a href="/records" rel="external" class="ui-btn ui-btn-icon-notext ui-corner-all ui-icon-back ui-nodisc-icon ui-alt-icon ui-btn-left">Back</a>
            <a href="#" id="btn_add" class="ui-btn ui-btn-icon-notext ui-corner-all ui-icon-plus ui-nodisc-icon ui-alt-icon ui-btn-right">Add</a>
        </div>

        <!-- Main content -->
        <div role="main" class="ui-content jqm-content">
            <h1>§Records§</h1>

            <table data-role="table" data-mode="reflow" class="rtable-breakpoint" id="rectable" recurr="§none§">
             <thead>
               <tr>
                 <th>§Record name§:</th>
                 <th>§Channel§:</th>
                 <th>§at§:</th>
                 <th>§till§:</th>
                 <th>§Recurrent§:</th>
                 <th id="tcntrl">§Controls§:</th>
               </tr>
             </thead>
             <tbody id="recbody">
               </tbody>
           </table>
        </div>
       
        <!-- Main footer -->    
        <div data-role="footer" data-position="fixed" data-tap-toggle="false" class="jqm-footer">
            <p>tvstreamrecord Mobile<span class="jqm-version"></span></p>
            <p>Powered by <a href="http://jquery.com">jQuery</a> and <a href="http://jquerymobile.com">jQuery Mobile</a></p>
        </div>
        
    </div>

    <!-- Channel selection -->
    <div data-role="page" id="channel" class="tsr-mobile jqm-home">
        <h6>§Channel§</h6>
        <div data-role="collapsibleset" data-content-theme="a" data-iconpos="right" id="set"></div>        
        <a href="#" data-role="button" id="btn_cancel">§Cancel§</a> 
	</div>

    <!-- Day selection -->
    <div data-role="page" id="day" class="tsr-mobile jqm-home">
        <h6>§Start date§</h6>
        <div><div><input type="text" autocomplete="off" data-role="datebox" data-options='{"mode":"flipbox","useInline":true,"hideInput":true,"enablePopup":true,"popupPosition":false,"useSetButton":false,"useHeader":false,"calHighToday":false}' id="datebox1"></div></div>
        <a href="#" data-role="button" id="btn_day_ok">§Next§</a> 
        <a href="#" data-role="button" id="btn_cancel">§Cancel§</a> 
	</div>
    
    <!-- EPG selection -->
    <div data-role="page" id="epg" class="tsr-mobile jqm-home">
        <h6>EPG</h6>
        <ul data-role='listview' id='epglist' skip="§Skip§"></ul>
<!--        <a href="#" data-role="button" id="btn_epg_ok">§Next§</a> -->
        <a href="#" data-role="button" id="btn_cancel">§Cancel§</a> 
	</div>
    
    <!-- Time selection -->
    <div data-role="page" id="time" class="tsr-mobile jqm-home">    	    
        <h6>§Start time§</h6>
        <div><div><input type="text" autocomplete="off" data-role="datebox" data-options='{"mode":"timeflipbox","useInline":true,"hideInput":true,"useSetButton":false,"useHeader":true}' id="timebox_v"  class="tmp_timebox"></div></div>
        <h6>§End time§</h6>
        <div><div><input type="text" autocomplete="off" data-role="datebox" data-options='{"mode":"timeflipbox","useInline":true,"hideInput":true,"useSetButton":false,"useHeader":true}' id="timebox_b"  class="tmp_timebox"></div></div>
        <a href="#" data-role="button" id="btn_time_ok">§Next§</a> 
        <a href="#" data-role="button" id="btn_cancel">§Cancel§</a> 
	</div>

    <!-- Record name selection -->
    <div data-role="page" id="rname" class="tsr-mobile jqm-home">    	    
        <h6>§Recurrent§</h6>
        <fieldset data-role="controlgroup" data-type="horizontal" id="recurr" data-mini="true">
            <input type="checkbox" id="wday0" /><label id="wwd0" for="wday0"></label>
            <input type="checkbox" id="wday1" /><label id="wwd1" for="wday1"></label>
            <input type="checkbox" id="wday2" /><label id="wwd2" for="wday2"></label>
            <input type="checkbox" id="wday3" /><label id="wwd3" for="wday3"></label>
            <input type="checkbox" id="wday4" /><label id="wwd4" for="wday4"></label>
            <input type="checkbox" id="wday5" /><label id="wwd5" for="wday5"></label>
            <input type="checkbox" id="wday6" /><label id="wwd6" for="wday6"></label>
        </fieldset>
        <h6>§Record name§</h6>
        <input type="text" id="recname" value="" autocomplete="off"/>
        <a href="#" data-role="button" id="btn_rname_ok">§Next§</a> 
        <a href="#" data-role="button" id="btn_cancel">§Cancel§</a> 
	</div>
    
    <!-- Deletion dialog -->
    <a id='lnkDialog' href="#dialog_del" data-rel="dialog" data-transition="pop" style='display:none;'></a>
    <div data-role="page" class="tsr-mobile jqm-home" id="dialog_del">
        <div data-role="header">
			<h1>§Delete§</h1>
		</div>
		<div role="main" class="ui-corner-bottom ui-content ui-body-c" data-role="content">
			<h7>§Shall I delete this record?§</h7>
			<a class="ui-btn ui-shadow ui-btn-corner-all" data-wrapperels="span" data-iconshadow="true" data-shadow="true" data-corners="true" href="#" data-role="button" data-rel="back" id="dia_del"><span class="ui-btn-inner ui-btn-corner-all"><span class="ui-btn-text">§Delete§</span></span></a>       
			<a class="ui-btn ui-shadow ui-btn-corner-all" data-wrapperels="span" data-iconshadow="true" data-shadow="true" data-corners="true" href="#" data-role="button" data-rel="back" id="btn_cancel"><span class="ui-btn-inner ui-btn-corner-all"><span class="ui-btn-text">§Cancel§</span></span></a>    
		</div>
	</div>

</body>
</html>
