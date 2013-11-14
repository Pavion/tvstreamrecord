%# coding=UTF-8
%include header 
<div id="zoom" zoom="{{zoom}}"></div>
<div id="users-contain" class="ui-widget">
<form method='POST' enctype='multipart/form-data' action='/epg' name='daychooser'>
<h1><div id="float">Current date:</div>
<input type="text" maxlength="10" id="datepicker3" class="text ui-widget-content ui-corner-all" name="datepicker3" value="{{curr}}"/> 
<div id="float">Keyword:</div>
<input type="text" maxlength="50" id="searchepg" class="text ui-widget-content ui-corner-all" name="searchepg" value=""/> 
<button id="searchepgbutton">Highlight</button>
<button id="getepg">Load XMLTV information</button>
%if grabstate[0] == False:
<button id="grabepgstart">Grab EPG from {{grabstate[2]}} streams</button>
%else:
<button id="grabepgstop">Stop grabbing EPG (State: {{grabstate[1]}}/{{grabstate[2]}})</button>
%end
</h1></form>
</div>
%cnt=0
%for rows in rowss:
%if len(rows)>0:
%if rows[0][0] == -1:
<div id="epg_cname" cnt="{{cnt}}"></div>
%else:
<div id="epg_cname" cnt="{{cnt}}"><h1><b><a href="live/{{rows[0][0]}}.m3u">{{rows[0][7]}}</a></b></h1></div>
%end
<div id="selectable">
%for row in rows:
<div class="ui-state-default" id="event" cnt="{{cnt}}" x="{{row[1]}}" width="{{row[2]}}" cid="{{row[0]}}" rid="{{row[6]}}" fulltext="{{row[5]}}" recording="{{row[8]}}" title="{{row[4]}}">{{row[3]}}</div>
%end
</div>
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

