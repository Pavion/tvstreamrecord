%include header 

<div id="users-contain" class="ui-widget">
<h1>Configuration:
<button id="submit_cfg">Submit changes</button>
<button id="removeepg">Remove all EPG data</button>
<button id="resetlog">Reset log</button>
</h1>
<form method='POST' enctype='multipart/form-data' action='/config' name='submit_cfg_form'>
<!--<table id="clist">  -->
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
%for row in rows:
<tr><td>{{row[1]}}</td><td><input type="text" class="text ui-widget-content ui-corner-all" id="{{row[0]}}" name="{{row[0]}}" value="{{row[2]}}" autocomplete="off" /></tr>
%end
</tbody>
</table>
</form>
</div>
<div id="dialog" title="Confirmation request">
	<p>Do you want to delete all of your EPG data?</p>
</div>
%include footer
           