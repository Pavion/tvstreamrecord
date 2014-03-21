%include header style=curstyle, version=version 
<div id="users-contain" class="ui-widget">
<h1>Electronic Program Guide List:
<button id="grabepg"></button>
<div id="listmode" value="{{listmode}}"></div>
</h1>
<table id="table_epglist">
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