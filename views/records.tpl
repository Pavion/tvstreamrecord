%include header 
<div id="dialog-form" title="Create new record">
<p class="validateTips"></p>
<form>
<fieldset>
<label for="channel">Name</label>
<input type="text" maxlength="20" id="recname" class="text ui-widget-content ui-corner-all" name="recname" value=""/> 
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
</fieldset>
</form>
</div>
<div id="users-contain" class="ui-widget">
<h1>Records:
<button id="create-user">Create new record</button></h1>
<table id="recordlist"><!--<table id="clist1"><table id="users" class="ui-widget ui-widget-content">-->
<thead>
<tr class="ui-widget-header ">
<th class="rname">Record name</th>
<th class="rchan">Channel</th>
<th class="rat">at</th>
<th class="rtill">till</th>
<th class="rcontrols">control</th>
</tr>
</thead>
<tbody>
</tbody>
</table>
</div>
    
<div id="dialog" title="Dialog Title">
	<p>Shall I delete this record?</p>
</div>
<script type="text/javascript">
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1; //January is 0!
    var hr = today.getHours();
    var min = today.getMinutes();

    var yyyy = today.getFullYear();
    if(dd<10){dd='0'+dd} if(mm<10){mm='0'+mm} today = dd+'.'+mm+'.'+yyyy;
    document.getElementById("datepicker").value = today;
    if(hr<10){hr='0'+hr} if(min<10){min='0'+min} today = hr+':'+min;
    document.getElementById("timepicker_inline_div1").value = today;
    today = new Date();
    hr = today.getHours() + 1;
    if(hr==24) {hr=0} if(hr<10){hr='0'+hr} today = hr+':'+min;    
    document.getElementById("timepicker_inline_div2").value = today;

</script>
%include footer
           
