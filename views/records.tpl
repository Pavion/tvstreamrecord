%include ('create.tpl')
<div id="users-contain" class="ui-widget">
    <h1>§Records§:
        <button id="button_create_record">§Create new record§</button>
        <button id="button_purge_records">§Purge old records§</button>
    </h1>
    <table id="table_recordlist" recurr="§none§">
        <thead>
            <tr class="ui-widget-header ">
                <th class="rname">§Record name§</th>
                <th class="rchan">§Channel§</th>
                <th class="rat">§at§</th>
                <th class="rtill">§till§</th>
                <th class="rrecu">§Recurrent§</th>
                <th class="rcontrols">§Controls§</th>
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
    
<div id="dialog_remove" title="§Confirmation request§" cancel="§Cancel§" delete="§Delete§"> 
	<p>§Shall I delete this record?§</p>
</div>
<div id="dialog_purge" title="§Purging records§" ok="§OK§" cancel="§Cancel§">
	<p>§All old records will be deleted! Are you sure?§</p>
</div>
