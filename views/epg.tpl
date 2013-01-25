%# coding=UTF-8
%include header 

<form method='POST' enctype='multipart/form-data' action='/epg' name='daychooser'>
<div id="users-contain" class="ui-widget">
<h1><div id="float">Current date:</div>
<input type="text" maxlength="10" id="datepicker1" class="text ui-widget-content ui-corner-all" name="datepicker1" value="{{curr}}"/> 
<button id="refreshme">Refresh</button></h1>
</form>
%for rows in rowss:
%if rows[0][0] == -1:
<ol id="selectabletitle">
%else:
<ol id="selectable">
%end
%for row in rows:
<li class="ui-state-default" id="event" x="{{row[1]}}" width="{{row[2]}}" cid="{{row[0]}}" rid="{{row[6]}}" fulltext="{{row[5]}}" title="{{row[4]}}">{{row[3]}}</li>
%end
</ol>
%end
</div>

<div id="record_from_epg" title="Detail view">
<div id="dialog_content">
hahaha
</div>
</div>

</body>
</html>