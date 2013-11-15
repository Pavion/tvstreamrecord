%include header 
%include create
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
           
