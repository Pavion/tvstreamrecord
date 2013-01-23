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
<table id="users" class="ui-widget ui-widget-content">
<thead>
<tr class="ui-widget-header ">
<th>Record name</th>
<th>Channel</th>
<th>at</th>
<th>till</th>
<th>control</th>
</tr>
</thead>
<tbody>
%for row in rows1:
%chk = ""
%if row[5]==1:
%chk = "checked=\"checked\""
%end
<tr><td>{{row[1]}}</td><td>{{row[2]}}</td><td>{{row[3]}}</td><td>{{row[4]}}</td><td>
<div id="progressbar{{row[6]}}"></div>
<input type="checkbox" class="switch icons" id="switch-{{row[0]}}" {{chk}} />  
<a href="#" id="icons-{{row[0]}}" class="ui-state-default ui-corner-all"><span class="ui-icon ui-icon-trash"></span></a>
</tr>
%end
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
           
