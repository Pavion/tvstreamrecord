/*
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

var dialognr = -1;
var weekdays = new Array('Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su');

function where() {
    return window.location.href.slice(window.location.href.lastIndexOf("/"));
}
function here(url) {
    var postto = window.location.href.slice(window.location.href.lastIndexOf("/"));
    return (postto == "/"+url || postto.startsWith("/"+url));
}

function switchMe(sw,  how) {
    if (how) {
        $(sw).attr("checked","checked");
        $("a"+sw).children(".ss-on").attr("style", "");
        $("a"+sw).children(".ss-slider").attr("style", "left: 13px;");
    } else {
        $(sw).removeAttr("checked");
        $("a"+sw).children(".ss-on").attr("style", "display: none;");
        $("a"+sw).children(".ss-slider").attr("style", "left: 0px;");
    }
}

function updateTips( t ) {
    $( ".validateTips" )
    .text( t )
    .addClass( "ui-state-highlight" );
    setTimeout(function() {
        $( ".validateTips" ).removeClass( "ui-state-highlight", 1500 );
    }, 500 );
}


function checkLength( o, n, min, max ) {
    x = document.getElementById(o);
    if ( x.value.length > max || x.value.length < min ) {
        $("#"+o).addClass( "ui-state-error" );
        updateTips( "Length of " + n + " must be between " +
        min + " and " + max + "." );
        return false;
    } else {
        return true;
    }
}

function checkRegexp(o, regexp, n ) {
    x = document.getElementById(o);
    if ( !( regexp.test( x.value ) ) ) {
        $("#"+o).addClass( "ui-state-error" );
        updateTips( n );
        return false;
    } else {
        return true;
    }
}

function initProgressbar() {
    $( "[id^=progressbar]" ).each(function(i) {
        $(this).progressbar({
            value: parseInt($(this).attr('id').replace("progressbar",""))
        });
        $(this).width(100);
        $(this).height(14);
        $(this).css("float", "left");
    });
}

function initIcons() {
    $( "[id^=iconsEPG-], [id^=icons-], [id^=iconsRec-]" ).hover(
        function() {
            $( this ).addClass( "ui-state-hover" );
        },
        function() {
            $( this ).removeClass( "ui-state-hover" );
        }
    );

    $( "[id^=iconsEPG-]" ).click(function( event ) {
        dialognr = parseInt($(this).attr('id').replace("iconsEPG-",""));
        post('/grab_channel', { myid:dialognr }, 0);
        if($( this ).children().hasClass( "ui-icon-plus" )) {
             $( this ).children().removeClass( "ui-icon-plus" );
             $( this ).children().addClass( "ui-icon-minus" );
        } else {
             $( this ).children().removeClass( "ui-icon-minus" );
             $( this ).children().addClass( "ui-icon-plus" );
        }
    });

    $( "[id^=iconsRec-]" ).click(function( event ) {
        dialognr = parseInt($(this).attr('id').replace("iconsRec-",""));
        $( "#dialog-form" ).dialog( "open" );
        event.preventDefault();
    });

    $( "[id^=icons-]" ).click(function( event ) {
        dialognr = parseInt($(this).attr('id').replace("icons-",""));
//        var postto = window.location.href.slice(window.location.href.lastIndexOf("/"));
//        if (postto.slice(0,8) == "/records") {
        if (here("records")) {
            $( "#dialog-form" ).dialog( "open" );
        } else {
            $( "#createchannel-form" ).dialog( "open" );
        }
        event.preventDefault();
    });

}

function initSwitch() {
    $('[id^=switch-]').each(function() {
        var switchnr = parseInt($(this).attr('id').replace("switch-",""));
//        var postto = window.location.href.slice(window.location.href.lastIndexOf("/"));
        $(this).slickswitch({
            toggledOn: function() {
                post(where(), { myid:switchnr, what:"1" }, 0);
            },
            toggledOff: function() {
                post(where(), { myid:switchnr, what:"0" }, 0);
            }
        });
    });
}

function post(dest1, data1, rel) {
    $.ajax({
        type: "POST",
        url: dest1,
        data: data1,
        dataType: "json",
        success: function(data, textStatus) {
            if(rel==1) {
                window.location.reload(false);
            }
        }
    });
}

function endsWith(str, suffix) {
    return str.indexOf(suffix, str.length - suffix.length) !== -1;
}


$(function() {
    $(document).tooltip();

    var pickerform = "dd.mm.yy";

    $("#timepicker_inline_div1").timepicker({
        constrainInput: true,
        showPeriodLabels: false
    });
    $("#timepicker_inline_div2").timepicker({
        constrainInput: true,
        showPeriodLabels: false
    });

    $( "#switch00" ).slickswitch();
    $( "#switch01" ).slickswitch();
    $( "#switch02" ).slickswitch();

    $( "#dialog" ).dialog({
        autoOpen: false,
        width: 300,
        buttons: [
            {
                text: "Delete",
                click: function() {
//                    var postto = window.location.href.slice(window.location.href.lastIndexOf("/"));
//                    if (postto.slice(0,7)=="/config") {
                    if (here("/config")) {
                        post("/removeepg", {}, 1);
                    } else {
                        post(where(), { myid:dialognr, what:"-1" }, 1);
                    }
                    $( this ).dialog( "close" );
                }
            },
            {
                text: "Cancel",
                click: function() {
                    $( this ).dialog( "close" );
                }
            }
        ]
    });

    $( "#cldown" ).dialog({
        autoOpen: false,
        width: 200,
        buttons: [
            {
                text: "OK",
                click: function() {
                    $( this ).dialog( "close" );
                }
            }
        ]
    });

    $( "#confirm01" ).dialog({
        autoOpen: false,
        width: 300,
        buttons: [
            {
                text: "OK",
                click: function() {
//                    var postto = window.location.href.slice(window.location.href.lastIndexOf("/"));
                    post(where(), { myid:'-1', what:"-2" }, 1);
                    $( this ).dialog( "close" );
                }
            },
            {
                text: "Cancel",
                click: function() {
                    $( this ).dialog( "close" );
                }
            }
        ]
    });

    $( "#datepicker" ).datepicker({
        constrainInput: true,
        minDate: -1,
        defaultDate: 0,
        dateFormat: pickerform
    });

    $( "#datepicker3" ).datepicker({
        constrainInput: true,
        minDate: 0,
        defaultDate: 0,
        onSelect: function() {
            document.daychooser.submit();
        },
        dateFormat: pickerform
    });


    $( "#slider" ).slider({
        range: true,
        values: [ 17, 67 ]
    });

    var selcount = 0;

    var zoom = +$("#zoom").attr('zoom');
    if (zoom==0) zoom=1;
    var maxcnt=0;

    $( "[id=event]" ).each(function(i) {
        w = +$(this).attr('width');
        x = +$(this).attr('x');
        cnt = +$(this).attr('cnt');
        rec = $(this).attr('recording');
        if(rec == 1) $(this).css("background", "#98FB98");
        $(this).css("font-size", ((cnt==0?11:8)+Math.round(Math.abs(zoom*2))) + 'px');

        if (zoom>0) {
            $(this).css("height", cnt==0?'20px':'60px');
            $(this).css("margin-top", cnt==0?10:(80+(cnt-1)*100) + 'px');
            $(this).css("margin-left", x+'%');
            $(this).css("width", w+'%');
        } else {
            $(this).css("left", cnt==0?0:((cnt-1) * 250 + 60) + 'px');
            $(this).css("top", x+'%');
            $(this).css("width", cnt==0?'50px':'240px');
            $(this).css("height", w + "%");
        }
    });

    $( "[id=epg_cname]" ).each(function(i) {
        cnt = +$(this).attr('cnt');
        if (cnt>maxcnt) maxcnt=cnt;
        if (zoom>0) {
            $(this).css("margin-top", (50+(cnt-1)*100) + 'px' );
        } else {
            $(this).css("width", cnt==0?'50px':'240px');
            $(this).css("margin-top", '-10px');
            $(this).css("margin-left", cnt==0?0:((cnt-1) * 250 + 60) + 'px');
            $(this).css("z-index", '1');

        }
    });

    if(!isNaN(zoom)) {
        if (zoom>0) {
            if(zoom!=1) $("body").css("width", (zoom*100)+"%");
            $("#mybody").css("height", (maxcnt * 100 + 100) +"px");
            $("[id=selectable]").each(function(i) { $(this).css("clear", "left"); });
        } else {
            $("[id=selectable]").each(function(i) {
                $(this).css("float", "left");
                $(this).css("height", (-zoom*800)+"px");
            });
            $("body").css("width", (250*maxcnt+100)+"px");
            $("#mybody").css("height", (-zoom*800+80)+"px");
        }
    }

    $( "#searchepg" ).change(function() {
        var tofind = $(this).val().toLowerCase();
        if (tofind.length>0) {

            $( "[id=event]" ).each(function(i) {
                var text = $(this).attr('fulltext').toLowerCase();
                if(text.indexOf(tofind)!=-1) {
                    $(this).addClass("ui-selected");
                } else {
                    $(this).removeClass("ui-selected");
                }
            });
        }
    });

    $( "#searchepgbutton" )
        .button()
        .click(function(event ) {
            $( "#searchepg" ).change();
            event.preventDefault();
        });

    $("[id=event]").live("click", function(event) {
           $("[id=event]").siblings().removeClass("ui-selected");
           $(this).addClass("ui-selected");
           var ft = $(this).attr("fulltext");
           if (ft)  {
            $("#ret").val($(this).attr("rid"));
            $("#dialog_content").html ( ft );
            $( "#record_from_epg" ).dialog( "open" );
            $(this).removeClass("ui-selected");
           }

    });


    var allFields =  $( [] ).add( "#recname" ).add( "#channel" ).add( "#datepicker" ).add( "#timepicker_inline_div1" ).add( "#timepicker_inline_div2" ).add("#cname").add("#ccid").add("#cpath");

    $( "#dialog-form" ).dialog({
        autoOpen: false,
        height: 350,
        width: 350,
        modal: true,
        open: function( event, ui ) {

            for(var i=0;i<7;i++) {
                $("#wwd"+i).removeClass("ui-state-active");
            }

            var cancelbutton = {
                text: "Cancel", click: function() {
                    $( this ).dialog( "close" );
                }
            };

            var deletebutton = {
                text: "Delete", click: function()
                {
                    $( this ).dialog( "close" );
                    $( "#dialog" ).dialog( "open" );
                }
            };

            var updatebutton = {
                text: ((dialognr==-1 || here('list'))?"Schedule a record":"Change a record"), click: function()
                {
                    var bValid = true;
                    allFields.removeClass( "ui-state-error" );
                    bValid = bValid && checkLength( "recname", "record name", 1, 255 );
                    bValid = bValid && checkRegexp( "recname", /^(?!^(PRN|AUX|CLOCK\$|NUL|CON|COM\d|LPT\d|\..*)(\..+)?$)[^\x00-\x1f\\?*:\";|//]+$/, "No special chars in this field please" );
                    bValid = bValid && checkLength( "channel", "channel", 1, 50 );
                    bValid = bValid && checkLength( "datepicker", "date", 10, 10 );
                    bValid = bValid && checkRegexp( "datepicker", /^((((0?[1-9]|[12]\d|3[01])[\.\-\/](0?[13578]|1[02])[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|((0?[1-9]|[12]\d|30)[\.\-\/](0?[13456789]|1[012])[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|((0?[1-9]|1\d|2[0-8])[\.\-\/]0?2[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|(29[\.\-\/]0?2[\.\-\/]((1[6-9]|[2-9]\d)?(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)|00)))|(((0[1-9]|[12]\d|3[01])(0[13578]|1[02])((1[6-9]|[2-9]\d)?\d{2}))|((0[1-9]|[12]\d|30)(0[13456789]|1[012])((1[6-9]|[2-9]\d)?\d{2}))|((0[1-9]|1\d|2[0-8])02((1[6-9]|[2-9]\d)?\d{2}))|(2902((1[6-9]|[2-9]\d)?(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)|00))))$/, "Please use DD.MM.YYYY for this field" );
                    bValid = bValid && checkLength( "timepicker_inline_div1", "start time", 5, 5 );
                    bValid = bValid && checkRegexp( "timepicker_inline_div1", /^(([0-1]?[0-9])|([2][0-3])):([0-5]?[0-9])(:([0-5]?[0-9]))?$/, "Please use HH:MM format for this field" );
                    bValid = bValid && checkLength( "timepicker_inline_div2", "end time", 5, 5 );
                    bValid = bValid && checkRegexp( "timepicker_inline_div2", /^(([0-1]?[0-9])|([2][0-3])):([0-5]?[0-9])(:([0-5]?[0-9]))?$/, "Please use HH:MM format for this field" );
                    var mask = 0;
                    for (var i=0; i<7; i++) {
                        if ( $("#wwd" + i).hasClass("ui-state-active") ) {
                            mask += Math.pow(2, i);
                        }
                    }
                    if ( bValid ) {
                        $( this ).dialog( "close" );
                        var akt = 0;
                        if ($("#switch00").attr("checked") == "checked") {akt = 1;}
                        post("/create", {
                            prev:$("#prev").val(),
                            recname:$("#recname").val(),
                            Sender:$("#channel").val(),
                            von:$("#timepicker_inline_div1").val(),
                            bis:$("#timepicker_inline_div2").val(),
                            am:$("#datepicker").val(),
                            aktiv:akt,
                            recurr:mask
                        }, 1);
                    }
                }
            };

            if((dialognr!=-1 && !here('list'))) {
                $( this ).dialog( "option", "buttons", [deletebutton, updatebutton, cancelbutton] );

                oTable = $('#recordlist').dataTable();
                var data = oTable.fnGetData();
                var len = data.length;
                if (len>0) {
                    for(var i=0;i<len;i++) {
                        if(data[i][7]==dialognr) {

                            var recur = data[i][4];
                            if(data!="no") {
                                for(var j=0;j<7;j++) {
                                    if(recur.search(weekdays[j])!=-1) {
                                        $("#wwd"+j).addClass("ui-state-active");
                                    }
                                }
                            }

                            var kids = $("#channel").children();
                            for (var j=0;j<kids.length;j++) {
                            	if (kids[j].innerHTML==data[i][1].replace(/<(?:.|\n)*?>/gm, '')) {

									$("#channel").val(kids[j].value);
                            		break;
                            	}	
                            }

                            switchMe("#switch00", ($("#switch-" + dialognr).attr("checked") == "checked") );
                            $("#prev").val(dialognr);
                            $("#recname").val(data[i][0]);
                            $("#timepicker_inline_div1").val(data[i][2].slice(11,16));
                            $("#timepicker_inline_div2").val(data[i][3].slice(11,16));
                            $("#datepicker").val(data[i][2].slice(0,10));
                            break;
                        }
                    }
                }
            } else {
                $( this ).dialog( "option", "buttons", [updatebutton, cancelbutton] );

                var today = new Date();
                var dd = today.getDate();
                var mm = today.getMonth()+1; //January is 0!
                var hr = today.getHours();
                var min = today.getMinutes();

                var yyyy = today.getFullYear();
                if(dd<10){dd='0'+dd;} if(mm<10){mm='0'+mm;} today = dd+'.'+mm+'.'+yyyy;
                $("#datepicker").val(today);
                if(hr<10){hr='0'+hr;} if(min<10){min='0'+min;} today = hr+':'+min;
                $("#timepicker_inline_div1").val(today);
                today = new Date();
                hr = today.getHours() + 1;
                if(hr==24) {hr=0;} if(hr<10){hr='0'+hr;} today = hr+':'+min;
                $("#timepicker_inline_div2").val(today);

                switchMe("#switch00", true);

                $("#channel").val(0);
                $("#prev").val("");
                $("#recname").val("");

                if(here("list")) {
                    $("#channel").val(dialognr);
                    $("#recname").val(document.getElementById("channel").options[document.getElementById("channel").selectedIndex].innerHTML);
                }
            }

        },
        close: function() {
            allFields.removeClass( "ui-state-error" );
        }
    });

    $( "#record_from_epg" ).dialog({
        autoOpen: false,
        height: 310,
        width: 350,
        modal: true,
        buttons: {
            "Record": function() {
                $( this ).dialog( "close" );
                $("#dialog_content").html("");
                document.returnform.submit();
            },
            Cancel: function() {
                $( this ).dialog( "close" );
                $("#dialog_content").html("");
            }
        },
        close: function() {
            $("#dialog_content").html("");
        }
    });



    $( "#upload-form" ).dialog({
        autoOpen: false,
        height: 190,
        width: 270,
        modal: true,
        buttons: {
            "Upload file": function() {
                $( this ).dialog( "close" );
                document.uploader.submit();
            },
            Cancel: function() {
                $( this ).dialog( "close" );
            }
        },
        close: function() {
            allFields.val( "" ).removeClass( "ui-state-error" );
        }
    });


    $( "#createchannel-form" ).dialog({
        autoOpen: false,
        height: 340,
        width: 250,
        modal: true,
        close: function() {
            allFields.val( "" ).removeClass( "ui-state-error" );
        },
        open: function( event, ui ) {

            var cancelbutton = {
                text: "Cancel", click: function() {
                    $( this ).dialog( "close" );
                }
            };
            var updatebutton = {
                text: (dialognr==-1?"Create channel":"Update"), click: function()
                {
                    var bValid = true;
                    allFields.removeClass( "ui-state-error" );
                    bValid = bValid & checkRegexp(  "ccid", /^[0-9]{1,5}$/, "Please enter a valid number" );
                    bValid = bValid & checkRegexp(  "cname", /^(?=\s*\S).*$/, "Please enter a valid name" );
                    bValid = bValid & checkRegexp(  "cpath", /^(?=\s*\S).*$/, "Please enter a valid URL" );
                    if (bValid) {
                        var akt = 0;
                        var epggrab = 0;
                        if ($("#switch01").attr("checked") == "checked") {akt = 1;}
                        if ($("#switch02").attr("checked") == "checked") {epggrab = 1;}
                        post("/create_channel", {
                            prev: $("#prev").val(),
                            ccid: $("#ccid").val(),
                            cname:$("#cname").val(),
                            cpath:$("#cpath").val(),
                            cext: $("#cext").val(),
                            aktiv:akt,
                            epggrab: epggrab
                        }, 1);
                        $( this ).dialog( "close" );
                    }
                }
            };
            var deletebutton = {
                text: "Delete", click: function()
                {
                    $( this ).dialog( "close" );
                    $( "#dialog" ).dialog( "open" );
                }
            };

            if(dialognr!=-1) {
                $( this ).dialog( "option", "buttons", [deletebutton, updatebutton, cancelbutton] );

                oTable = $('#clist').dataTable();
                var data = oTable.fnGetData();
                var len = data.length;
                if (len>0) {
                    for(var i=0;i<len;i++) {
                        if(data[i][0]==dialognr) {

                            switchMe("#switch01", ($("#switch-" + data[i][0]).attr("checked") == "checked") );
                            switchMe("#switch02", ( $("#iconsEPG-" + dialognr).children().attr("class").indexOf("plus") > 0) );

                            $("#prev").val(data[i][0]);
                            $("#ccid").val(data[i][0]);
                            $("#cname").val(data[i][1].replace(/<(?:.|\n)*?>/gm, ''));
                            $("#cpath").val(data[i][2]);
                            $("#cext").val(data[i][3]);
                            break;
                        }
                    }
                }
            } else {

                $( this ).dialog( "option", "buttons", [updatebutton, cancelbutton] );

                switchMe("#switch01", true );
                switchMe("#switch02", false );
                $("#prev").val("");
                $("#ccid").val("1");
                $("#cname").val("");
                $("#cpath").val("");
                $("#cext").val("");
            }

        }
    });

    $( "#create-user" )
        .button()
        .click(function() {
            dialognr = -1;
            $( "#dialog-form" ).dialog( "open" );
        });

    $( "#purge-records" )
        .button()
        .click(function() {
            $( "#confirm01" ).dialog( "open" );
        });

    $( "#getepg" )
        .button()
        .click(function(event ) {
            post("/getepg", {}, 0);
            event.preventDefault();
        });

    $( "#grabepgstart" )
        .button()
        .click(function(event ) {
            post("/grabepgstart", {}, 0);
            $(this).html('Please refresh to see progress');
            $(this).css('height', "20px");
            $(this).addClass( "ui-state-disabled" );
            event.preventDefault();
        });

    $( "#grabepgstop" )
        .button()
        .click(function(event ) {
            post("/grabepgstop", {}, 1);
            event.preventDefault();
        });

    $( "#removeepg" )
        .button()
        .click(function(event ) {
            $( "#dialog" ).dialog( "open" );
            //post("/removeepg", {}, 1);
            event.preventDefault();
        });

    $( "#resetlog" )
        .button()
        .click(function(event ) {
            post("/resetlog", {}, 1);
            event.preventDefault();
        });

    $( "#create-channel" )
        .button()
        .click(function(event ) {
            dialognr=-1;
            $( "#createchannel-form" ).dialog( "open" );
            event.preventDefault();
        });

    $( "#upload-user" )
        .button()
        .click(function(event ) {
            $( "#upload-form" ).dialog( "open" );
            event.preventDefault();
        });

    $( "#submit_cfg" )
        .button()
        .click(function(event ) {
            document.submit_cfg_form.submit();
            event.preventDefault();
        });

    $( "#downlog" )
        .button()
        .click(function(event ) {
            window.location = "./log.txt";
            event.preventDefault();
        });

    $( "#downcl" )
        .button()
        .click(function(event ) {

            $.ajax({
                type: "POST",
                url: "/clgen",
                data: {},
                dataType: "json",
                success: function(data, textStatus) {
                    $( "#cldown" ).dialog( "open" );
                }
            });
        });


     $( "#wday" ).button();
    $( "#weekday" ).buttonset();

     $('#clist').dataTable({
        "bJQueryUI": true,
        "sPaginationType": "full_numbers",
        "bProcessing": true,
        "sAjaxSource": "/channellist",
        "fnDrawCallback": function( oSettings ) {
            initSwitch();
            initIcons();
        },
        "fnRowCallback": function( nRow, aData, iDisplayIndex ) {
            var data4 = "";
            if (aData[4] == 1) data4 = "plus"; else data4="minus";
            var chk = "";
            if (aData[5] == 1) chk = 'checked="checked"';
            $('td:eq(4)', nRow).html('<input type="checkbox" class="switch icons" id="switch-' + aData[0] + '" ' + chk + ' /><label title="EPG grab?" id="iconsEPG-' + aData[0] + '" class="ui-state-default ui-corner-all"><span class="ui-icon ui-icon-'+data4+'"></span></label><label title="Create record" id="iconsRec-' + aData[0] + '" class="ui-state-default ui-corner-all"><span class="ui-icon ui-icon-play"></span></label><a href="#" id="icons-' + aData[0] + '" class="ui-state-default ui-corner-all"><span class="ui-icon ui-icon-gear"></span></a>');
        }
    });

     $('#recordlist').dataTable({
        "bJQueryUI": true,
        "sPaginationType": "full_numbers",
        "bProcessing": true,
        "sAjaxSource": "/getrecordlist",
        "aoColumnDefs": [ { "bSearchable": false, "bVisible": false, "aTargets": [ 6,7,8,9 ] },
                          { "iDataSort": 8, "aTargets": [ 2 ] },
                          { "iDataSort": 9, "aTargets": [ 3 ] } ],
        "fnDrawCallback": function( oSettings ) {
            initSwitch();
            initIcons();
            initProgressbar();

        },
        "fnRowCallback": function( nRow, aData, iDisplayIndex ) {
            var chk = "";
            if (aData[5] == 1) chk = 'checked="checked"';
            htmltext  = '<div id="progressbar' + aData[6] + '"></div>';
            htmltext += '<input type="checkbox" class="switch icons" id="switch-' + aData[7] + '" ' + chk + ' />';
            htmltext += '<a href="#" id="icons-' + aData[7] + '" class="ui-state-default ui-corner-all"><span class="ui-icon ui-icon-gear"></span></a>';
            $('td:eq(5)', nRow).html(htmltext);
        },
        "fnInitComplete": function() {
             this.fnSort([ [2,'desc'] ]);
        }

    });

     $('#loglist').dataTable({
        "bJQueryUI": true,
        "sPaginationType": "full_numbers",
        "bProcessing": true,
        "sAjaxSource": "/logget",
        "fnInitComplete": function() {
             this.fnSort([ [0,'desc'] ]);
        }
    });

});
