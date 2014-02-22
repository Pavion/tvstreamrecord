%include header 

<div id="users-contain" class="ui-widget">
<h1>Configuration:
<button id="submit_cfg">Submit changes</button>
</h1>
<!--<form method='POST' enctype='multipart/form-data' action='/config' name='submit_cfg_form'>-->
<!--<table id="clist">  -->

<div id="configtabs">
<ul>
<li><a href="#configtabs-1">General</a></li>
<li><a href="#configtabs-2">EPG</a></li>
<li><a href="#configtabs-3">FFMPEG support</a></li>
<li><a href="#configtabs-4">Advanced</a></li>
</ul>
<div id="configtabs-1">
<!--General configuration-->
<table width="90%">
<colgroup>
    <col width="50%">
    <col width="50%">
</colgroup>
<thead>
<tr class="ui-widget-header ">
<th>Parameter name</th>
<th>Value</th>
</tr>
</thead>
<tbody>
<tr><td>Path for your recordings</td><td><input type="text" class="text ui-widget-content ui-corner-all" id="cfg_recordpath" value="" autocomplete="off" /></td></tr>
<tr><td>File extension for the recorded stream (default='.ts')</td><td><input type="text" class="text ui-widget-content ui-corner-all" id="cfg_file_extension" value="" autocomplete="off" /></td></tr>
</tbody>
</table>

</div>
<div id="configtabs-2">
<!--EPG configuration-->
<table width="90%">
<colgroup>
    <col width="50%">
    <col width="50%">
</colgroup>
<thead>
<tr class="ui-widget-header ">
<th>Parameter name</th>
<th>Value</th>
</tr>
</thead>
<tbody>
<tr><td>Lenghten an EPG-record (delta before and after), [minutes]</td><td><input id="cfg_delta_for_epg" /></td></tr>
<tr><td>Automatic XMLTV-Import</td><td><input type="checkbox" class="switch icons" id="cfg_switch_xmltv_auto" /></td></tr>
<tr><td>Initial path for an XMLTV-Import</td><td><input type="text" class="text ui-widget-content ui-corner-all" id="cfg_xmltvinitpath" value="" autocomplete="off" /></td></tr>
<tr><td>Automatic stream scan / grab</td><td><input type="checkbox" class="switch icons" id="cfg_switch_grab_auto" /></td></tr>
<tr><td>Maximal EPG scan duration per channel, [seconds] (default '60')</td><td><input id="cfg_grab_max_duration" /></td></tr>
<tr><td>Time to perform daily EPG/XMLTV grab (hh:mm format, 24h based, default '0' for manual only)</td><td><input type="text" maxlength="5" id="cfg_grab_time" class="text ui-widget-content ui-corner-all" /></td></tr>
<tr><td>Zoom level for EPG view. Positive values for horizontal, negative for vertical view (default '1' for old style)</td><td><input id="cfg_grab_zoom" /></td></tr>
<tr><td>EPG list mode. Disable for client-side processing (more network load), enable for server-side processing (more server load)</td><td><input type="checkbox" class="switch icons" id="cfg_switch_epglist_mode" /></td></tr>
<tr><td>Delete/reset all EPG data</td><td><button id="removeepg">Delete EPG data</button></td></tr>
</tbody>
</table>
</div>
<div id="configtabs-3">
<!--FFMPEG configuration-->
<table width="90%">
<colgroup>
    <col width="50%">
    <col width="50%">
</colgroup>
<thead>
<tr class="ui-widget-header ">
<th>Parameter name</th>
<th>Value</th>
</tr>
</thead>
<tbody>
<tr><td>Stream types, which should be forwarded to ffmpeg (space separated)</td><td><input type="text" class="text ui-widget-content ui-corner-all" id="cfg_ffmpeg_types" value="" autocomplete="off" /></td></tr>
<tr><td>Full path to ffmpeg for other streams support</td><td><input type="text" class="text ui-widget-content ui-corner-all" id="cfg_ffmpeg_path" value="" autocomplete="off" /></td></tr>
<tr><td>Additional output arguments for ffmpeg (default: '-acodec copy -vcodec copy')</td><td><input type="text" class="text ui-widget-content ui-corner-all" id="cfg_ffmpeg_params" value="" autocomplete="off" /></td></tr>
</tbody>
</table>
</div>
<div id="configtabs-4">
<!--Advanced configuration-->
<table width="90%">
<colgroup>
    <col width="50%">
    <col width="50%">
</colgroup>
<thead>
<tr class="ui-widget-header ">
<th>Parameter name</th>
<th>Value</th>
</tr>
</thead>
<tbody>
<tr><td>Purge database records older than [days]</td><td><input id="cfg_purgedelta" /></td></tr>
<tr><td>Server bind address (restart needed)</td><td><input type="text" class="text ui-widget-content ui-corner-all" id="cfg_server_bind_address" value="" autocomplete="off" /></td></tr>
<tr><td>Server port (restart needed)</td><td><input type="text" class="text ui-widget-content ui-corner-all" id="cfg_server_port" value="" autocomplete="off" /></td></tr>
<tr><td>Reset the log file</td><td><button id="resetlog">Reset log</button></td></tr>
</tbody>
</table>
</div>
</div>
<!--</form>-->
</div>
<div id="dialog" title="Confirmation request">
	<p>Do you want to delete all of your EPG data?</p>
</div>
%include footer
           