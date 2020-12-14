<div id="dialog_create_record" ctitle="§Create new record§" utitle="§Update record§" cancel="§Cancel§" delete="§Delete§" change="§Update§" schedule="§Create§">
<form>
    <fieldset>
        <input type="hidden" maxlength="5" id="rprev" value=""/> 
        <label for="channel">§Name§</label>
        <input type="text" maxlength="255" id="recname" class="text ui-widget-content ui-corner-all" name="recname" value=""/> 
        <label for="channel">§Channel§</label>
        <select name='channel' id="channel" class="text ui-widget-content ui-corner-all">
        %for row in rows2:
            <option value='{{row[0]}}'>{{row[1]}}</option>
        %end    
        </select>
        <input type="checkbox" class="switch icons" id="switch_create" checked="checked" />  
        <label for="name">§Start date§</label>
        <input type="text" maxlength="10" id="datepicker_create" class="text ui-widget-content ui-corner-all" name="name" value=""/> 
        <label for="email">§Start/end time§</label>
        <input type="text" maxlength="5" name="email" id="timepicker_inline_div1" class="text ui-widget-content ui-corner-all" />
        <input type="text" maxlength="5" name="email" id="timepicker_inline_div2" class="text ui-widget-content ui-corner-all" />
        <label for="recurr">§Recurrent records§</label>
        <div id="weekday">
            <input type="checkbox" id="wday0" /><label id="wwd0" for="wday0"></label>
            <input type="checkbox" id="wday1" /><label id="wwd1" for="wday1"></label>
            <input type="checkbox" id="wday2" /><label id="wwd2" for="wday2"></label>
            <input type="checkbox" id="wday3" /><label id="wwd3" for="wday3"></label>
            <input type="checkbox" id="wday4" /><label id="wwd4" for="wday4"></label>
            <input type="checkbox" id="wday5" /><label id="wwd5" for="wday5"></label>
            <input type="checkbox" id="wday6" /><label id="wwd6" for="wday6"></label>
        </div>
    </fieldset>
</form>
<!--<p class="validateTips"></p>-->
</div>