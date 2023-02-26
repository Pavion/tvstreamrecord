%include('create.tpl')
<div id="users-contain" class="ui-widget">
    <h1>Channels:
        <button id="button_create_channel">§Create new§</button>
        <button id="button_import_clist">§Import§</button>
        <button id="button_download_clist">§Export§</button>
    </h1>
    <table id="table_channellist"> 
        <thead>
            <tr class="ui-widget-header ">
                <th class="cid">ID</th>
                <th class="cname">§Channel name§</th>
                <th class="curl">§Channel URL§</th>
                <th class="cext">§Type§</th>
                <th class="ccontrols">§Controls§</th>
            </tr>
        </thead>
        <tbody>
        </tbody>
    </table>
</div>
<div id="dialog_download_clist" title="§Channel list download§" ok="§OK§">
	<p align="center">§Channel list export finished§<br> 
    <a href="channels.m3u">§right click to save as§</a></p>
</div>
<div id="dialog_remove" title="§Confirmation request§" cancel="§Cancel§" delete="§Delete§"> 
	<p>§Shall I delete this channel?§</p>
</div>
<div id="dialog_create_channel" title="§Create/edit a channel§" cancel="§Cancel§" create="§Create§" update="§Update§" delete="§Delete§" errname="§Please enter a valid name§" errid="§Please enter a valid ID§" errurl="§Please enter a valid URL§" >
    <form>
        <fieldset>
            <label for="name">§Channel ID§</label>
            <input type="hidden" maxlength="5" id="cprev" value=""/> 
            <input type="text" maxlength="5" id="ccid" class="text ui-widget-content ui-corner-all" name="ccid" value=""/> 
            <label for="name">§Channel name§</label>
            <input type="text" maxlength="30" id="cname" class="text ui-widget-content ui-corner-all" name="cname" value=""/> 
            <label for="channel">§Channel URL§</label>
            <input type="text" maxlength="512" id="cpath" class="text ui-widget-content ui-corner-all" name="cpath" value=""/> 
            <label for="channel">§File extension (i.e. .mpg)§</label>
            <input type="text" maxlength="8" id="cext" class="text ui-widget-content ui-corner-all" name="cext" value=""/> 
            <label for="lactive" id="lactive">§Enabled§</label>
            <input type="checkbox" class="switch icons" id="switch_list_active" checked="checked" />
        </fieldset>
    </form>
    <p class="validateTips"></p>
</div>
<div id="dialog_import_clist" title="§Import channel list§" upload="§Import§" cancel="§Cancel§">
    <form method='POST' enctype='multipart/form-data' action='/upload' name='uploader'>
        <fieldset>
            <label for="filenamelabel">§From .m3u file§</label>
            <input type="file" id="upfile" width="80%" class="text ui-widget-content ui-corner-all" name="upfile" value=""/>
            <label for="filenamelabel">§From HTTP URL§</label>
            <input type="text" id="upfileurl" class="text ui-widget-content ui-corner-all" name="upfileurl" value=""/>
            <label for="append" id="append">§Append to existing channels§:</label>
            <input type="checkbox" class="switch icons" name="switch_list_append" id="switch_list_append" />
        </fieldset>
    </form>
</div>
