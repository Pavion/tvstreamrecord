%include header 
<div id="users-contain" class="ui-widget">
<h1>Channels:
<button id="upload-user">Import</button>
<button id="create-channel">Create</button>
</h1>
<table id="clist"> <!-- <table id="users" class="ui-widget ui-widget-content">-->
<thead>
<tr class="ui-widget-header ">
<th class="cid">ID</th>
<th class="cname">Name</th>
<th class="curl">URL</th>
<th class="cext">Type</th>
<th class="ccontrols">Active</th>
</tr>
</thead>
<tbody>
</tbody>
</table>
</div>
<div id="dialog" title="Dialog Title">
	<p>Shall I delete this channel?</p>
</div>
<div id="createchannel-form" title="Create a new channel">
<form>
<fieldset>
<label for="name">Channel name</label>
<input type="text" maxlength="30" id="cname" class="text ui-widget-content ui-corner-all" name="cname" value=""/> 
<input type="checkbox" class="switch icons" id="switch01" checked="checked" />  
<label for="channel">Channel URL</label>
<input type="text" maxlength="100" id="cpath" class="text ui-widget-content ui-corner-all" name="cpath" value=""/> 
<label for="channel">File extension (i.e. .mpg)</label>
<input type="text" maxlength="8" id="cext" class="text ui-widget-content ui-corner-all" name="cext" value=""/> 
</fieldset>
</form>
</div>
<div id="upload-form" title="Import channel list from .m3u file">
<form method='POST' enctype='multipart/form-data' action='/upload' name='uploader'>
<fieldset>
<label for="filenamelabel">.m3u file name</label>
<input type="file" id="upfile" width="80%" class="text ui-widget-content ui-corner-all" name="upfile" value=""/> 
<label for="append" id="append">Append to existing channels:</label>
<input type="checkbox" class="switch icons" id="switch00" name="switch00" />  
</fieldset>
</form>
</div>

%include footer
           