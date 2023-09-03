/**
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License,
    or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, see <http://www.gnu.org/licenses/>.

    @author: Pavion
*/

// Default locale
var weekdays = ["Su","Mo","Tu","We","Th","Fr","Sa"];
var firstday = 1;
var dateformat = "mm/dd/yy";

// Varlist
var rprev = ""; // No edit support as of now, use standard version instead
var recname = ""; // Record name
var sender = ""; // Channel ID
var cname = "";// Channel name
var rday = ""; // Record date as JS object
var am = "";  // Text date
var von = ""; // Start time
var bis = ""; // End time
var akt = 1; // Active only for now
var mask = 0; // Recurrent records
var title = ""; //  Record title

$(function() {
    // Localization
    getLocale();

    function showChannels() {
        $.get( "getchannelgroups", function( data )  {
            var data = data.aaData;
            if (data.length==0) {
                alert ("This is a mobile version of tvstreamrecord.\nNo channels could be found, please configure this package in a desktop version first!\nYou will be now redirected to the channel creation page.");
                window.location ="list";
                exit();
            }

            $("#set").empty();
            $("#set").append($('<div data-role="collapsible" id="set-" data-collapsed="true"><h3>Top10</h3></div>'));
            for (var i = 0; i < data.length; i++) {
                $("#set").append($('<div data-role="collapsible" id="set' + data[i][0] + '" data-collapsed="true"><h3>' + data[i][0] + '.. (' + data[i][1] + ')</h3></div>'));
            }
            $("#set").trigger( "create" );

            $('#set').children().bind('collapsibleexpand', function () {
                var id = $(this).attr('id').replace("set","");
                // Set expanded
                var my = $(this);
                $("#blip").remove();

                $.post( "getchannelgroup", {"id": id}, function( data )  {
                    var data = data.aaData;
                    my.children(".ui-collapsible-content").empty().append($("<ul data-role='listview' id='blip'></ul>"));

                    for (var i = 0; i < data.length; i++) {
                        $("#blip").append($("<li id='chli-" + data[i][0] + "'><a href='#'>" + data[i][1] + "</a></li>"));
                    }

                    // Channel selection
                    $("#blip").listview().children().click(function() {
                        sender = $(this).attr("id").replace("chli-","");;
                        cname = $(this).text().trim();
                        $("body").pagecontainer("change", "#day");
                    });

                },"json");

            }).bind('collapsiblecollapse', function () {
                // Data can be released here but why? It's already there.
            });

        },"json");
        
    }   
    
    // Add new record button
    $("#btn_add").click(function(event) {
        event.preventDefault();
        $("body").pagecontainer("change", "#channel");
        title = "";
        rprev = ""; 
        recname = ""; 
        sender = ""; 
        cname = "";
        rday = "";
        am = "";  
        von = "";
        bis = "";
        akt = 1; 
        mask = 0; 
        showChannels();
    });

    // Day confirmation button
    $("#btn_day_ok").click(function(event) {
        event.preventDefault();

        rday =  $("#datebox1").datebox('getTheDate');
        var m = rday.getMonth()+1;  var mt = m<10?"0"+m:m;
        var d = rday.getDate();     var dt = d<10?"0"+d:d;
        am = rday.getFullYear() + "-" + mt + "-" + dt;

        if (von != "" && bis != "") {
            $("body").pagecontainer("change", "#time");
            $("#timebox_v").datebox("setTheDate",new Date(von));
            $("#timebox_b").datebox("setTheDate",new Date(bis));                    
        } else {
            $.post( "getepgday", {"cname": cname, "rdate": am}, function( data )  {
                if (data) {
                    var data = data.aaData;
                    $("body").pagecontainer("change", "#epg");
                    $("#epglist").empty();
                    $("#epglist").append($('<li start="" stop=""><a href="#"><h2>' + $("#epglist").attr('skip') + ' EPG</h2></a></li>'));

                    for (var i = 0; i < data.length; i++) {
                        if (data[i][0].length===50) data[i][0] += "...";
                        if (data[i][2].length===100) data[i][2] += "...";
                        $("#epglist").append($('<li start="' + data[i][1].substr(11,5) + '" stop="' + data[i][3].substr(11,5) + '"><a href="#"><h2>' + data[i][0] + '</h2><p>' + data[i][2] + '</p><p class="ui-li-aside"><strong>' + data[i][1].substr(11,5) + '</strong></p></a></li>'));
                    }
                    $("#epglist").listview().children().click(function() {
                        $("body").pagecontainer("change", "#time");
                        if ($(this).attr("start")=="") {
                            $("#timebox_v").datebox("setTheDate",new Date((new Date()).getTime()));
                            $("#timebox_b").datebox("setTheDate",new Date((new Date()).getTime() + 1*60*60*1000));
                        } else {
                            // Use EPG delta? Yes!
                            var delta_before = $("#delta_before_epg").attr("delta");
                            var delta_after = $("#delta_after_epg").attr("delta");
                            $("#timebox_v").datebox("setTheDate",new Date(new Date(1970,0,1,parseInt($(this).attr("start").substr(0,2)),parseInt($(this).attr("start").substr(3,2)),0,0).getTime() - delta_before*60000 ));
                            $("#timebox_b").datebox("setTheDate",new Date(new Date(1970,0,1,parseInt($(this).attr("stop").substr(0,2)),parseInt($(this).attr("stop").substr(3,2)),0,0).getTime() + delta_after*60000 ));
                            title = $(this).children('a').children('h2').text();
                        }
                    });
                    $("#epglist").listview( "refresh" );

                } else {
                    $("body").pagecontainer("change", "#time");
                    $("#timebox_v").datebox("setTheDate",new Date((new Date()).getTime()));
                    $("#timebox_b").datebox("setTheDate",new Date((new Date()).getTime() + 1*60*60*1000));
                }

            },"json");
        }
    });

    // Time confirmation button
    $("#btn_time_ok").click(function(event) {
        event.preventDefault();
        var time_v =  $("#timebox_v").datebox('getTheDate');
        var time_b =  $("#timebox_b").datebox('getTheDate');
        von = time_v.getHours() + ":" + time_v.getMinutes()
        bis = time_b.getHours() + ":" + time_b.getMinutes()

        $("body").pagecontainer("change", "#rname");
        if (title === "") {
            $("#recname").val(cname);
        } else {
            $("#recname").val(title);
        }

        for(var i=0;i<7;i++) {
            $("#wwd"+i).text(weekdays[i]);
        }
        for(var i=0;i<firstday;i++) {
            $( "#wwd"+i ).parent().insertAfter( $( "#wday" + (i===0?6:i-1) ).parent());
        }
        if (mask == "") mask = 0;
        for(var i=0;i<7;i++) {
            if ( (mask & Math.pow(2,i)) == Math.pow(2,i)) {
                $("#wday"+i).prop("checked",true).checkboxradio("refresh");
            } else {
                $("#wday"+i).prop("checked",false).checkboxradio("refresh");
            }
        }
        $("#recurr").controlgroup( "refresh" );

    });

    // Record name confirmation button (and record creation)
    $("#btn_rname_ok").click(function(event) {
        event.preventDefault();
        rn = $("#recname").val().trim();
        if (rn!="") {
            $("#recname").val("");
            recname = rn;

            mask = 0;
            for (var i=0; i<7; i++) {
                if ( $("#wwd" + i).hasClass("ui-checkbox-on") ) {
                    mask += Math.pow(2, i);
                }
            }

            $.post("create", {
                            "rprev": rprev,
                            "recname":recname,
                            "Sender":sender,
                            "von":von,
                            "bis":bis,
                            "am":am,
                            "aktiv":akt,
                            "recurr":mask
                        }, function() {
                            $("body").pagecontainer("change", "#");
                            getTableData();                            
                        }, "json");
        }
    });

    // Each cancel button    
    $("[id^=btn_cancel]").click(function(event) {
        event.preventDefault();
        $.mobile.navigate("#");
    });

    // Record deletion button (icon)
    $("#dia_del").click(function(event) {
        if (act_rid!=-1) {
            event.preventDefault();
            $.post("records", { "what": -1, "myid":act_rid }, function() {
                $.mobile.navigate("#");
                getTableData();
            }, "json");
        }
    });


    // Entry point check. Ask forgiveness not permission.
    try {
        $("#rectable").table("refresh");
        getTableData();
    } catch (e) {
        $("body").pagecontainer("change", "#");
        getTableData();
    }

});

