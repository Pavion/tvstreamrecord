%include ('create.tpl')
<div id="keyword_for_epg" keyword_for_epg="{{keyword_for_epg}}"></div>
<div id="delta_before_epg" delta="{{deltab}}"></div>
<div id="delta_after_epg" delta="{{deltaa}}"></div>
    <div id="listmode" value="{{listmode}}"></div>
<div id="users-contain" class="ui-widget">
    <h1><div class="lefty">§Electronic Program Guide§ - §list view§</div>
<button id="grabepg" class="grabepgclass">§Import EPG§</button>
</h1>
<table id="table_epglist">
    <thead>
        <tr class="ui-widget-header">
            <th class="echan">§Channel§</th>
            <th class="etit">§Title§</th>
            <th class="edesc">§Description§</th>
            <th class="estart">§Start time§</th>
            <th class="estop">§End time§</th>
            <th class="econtrol">§Record§</th>
        </tr>
    </thead>
    <tbody>
    </tbody>
</table>
</div>
<div id="dialog_record_from_epg" title="§Detail view§" record="§Record§" tunerecord="§Edit&Record§" cancel="§Cancel§">
    <div id="dialog_content"></div>        
</div>
<div id="dialog_remove" title="§Confirmation request§" cancel="§Cancel§" delete="§Delete§"> 
	<p>§Shall I delete this record?§</p>
</div>
<form>
    <input type="text" style="display: none;" name="ret" id="ret" value="X"/>
</form>