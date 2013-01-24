%include header 

%for rows in rowss:
%if rows[0][0] == 1:
<ol id="selectabletitle">
%else:
<ol id="selectable">
%end
%for row in rows:
<li class="ui-state-default" id="event" x="{{row[1]}}" width="{{row[2]}}" y="{{row[0]}}" title="{{row[4]}}">{{row[3]}}</li>
%end
</ol>
%end

</body>
</html>