var act_rid = -1;

function getTableData() {
    $("#recbody").empty();
    $.get( "getrecordlist", function( data )  {
        var data = data.aaData;
        for (var i = 0; i < data.length; i++) {
            var row = "<tr><th>" + data[i][0] + "</th>";
            row += "<td>" + data[i][1] + "</td>";
            row += "<td>" + formatDate(data[i][2],dateformat) + "</td>";
            row += "<td>" + formatDate(data[i][3],dateformat) + "</td>";
            var recurr = "";
            if (data[i][4] == 0) {
                recurr = $('#rectable').attr("recurr");
            } else {
                for(var j=firstday; j<7+firstday; j++) {
                    var day = j>=7?j-7:j;
                    if (( data[i][4] & Math.pow(2,day)) === Math.pow(2,day)) recurr += weekdays[day];
                }
            }
            row += "<td>" + recurr + "</td>";
            row += '<td><div id="flt"><input type="checkbox" id="chk-' + data[i][7] + '" data-mini="true" data-role="flipswitch" >';
            row += '<a href="#" id="edt-' + data[i][7] + '" class="ui-btn ui-btn-icon-notext ui-corner-all ui-icon-gear ui-nodisc-icon ui-alt-icon"></a>';
            row += '<a href="#" id="del-' + data[i][7] + '" class="ui-btn ui-btn-icon-notext ui-corner-all ui-icon-delete ui-nodisc-icon ui-alt-icon"></a>';
            row += '</div></td></tr>';
            $("#recbody").append($(row));
            $("#chk-" + data[i][7]).flipswitch();
            if (data[i][5] == 1) {
                $("#chk-" + data[i][7]).prop( "checked", true ).flipswitch( "refresh" );
            }
            $("#chk-" + data[i][7]).change(function(event) {
                event.stopPropagation();
                var what = $(this).prop( "checked" )?1:0;
                var myid = $(this).attr("id").replace("chk-","");
                $.post("records", { "what": what, "myid":myid }, function() {}, "json");
            });
            $("#edt-" + data[i][7]).click(function(event) {
                event.stopPropagation();
                event.preventDefault();
                var myid = $(this).attr("id").replace("edt-","");
                var mydata;
                for (var j=0;j<data.length;j++) {
                    if(data[j][7] == myid) {
                        mydata = data[j];
                        break;
                    }
                }
                     
                rprev = mydata[7]; 
                title = mydata[0]; 
                recname = mydata[0]; 
                sender = mydata[10]; 
                cname = mydata[1];
                von = mydata[8];
                bis = mydata[9];
                akt = mydata[5]; 
                mask = mydata[4]; 

                $("body").pagecontainer("change", "#day");
                $("#datebox1").datebox('setTheDate', new Date(von));
            });
            $("#del-" + data[i][7]).click(function(event) {
                event.preventDefault();
                act_rid = $(this).attr("id").replace("del-","");
                $("#lnkDialog").click();
            });


        }
        $("#rectable").table("refresh");
    },"json");
}

