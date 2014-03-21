%include header style=curstyle, version=version 
%include create
<div id="users-contain" class="ui-widget">
<h1>Channels:
<button id="button_create_channel">Create new</button>
<button id="button_import_clist">Import</button>
<button id="button_download_clist">Export</button>
</h1>
<table id="table_channellist"> 
<thead>
<tr class="ui-widget-header ">
<th class="cid">ID</th>
<th class="cname">Name</th>
<th class="curl">URL</th>
<th class="cext">Type</th>
<th class="ccontrols">Controls</th>
</tr>
</thead>
<tbody>
</tbody>
</table>
</div>
<div id="dialog_download_clist" title="Channel list download">
	<p align="center">Channel list export finished<br> 
    <a href="channels.m3u">right click to save as</a></p>
</div>
<div id="dialog_remove" title="Confirmation request">
	<p>Shall I delete this channel?</p>
</div>
<div id="dialog_create_channel" title="Create/edit a channel">
    <form>
        <fieldset>
            <label for="name">Channel ID</label>
            <input type="hidden" maxlength="5" id="prev" value=""/> 
            <input type="text" maxlength="5" id="ccid" class="text ui-widget-content ui-corner-all" name="ccid" value=""/> 
            <label for="name">Channel name</label>
            <input type="text" maxlength="30" id="cname" class="text ui-widget-content ui-corner-all" name="cname" value=""/> 
            <label for="channel">Channel URL</label>
            <input type="text" maxlength="512" id="cpath" class="text ui-widget-content ui-corner-all" name="cpath" value=""/> 
            <label for="channel">File extension (i.e. .mpg)</label>
            <input type="text" maxlength="8" id="cext" class="text ui-widget-content ui-corner-all" name="cext" value=""/> 
            <div id="chb1">
                <label for="lactive" id="lactive">Enabled</label>
                <input type="checkbox" class="switch icons" id="switch_list_active" checked="checked" />
            </div>  
            <div id="chb2">
                <label for="lepg" id="lepg">Grab EPG</label>
                <input type="checkbox" class="switch icons" id="switch_list_grab"  />  
            </div>  
        </fieldset>
    </form>
    <p class="validateTips"></p>
</div>
<div id="dialog_import_clist" title="Import channel list from .m3u file">
<form method='POST' enctype='multipart/form-data' action='/upload' name='uploader'>
<fieldset>
<label for="filenamelabel">.m3u file name</label>
<input type="file" id="upfile" width="80%" class="text ui-widget-content ui-corner-all" name="upfile" value=""/> 
<label for="append" id="append">Append to existing channels:</label>
<input type="checkbox" class="switch icons" name="switch_list_append" id="switch_list_append" />  
</fieldset>
</form>
</div>

%include footer
           
