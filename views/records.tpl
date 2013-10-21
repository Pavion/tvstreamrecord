%include header 
<div id="dialog-form" title="Create new record">
<p class="validateTips"></p>
<form>
<fieldset>
<input type="hidden" maxlength="5" id="prev" value=""/> 
<label for="channel">Name</label>
<input type="text" maxlength="255" id="recname" class="text ui-widget-content ui-corner-all" name="recname" value=""/> 
<label for="channel">Channel</label>
<select name='channel' id="channel" class="text ui-widget-content ui-corner-all">
%for row in rows2:
    <option value='{{row[0]}}'>{{row[1]}}</option>
%end    
</select>
<input type="checkbox" class="switch icons" id="switch00" checked="checked" />  
<label for="name">Start date</label>
<input type="text" maxlength="10" id="datepicker" class="text ui-widget-content ui-corner-all" name="name" value=""/> 
<label for="email">Start/end time</label>
<input type="text" maxlength="5" name="email" id="timepicker_inline_div1" class="text ui-widget-content ui-corner-all" />
<input type="text" maxlength="5" name="email" id="timepicker_inline_div2" class="text ui-widget-content ui-corner-all" />
<label for="recurr">Recurrent records</label>
<div id="weekday">
<input type="checkbox" id="wday0" /><label id="wwd0" for="wday0">Mo</label>
<input type="checkbox" id="wday1" /><label id="wwd1" for="wday1">Tu</label>
<input type="checkbox" id="wday2" /><label id="wwd2" for="wday2">We</label>
<input type="checkbox" id="wday3" /><label id="wwd3" for="wday3">Th</label>
<input type="checkbox" id="wday4" /><label id="wwd4" for="wday4">Fr</label>
<input type="checkbox" id="wday5" /><label id="wwd5" for="wday5">Sa</label>
<input type="checkbox" id="wday6" /><label id="wwd6" for="wday6">So</label>
</div>
<!-- <input type="text" maxlength="3" id="recurrinp" class="text ui-widget-content ui-corner-all" name="recurrinp" value="0"/>--> 
</fieldset>
</form>
</div>
<div id="users-contain" class="ui-widget">
<h1>Records:
<button id="create-user">Create new record</button>
<button id="purge-records">Purge old records</button></h1>
<table id="recordlist"><!--<table id="clist1"><table id="users" class="ui-widget ui-widget-content">-->
<thead>
<tr class="ui-widget-header ">
<th class="rname">Record name</th>
<th class="rchan">Channel</th>
<th class="rat">at</th>
<th class="rtill">till</th>
<th class="rrecu">Recurrent</th>
<th class="rcontrols">control</th>
<th class="rcontrols">c1</th>
<th class="rcontrols">c2</th>
<th class="rcontrols">c3</th>
<th class="rcontrols">c4</th>
</tr>
</thead>
<tbody>
</tbody>
</table>
</div>
    
<div id="dialog" title="Record removal">
	<p>Shall I delete this record?</p>
</div>
<div id="confirm01" title="Purging records">
	<p>All old records will be deleted! Are you sure?</p>
</div>
%include footer
           
