%# coding=UTF-8
%include header 

<div id="users-contain" class="ui-widget">
<form method='POST' enctype='multipart/form-data' action='/epg' name='daychooser'>
<h1><div id="float">Current date:</div>
<input type="text" maxlength="10" id="datepicker3" class="text ui-widget-content ui-corner-all" name="datepicker3" value="{{curr}}"/> 
<button id="getepg">Load XMLTV information</button>
%if grabstate[0] == False:
<button id="grabepgstart">Grab EPG from {{grabstate[2]}} streams</button>
%else:
<button id="grabepgstop">Stop grabbing EPG (State: {{grabstate[1]}}/{{grabstate[2]}})</button>
%end
</h1></form>
%cnt=0
%for rows in rowss:
%if len(rows)>0:
%if rows[0][0] == -1:
<div id="epg_cname" cnt="{{cnt}}"></div>
<ol id="selectabletitle">
%else:
<div id="epg_cname" cnt="{{cnt}}"><h1><b><a href="live/{{rows[0][0]}}.m3u">{{rows[0][7]}}</a></b></h1></div>
<ol id="selectable">
%end
%for row in rows:
<li class="ui-state-default" id="event" cnt="{{cnt}}" x="{{row[1]}}" width="{{row[2]}}" cid="{{row[0]}}" rid="{{row[6]}}" fulltext="{{row[5]}}" recording="{{row[8]}}" title="{{row[4]}}">{{row[3]}}</li>
%end
</ol>
%cnt=cnt+1
%end
%end
</div>
<div id="record_from_epg" title="Detail view">
<div id="dialog_content"></div></div>
<form method='POST' enctype='multipart/form-data' action='/createepg' name='returnform'>
<input type="text" style="display: none;" name="ret" id="ret" value="X"/>
</form>

%include footer

