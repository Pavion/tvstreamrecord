%include header 
<div id="users-contain" class="ui-widget">
<h1>
<button id="getepg">Load XMLTV information</button>
%if grabstate[0] == False:
<button id="grabepgstart">Grab EPG from {{grabstate[2]}} streams</button>
%else:
<button id="grabepgstop">Stop grabbing EPG (State: {{grabstate[1]}}/{{grabstate[2]}})</button>
%end
</h1>
<table id="epglist">
<thead>
<tr class="ui-widget-header">
<th class="echan">Channel</th>
<th class="etit">Title</th>
<th class="edesc">Description</th>
<th class="estart">Start time</th>
<th class="estop">End time</th>
<th class="econtrol">Record</th>
</tr>
</thead>
<tbody>
</tbody>
</table>
</div>
<div id="record_from_epg" title="Detail view">
<div id="dialog_content"></div></div>
<form method='POST' enctype='multipart/form-data' action='/createepg' name='returnform'>
<input type="text" style="display: none;" name="ret" id="ret" value="X"/>
</form>
%include footer