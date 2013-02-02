%# coding=UTF-8
%include header 

<div id="users-contain" class="ui-widget">
<form method='POST' enctype='multipart/form-data' action='/epg' name='daychooser'>
<h1><div id="float">Current date:</div>
<input type="text" maxlength="10" id="datepicker3" class="text ui-widget-content ui-corner-all" name="datepicker3" value="{{curr}}"/> 
<button id="getepg">Load EPG information</button></h1>
</form>
%for rows in rowss:
%if rows[0][0] == -1:
<ol id="selectabletitle">
%else:
<h1><b>{{rows[0][7]}}</b></h1>
<ol id="selectable">
%end
%for row in rows:
<li class="ui-state-default" id="event" x="{{row[1]}}" width="{{row[2]}}" cid="{{row[0]}}" rid="{{row[6]}}" fulltext="{{row[5]}}" title="{{row[4]}}">{{row[3]}}</li>
%end
</ol>
%end
</div>

<div id="record_from_epg" title="Detail view">
<div id="dialog_content"></div></div>
<form method='POST' enctype='multipart/form-data' action='/createepg' name='returnform'>
<input type="text" style="display: none;" name="ret" id="ret" value="X"/>
</form>

%include footer