// Dateflipbox and timeflipbox localization
function getLocale() {
    var mydata = $("#locale").attr("loc");
    try {
        var data = jQuery.parseJSON( mydata );
        datef = data.dateFormat.toLowerCase();
        m = datef.indexOf("m");
        d = datef.indexOf("d");
        y = datef.indexOf("y");

        var fo=(m>d)?((y>m)?['d','m','y']:((y>d)?['d','y','m']:['y','d','m'])):((y>m)?((y>d)?['m','d','y']:['m','y','d']):['y','m','d']);

        weekdays = data.dayNamesMin;
        firstday = data.firstDay;
        dateformat = data.dateFormat;

        jQuery.extend(jQuery.mobile.datebox.prototype.options.lang, {
            'curr': {
                daysOfWeek: data.dayNames,
                daysOfWeekShort: data.dayNamesShort,
                monthsOfYear: data.monthNames,
                monthsOfYearShort: data.monthNamesShort,
                durationLabel: ['Days', data.hourText, data.minuteText, data.secondText],
                timeFormat: 24,
                dateFieldOrder: fo,
                headerFormat: '',
                slideFieldOrder: fo,
                calStartDay: data.firstDay
            }
        });
        jQuery.extend(jQuery.mobile.datebox.prototype.options, {
            useLang: 'curr'
        });
    } catch (e) {
        // Die quiet
    }
}

// Date conversion
function formatDate(date_in) {
    var date = new Date(Date.parse(date_in.substr(0,10)));
    var time = date_in.substr(11,5);
    var m = date.getMonth()+1;  var mt = m<10?"0"+m:m;
    var d = date.getDate();     var dt = d<10?"0"+d:d;
    var yt = date.getFullYear();
    return dateformat.replace("mm", mt).replace("dd",dt).replace("yy",yt) + " " + time;
}