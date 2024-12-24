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

/**
 * Common functions
 */

/**
 * Persistent variables
 */
var recName;
var recChannel;
var recDate;
var recStart;
var recEnd;

/**
 * @param {int} days Number of days to be added to this date object
 * @returns {Date|Date.prototype.addDays.dat}
 */
Date.prototype.addDays = function(days)
{
    var dat = new Date(this.valueOf());
    dat.setDate(dat.getDate() + days);
    return dat;
};

/**
 * Parse String to local Date
 * @param {type} stringDate in form: yyyy-mm-dd hh:mm:ss
 * @returns {Date} object
 */
function parseDate(stringDate) {
    var comp = stringDate.replace(" ", "-").replace(/:/g, "-").split("-");
    return new Date(comp[0], comp[1], comp[2], comp[3], comp[4], comp[5]);
}

/**
 * String function substitute
 */
if(typeof String.prototype.trim !== 'function') {
  String.prototype.trim = function() {
    return this.replace(/^\s+|\s+$/g, '');
  };
}

/**
 * String function substitute
 */
if (typeof String.prototype.startsWith !== 'function') {
  String.prototype.startsWith = function (str){
    return this.slice(0, str.length) == str;
  };
}

/**
 * Search function
 * @param {type} str Input string
 * @param {type} suffix Search suffix
 * @returns {Boolean} if the input string ends with supplied suffix
 */
function endsWith(str, suffix) {
    return str.indexOf(suffix, str.length - suffix.length) !== -1;
}

/**
 * Get location we are at now
 * @returns {String} location we are at
 */
function where() {
    var pos = window.location.href.lastIndexOf("&");
    return window.location.href.slice(window.location.href.lastIndexOf("/"), pos==-1?999:pos);
}

/**
 * Checks if we are at desired location
 * @param {type} url location to check with
 * @returns {Boolean} if we are located here
 */
function here(url) {
    var postto = window.location.href.slice(window.location.href.lastIndexOf("/"));
    return (postto == "/"+url || postto.startsWith("/"+url));
}

/**
 * Function to switch state
 * @param {type} sw Switch object
 * @param {type} how New value
 * @returns {undefined}
 */
function switchMe(sw,  how) {
    if (how) {
        $(sw).trigger('ss-toggleOn');

    /*    $(sw).attr("checked","checked");
        $("a"+sw).children(".ss-on").attr("style", "");
        $("a"+sw).children(".ss-slider").attr("style", "left: 13px;");*/
    } else {
        $(sw).trigger('ss-toggleOff');
    /*    $(sw).removeAttr("checked");
        $("a"+sw).children(".ss-on").attr("style", "display: none;");
        $("a"+sw).children(".ss-slider").attr("style", "left: 0px;");*/
    }
}

/**
 * Common function for updating tooltips
 * @param {type} t Tooltip text
 * @returns {undefined}
 */
function updateTips( t ) {
    $( ".validateTips" )
    .text( t )
    .addClass( "ui-state-highlight" );
    setTimeout(function() {
        $( ".validateTips" ).removeClass( "ui-state-highlight", 1500 );
    }, 500 );
}

/**
 * Common length check function
 * @param {type} o Object to check on
 * @param {type} n Tooltip info
 * @param {type} min minimal value
 * @param {type} max maximal value
 * @returns {Boolean}
 */
/*function checkLength( o, n, min, max ) {
    x = document.getElementById(o);
    if ( x.value.length > max || x.value.length < min ) {
        $("#"+o).addClass( "ui-state-error" );
        updateTips( "Length of " + n + " must be between " + min + " and " + max + "." );
        return false;
    } else {
        return true;
    }
}*/

/**
 * Common REGEXP check function
 * @param {type} o Object to check on
 * @param {type} regexp REGEXP to check with
 * @param {type} n Tooltip info
 * @returns {Boolean}
 */
function checkRegexp(o, regexp, n ) {
    x = document.getElementById(o);
    if ( !( regexp.test( x.value ) ) ) {
        $("#"+o).addClass( "ui-state-error" );
        updateTips( n );
        return false;
    } else {
        $("#"+o).removeClass( "ui-state-error" );
        return true;
    }
}

/**
 * Function to initialize all progress bars in a table
 * @returns {undefined}
 */
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

/**
 * Function to initialize all icons in a table
 * @returns {undefined}
 */
var dialognr = -1;
function initIcons() {
    $( "[id^=icons-], [id^=iconsRec-], [id^=iconsDisable-], [id^=iconsEStop-], [id^=iconsERec-]" ).hover(
        function() {
            $( this ).addClass( "ui-state-hover" );
        },
        function() {
            $( this ).removeClass( "ui-state-hover" );
            $(".ui-tooltip-content").parents('div').remove();
        }
    );

    $( "[id^=iconsDisable-]" ).click(function( event ) {
        dialognr = parseInt($(this).attr('id').replace("iconsDisable-",""));
        $( "#dialog_channel_disable" ).dialog( "open" );
        event.preventDefault();
    });

    $( "[id^=iconsRec-]" ).click(function( event ) {
        dialognr = parseInt($(this).attr('id').replace("iconsRec-",""));
        $( "#dialog_create_record" ).dialog( "open" );
        event.preventDefault();
    });

    $( "[id^=iconsERec-]" ).click(function( event ) {
        dialognr = parseInt($(this).attr('id').replace("iconsERec-",""));
        oTable = $('#table_epglist').dataTable();
        var data = oTable.fnGetData();
        var len = data.length;
        if (len>0) {
            for(var i=0;i<len;i++) {
                if(data[i][6]==dialognr) {
                    $("#ret").val(dialognr);
                    var dat_v = data[i][3].split(" ")[1].substr(0,5);
                    var dat_b = data[i][4].split(" ")[1].substr(0,5);
                    var delta_before = $("#delta_before_epg").attr("delta");
                    var delta_after = $("#delta_after_epg").attr("delta");
                    $( "#dialog_content" ).html ("<b>" + data[i][1] + ": "+dat_v + " - " + dat_b + "</b><BR><BR>" + data[i][2].replace(/\n/g, '<BR>'));
                    recName = data[i][1];
                    recChannel = data[i][0];
                    recDate = data[i][3].split(" ")[0];
                    recStart = new Date( parseDate(data[i][3]).valueOf() - delta_before*60000 ).toTimeString().substring(0, 5);
                    recEnd = new Date( parseDate(data[i][4]).valueOf() + delta_after*60000 ).toTimeString().substring(0, 5);

                    $( "#dialog_record_from_epg" ).dialog( "open" );
                    event.preventDefault();
                    break;
                }
            }
        }
    });

    $( "[id^=iconsEStop-]" ).click(function( event ) {
        dialognr = parseInt($(this).attr('id').replace("iconsEStop-",""));
        $( "#dialog_remove" ).dialog( "open" );
    });

    $( "[id^=icons-]" ).click(function( event ) {
        dialognr = parseInt($(this).attr('id').replace("icons-",""));
        if (here("records")) {
            $( "#dialog_create_record" ).dialog( "open" );
        } else {
            $( "#dialog_create_channel" ).dialog( "open" );
        }
        event.preventDefault();
    });

}

/**
 * Function to initialize all switches in a table
 * @returns none
 */
function initSwitch() {
    $('[id^=switch-]').each(function() {
        var switchnr = parseInt($(this).attr('id').replace("switch-",""));
        var data = $('.dataTable').DataTable().row( "tr:has(input#switch-" + switchnr + ")" ).data();
        $(this).slickswitch({
            toggledOn: function() {                        
                data[5]=1;
                post(where(), { myid:switchnr, what:"1" }, 0);
            },
            toggledOff: function() {
                data[5]=0;
                post(where(), { myid:switchnr, what:"0" }, 0);
            }
        });
    });
}

function post(dest1, data1, rel) {
    if(rel==1) {
        $("html").fadeTo("fast", 0.4);
        new imageLoader(cImageSrc, 'startAnimation()');
    }
    $.ajax({
        type: "POST",
        url: dest1,
        data: data1,
        dataType: "json",
        success: function() {
            if(rel==1) {
                window.location.reload(false);
            } else if (rel==2) {
                oTable = $('table:visible').DataTable();
                oTable.ajax.reload();
            }
        }
    });
}

/**
 * Can be used to dynamic adjust row colors for DataTables. Not used for now.
 * @returns {undefined}
 */
function paintTable() {
    // no row style in jQuery ThemeRoller :(
    /*$("tr:even").css("background-color", $("table.dataTable thead th").css("background-color") );
    $("tr:odd").css("background-color", $(".ui-tabs").css("background-color") );*/
}

/**
 * EPG button mode selector
 */
var epgmode = 0;

/**
 * Function for initializing EPG grab button
 * @return none
 */
function initEpgState() {
    getEpgState();
    $( "#grabepg" ).button()
    .click(function(event) {
        $.post("/grabepg", {"mode": epgmode},
            function() {
                getEpgState();
            }, "json");
        event.preventDefault();
    });
}

/**
 * Function for getting the current EPG state from server
 * @return none
 */
function getEpgState() {
    $.get("/getepgstate",
        function(data) {
            var state = data.grabState;
            epgmode = 0;
            $( "#grabepg" ).removeProp("disabled");
            $( "#grabepg" ).removeClass("ui-state-disabled");
            if (state[2]=='0') {
                $( "#grabepg" ).hide();
            } else {
                if (state[0] == false) {
                    //$( "#grabepg" ).html($( "#grabepg" ).attr("text1") );
                } else {
                    //if (state[3] == false) {
                        //$( "#grabepg" ).html($( "#grabepg" ).attr("text3") + " (" + state[1] + '/' + state[2] + ")");
                    //} else {
                        //$( "#grabepg" ).html($( "#grabepg" ).attr("text4"));
                        $( "#grabepg" ).prop("disabled", true);
                        $( "#grabepg" ).addClass("ui-state-disabled");
                    //}
                    epgmode = 1;
                }
                $( "#grabepg" ).show();
            }
        }, "json"
    );
}

$(function() {
    $(document).tooltip();

// Localization
    var language = $("#mybody").attr("language");

    $( "#datepicker_local" ).datepicker();
    //$( "#timepicker_local" ).timepicker();
    var mydateformat = $( "#datepicker_local" ).datepicker( "option", "dateFormat" );
    var mytimeformat = "HH:mm"; //$( "#timepicker_local" ).datepicker( "option", "timeFormat" );
    var weekdays = $( "#datepicker_local" ).datepicker( "option", "dayNamesMin");
    var firstday = $( "#datepicker_local" ).datepicker( "option", "firstDay");

// Common menu handling
    for ( var m = 0; m < $("#mainmenu").children().length; m ++ ) {
        if (where() ==  $( $("#mainmenu").children()[m] ).children().attr("href") ) {
            $( $("#mainmenu").children()[m] ).addClass('ui-tabs-active ui-state-active');
            break;
        }
    }

// Common dialogs and forms
    $("#timepicker_inline_div1,#timepicker_inline_div2,#cfg_grab_time").timepicker({
        constrainInput: true,
        showPeriodLabels: false,
        timeFormat: mytimeformat
    });

    $( "#dialog_remove" ).dialog({
        autoOpen: false,
        buttons: [{
            text: $( "#dialog_remove" ).attr("delete"),
            click: function() {
                if (here("config")) {
                    post("/removeepg", {}, 1);
                } else if (here("epglist") || here("records")) {
                    post("/records", { myid:dialognr, what:"-1" }, 2);
                } else if (here("epgchart")) {
                    post("/records", { myid:dialognr, what:"-1" }, 1);
                } else {
                    post(where(), { myid:dialognr, what:"-1" }, 1);
                }
                $( this ).dialog( "close" );
            }
        },
        {
            text: $( "#dialog_remove" ).attr("cancel"),
            click: function() {
                $( this ).dialog( "close" );
            }
        }]
    });

// Record create dialogs and forms
    var allFields =  $( [] ).add( "#recname" ).add( "#channel" ).add( "#datepicker_create" ).add( "#timepicker_inline_div1" ).add( "#timepicker_inline_div2" ).add("#cname").add("#ccid").add("#cpath");

    for(var i=0;i<7;i++) {
        $("#wwd"+i).text(weekdays[i]);
    }
    for(var i=0;i<firstday;i++) {
        $( "#wwd"+i ).insertAfter( $( "#wwd" + (i===0?6:i-1) ));
    }
    $( "#weekday" ).buttonset();


    $( "#switch_create").slickswitch();

    $( "#datepicker_create" ).datepicker({
        constrainInput: true,
        minDate: -1,
        defaultDate: 0
    });

    $( "#dialog_create_record" ).dialog({
        autoOpen: false,
        width: 400,
        modal: true,
        open: function( event, ui ) {

            for(var i=0;i<7;i++) {
                $("#wwd"+i).removeClass("ui-state-active");
            }

            var cancelbutton = {
                text: $(this).attr("cancel"), click: function() {
                    $( this ).dialog( "close" );
                }
            };

            var deletebutton = {
                text: $(this).attr("delete"), click: function()
                {
                    $( this ).dialog( "close" );
                    $( "#dialog_remove" ).dialog( "open" );
                }
            };

            var updatebutton = {
                text: ((dialognr==-1 || here('list') || here('epglist'))?$(this).attr("schedule"):$(this).attr("change")), click: function()
                {
                    var bValid = true;
                    allFields.removeClass( "ui-state-error" );

                    if ( $( "#recname" ).val().length == 0 ) { $( "#recname" ).addClass( "ui-state-error" ); bValid = false; }
                    if ( ! $.datepicker.parseTime("H:m", $( "#timepicker_inline_div1" ).val()) ) { $( "#timepicker_inline_div1" ).addClass( "ui-state-error" ); bValid = false; }
                    if ( ! $.datepicker.parseTime("H:m", $( "#timepicker_inline_div2" ).val()) ) { $( "#timepicker_inline_div2" ).addClass( "ui-state-error" ); bValid = false; }

//                    bValid = bValid && checkLength( "recname", "record name", 1, 255 );
//                    bValid = bValid && checkRegexp( "recname", /^(?!^(PRN|AUX|CLOCK\$|NUL|CON|COM\d|LPT\d|\..*)(\..+)?$)[^\x00-\x1f\\?*:\";|//]+$/, "No special chars in this field please" );
//                    bValid = bValid && checkLength( "channel", "channel", 1, 50 );
//                    bValid = bValid && checkLength( "datepicker_create", "date", 10, 10 );

//                    bValid = bValid && checkRegexp( "datepicker_create", /^((((0?[1-9]|[12]\d|3[01])[\.\-\/](0?[13578]|1[02])[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|((0?[1-9]|[12]\d|30)[\.\-\/](0?[13456789]|1[012])[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|((0?[1-9]|1\d|2[0-8])[\.\-\/]0?2[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|(29[\.\-\/]0?2[\.\-\/]((1[6-9]|[2-9]\d)?(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)|00)))|(((0[1-9]|[12]\d|3[01])(0[13578]|1[02])((1[6-9]|[2-9]\d)?\d{2}))|((0[1-9]|[12]\d|30)(0[13456789]|1[012])((1[6-9]|[2-9]\d)?\d{2}))|((0[1-9]|1\d|2[0-8])02((1[6-9]|[2-9]\d)?\d{2}))|(2902((1[6-9]|[2-9]\d)?(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)|00))))$/, "Please use DD.MM.YYYY for this field" );
//                    bValid = bValid && checkLength( "timepicker_inline_div1", "start time", 5, 5 );
//                    bValid = bValid && checkRegexp( "timepicker_inline_div1", /^(([0-1]?[0-9])|([2][0-3])):([0-5]?[0-9])(:([0-5]?[0-9]))?$/, "Please use HH:MM format for this field" );
//                    bValid = bValid && checkLength( "timepicker_inline_div2", "end time", 5, 5 );
//                    bValid = bValid && checkRegexp( "timepicker_inline_div2", /^(([0-1]?[0-9])|([2][0-3])):([0-5]?[0-9])(:([0-5]?[0-9]))?$/, "Please use HH:MM format for this field" );
                    var mask = 0;
                    for (var i=0; i<7; i++) {
                        if ( $("#wwd" + i).hasClass("ui-state-active") ) {
                            mask += Math.pow(2, i);
                        }
                    }
                    if ( bValid ) {
                        $( this ).dialog( "close" );
                        var akt = 0;
                        if ($("#switch_create").attr("checked") == "checked") akt = 1;
                        post("/create", {
                            rprev:$("#rprev").val(),
                            recname:$("#recname").val(),
                            Sender:$("#channel").val(),
                            von:$("#timepicker_inline_div1").val(),
                            bis:$("#timepicker_inline_div2").val(),
                            am:  $.datepicker.formatDate("yy-mm-dd", $("#datepicker_create").datepicker( "getDate" )),
                            aktiv:akt,
                            recurr:mask
                        },
                            here('list') ? 0 : ( here('epglist') ? 2 : 1 )
                        );
                    }
                }
            };

            if((dialognr!=-1 && !here('list') && !here('epglist'))) {
                $( this ).dialog( "option", "buttons", [deletebutton, updatebutton, cancelbutton] );
                $( this ).dialog( "option", "title", $( this ).attr("utitle"));

                oTable = $('#table_recordlist').dataTable();
                var data = oTable.fnGetData();
                var len = data.length;
                if (len>0) {
                    for(var i=0;i<len;i++) {
                        if(data[i][7]==dialognr) {

                            for(var j=0;j<7;j++) {
                                if ( (data[i][4] & Math.pow(2,j)) == Math.pow(2,j)) $("#wwd"+j).addClass("ui-state-active");
                            }

                            var kids = $("#channel").children();
                            for (var j=0;j<kids.length;j++) {
                                if (kids[j].innerHTML==data[i][1].replace(/<(?:.|\n)*?>/gm, '')) {
                                    $("#channel").val(kids[j].value);
                                    break;
                                }
                            }

                            switchMe("#switch_create", ($("#switch-" + dialognr).attr("checked") == "checked") );
                            $("#rprev").val(dialognr);
                            $("#recname").val(data[i][0]);
                            $("#timepicker_inline_div1").val(data[i][2].slice(11,16));
                            $("#timepicker_inline_div2").val(data[i][3].slice(11,16));
                            //$("#datepicker_create").val(data[i][2].slice(0,10)); //??
                            //$("#datepicker_create").datepicker( "setDate", mydatetime );
                            $("#datepicker_create").val( localDate(data[i][2]) );
                            break;
                        }
                    }
                }
            } else {
                $( this ).dialog( "option", "buttons", [updatebutton, cancelbutton] );
                $( this ).dialog( "option", "title", $( this ).attr("ctitle"));

                var today = new Date();
                var dd = today.getDate();
                var mm = today.getMonth()+1; //January is 0!
                var hr = today.getHours();
                var min = today.getMinutes();
                var yyyy = today.getFullYear();
                if(dd<10){dd='0'+dd;} if(mm<10){mm='0'+mm;} today = yyyy+'-'+mm+'-'+dd;
                //$("#datepicker_create").datepicker( "setDate", localDate(today) );
                $("#datepicker_create").val( localDate(today) );

                //console.log(localDate(today));

                if(hr<10){hr='0'+hr;} if(min<10){min='0'+min;} today = hr+':'+min;//+':00';
                $("#timepicker_inline_div1").val(today);
                today = new Date();
                hr = today.getHours() + 1;
                if(hr==24) {hr=0;} if(hr<10){hr='0'+hr;} today = hr+':'+min;
                $("#timepicker_inline_div2").val(today);

                switchMe("#switch_create", true);

                $("#channel").val(1);
                $("#rprev").val("");
                $("#recname").val("");

                if(here("list")) {
                    $("#channel").val(dialognr);
                    $("#recname").val(document.getElementById("channel").options[document.getElementById("channel").selectedIndex].innerHTML);
                }
            }

        },
        close: function() {
//            $( ".validateTips" ).html("");
            allFields.removeClass( "ui-state-error" );
        }
    });

    $( "#dialog_record_from_epg" ).dialog({
        autoOpen: false,
        modal: true,
        width: 600,
        buttons: [{
            text: $( "#dialog_record_from_epg" ).attr("record"),
            click: function() {
                $( this ).dialog( "close" );
                post("/createepg", { ret:$("#ret").val() }, 
                    here('epglist')?2:1 );
            }
        },
        {
            text: $( "#dialog_record_from_epg" ).attr("tunerecord"),
            click: function() {
                $( this ).dialog( "close" );
                $( "#dialog_create_record" ).dialog( "open" );

                //$("#prev").val(dialognr);
                $("#recname").val(recName);
                $("#timepicker_inline_div1").val(recStart);
                $("#timepicker_inline_div2").val(recEnd);

                if (recChannel<9999) {
                    $("#channel").val(recChannel);
                } else {
                    var kids = $("#channel").children();
                    for (var j=0;j<kids.length;j++) {
                        if (kids[j].innerHTML==recChannel) {
                            $("#channel").val(kids[j].value);
                            break;
                        }
                    }
                }
                $("#datepicker_create").val( localDate(recDate) );
            }
        },
        {
            text: $( "#dialog_record_from_epg" ).attr("cancel"),
            click: function() {
                $( this ).dialog( "close" );
            }
        }],
        close: function() {
            $("#dialog_content").html("");
        }
    });

    if (here("records")) {
// ------------------------------------ Records tab only
        $( "#button_create_record" )
        .button()
        .click(function() {
            dialognr = -1;
            $( "#dialog_create_record" ).dialog( "open" );
        });

        $( "#button_purge_records" )
        .button()
        .click(function() {
            $( "#dialog_purge" ).dialog( "open" );
        });

        $( "#dialog_purge" ).dialog({
            autoOpen: false,
            buttons: [{
                text: $( "#dialog_purge" ).attr("ok"),
                click: function() {
                    post(where(), { myid:'-1', what:"-2" }, 1);
                    $( this ).dialog( "close" );
                }
            },
            {
                text: $( "#dialog_purge" ).attr("cancel"),
                click: function() {
                    $( this ).dialog( "close" );
                }
            }]
        });



        $('#table_recordlist').dataTable({
            "oLanguage": {"sUrl": "lang/dataTables." + language + ".json"},
            "bJQueryUI": true,
            "sPaginationType": "full_numbers",
            "bProcessing": true,
            "bAutoWidth": false,
            "sAjaxSource": "/getrecordlist",
            "stateSave": true,
            "stateDuration": 60 * 60 * 60 * 24,
            "stateSaveCallback": function (oSettings, oData) {
                oData.search.search=''; // Don't save search text
                localStorage.setItem( 'DataTables_'+where(), JSON.stringify(oData) );
            },
            "stateLoadCallback": function (oSettings) {
                return JSON.parse( localStorage.getItem('DataTables_'+where()) );
            },
            "aoColumnDefs": [ { "bSearchable": false, "bVisible": false, "aTargets": [ 6,7,8,9 ] },
                              { "iDataSort": 8, "aTargets": [ 2 ] },
                              { "iDataSort": 9, "aTargets": [ 3 ] } ],
            "fnDrawCallback": function( oSettings ) {
                initSwitch();
                initIcons();
                initProgressbar();
                paintTable();
            },
            "fnRowCallback": function( nRow, aData, iDisplayIndex ) {
                $('td:eq(2)', nRow).html( localDateTime( aData[2] ) );
                $('td:eq(3)', nRow).html( localDateTime( aData[3] ) );
                var recurr="";
                if (aData[4] == 0) {
                    recurr = $('#table_recordlist').attr("recurr");
                } else {
                    for(var i=firstday; i<7+firstday; i++) {
                        var day = i>=7?i-7:i;
                        if ( (aData[4] & Math.pow(2,day)) == Math.pow(2,day)) recurr += weekdays[day];
                    }
                }
                $('td:eq(4)', nRow).html(recurr);
                var chk = "";
                if (aData[5] == 1) chk = 'checked="checked"';
                htmltext  = '<div id="progressbar' + aData[6] + '"></div>';
                htmltext += '<input type="checkbox" class="switch icons" id="switch-' + aData[7] + '" ' + chk + ' />';
                htmltext += '<a href="#" id="icons-' + aData[7] + '" class="ui-state-default ui-corner-all"><span class="ui-icon ui-icon-gear"></span></a>';
                $('td:eq(5)', nRow).html(htmltext);
            }

       });
    } else if (here("list")) {
// ------------------------------------ Channel list tab
        $( "#switch_list_active").slickswitch();
        $( "#switch_list_append").slickswitch();

        $( "#button_create_channel" )
        .button()
        .click(function(event ) {
            dialognr=-1;
            $( "#dialog_create_channel" ).dialog( "open" );
            event.preventDefault();
        });

        $( "#button_import_clist" )
        .button()
        .click(function(event ) {
            $( "#dialog_import_clist" ).dialog( "open" );
            event.preventDefault();
        });

        $( "#button_download_clist" )
        .button()
        .click(function(event ) {
            $.ajax({
                type: "POST",
                url: "/clgen",
                data: {},
                dataType: "json",
                success: function(data, textStatus) {
                    $( "#dialog_download_clist" ).dialog( "open" );
                }
            });
        });

        $( "#dialog_import_clist" ).dialog({
            autoOpen: false,
            modal: true,
            buttons: [{
                text: $( "#dialog_import_clist" ).attr("upload"),
                click: function() {
                    $( this ).dialog( "close" );
                    document.uploader.submit();
                }
            },
            {
                text: $("#dialog_import_clist").attr("cancel"),
                click: function() {
                    $( this ).dialog( "close" );
                }
            }]
        });

        $( "#dialog_download_clist" ).dialog({
            autoOpen: false,
            buttons: [{
                text: $( "#dialog_download_clist" ).attr("ok"),
                click: function() {
                    $( this ).dialog( "close" );
                }
            }]
        });

        $( "#dialog_create_channel" ).dialog({
            autoOpen: false,
            modal: true,
            width: 400,
            close: function() {
                $( ".validateTips" ).html("");
                allFields.val( "" ).removeClass( "ui-state-error" );
            },
            open: function( event, ui ) {

                var cancelbutton = {
                    text: $( this ).attr("cancel"), click: function() {
                        $( this ).dialog( "close" );
                    }
                };
                var updatebutton = {
                    text: (dialognr==-1?$( this ).attr("create"):$( this ).attr("update")), click: function()
                    {
                        var bValid = true;
                        allFields.removeClass( "ui-state-error" );
                        bValid = bValid & checkRegexp(  "ccid", /^[0-9]{1,5}$/, $(this).attr("errid") );
                        bValid = bValid & checkRegexp(  "cname", /^(?=\s*\S).*$/, $(this).attr("errname") );
                        bValid = bValid & checkRegexp(  "cpath", /^(?=\s*\S).*$/, $(this).attr("errurl") );
                        if (bValid) {
                            var akt = 0;
                            if ($("#switch_list_active").attr("checked") == "checked") {akt = 1;}

                            post("/create_channel", {
                                cprev: $("#cprev").val(),
                                ccid: $("#ccid").val(),
                                cname:$("#cname").val(),
                                cpath:$("#cpath").val(),
                                cext: $("#cext").val(),
                                aktiv:akt
                            }, 1);
                            $( this ).dialog( "close" );
                        }
                    }
                };
                var deletebutton = {
                    text: $( this ).attr("delete"), click: function()
                    {
                        $( this ).dialog( "close" );
                        $( "#dialog_remove" ).dialog( "open" );
                    }
                };

                if(dialognr!=-1) {
                    $( this ).dialog( "option", "buttons", [deletebutton, updatebutton, cancelbutton] );

                    oTable = $('#table_channellist').dataTable();
                    var data = oTable.fnGetData();
                    var len = data.length;
                    if (len>0) {
                        for(var i=0;i<len;i++) {
                            if(data[i][0]==dialognr) {

                                switchMe("#switch_list_active", ($("#switch-" + data[i][0]).attr("checked") == "checked") );

                                $("#cprev").val(data[i][0]);
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

                    switchMe("#switch_list_active", true );
                    $("#cprev").val("");
                    $("#ccid").val("1");
                    $("#cname").val("");
                    $("#cpath").val("");
                    $("#cext").val("");
                }

            }
        });

        $('#table_channellist').dataTable({
            "oLanguage": {"sUrl": "lang/dataTables." + language + ".json"},
            "bJQueryUI": true,
            "sPaginationType": "full_numbers",
            "bAutoWidth": false,
            "bProcessing": true,
            "sAjaxSource": "/channellist",
            "stateSave": true,
            "stateDuration": 60 * 60 * 60 * 24,
            "stateSaveCallback": function (oSettings, oData) {
                oData.search.search=''; // Don't save search text
                localStorage.setItem( 'DataTables_'+where(), JSON.stringify(oData) );
            },
            "stateLoadCallback": function (oSettings) {
                return JSON.parse(localStorage.getItem('DataTables_'+where()));
            },
            "fnDrawCallback": function( oSettings ) {
                initSwitch();
                initIcons();
                paintTable();
            },
            "fnRowCallback": function( nRow, aData, iDisplayIndex ) {
                $('td:eq(1)', nRow).html('<a href=\"live/'+aData[0]+'.m3u\">'+aData[1]+'</a>');
                var data4 = "";
                if (aData[4] == 1) data4 = "plus"; else data4="minus";
                var chk = "";
                if (aData[5] == 1) chk = 'checked="checked"';
                $('td:eq(4)', nRow).html('<input type="checkbox" class="switch icons" id="switch-' + aData[0] + '" ' + chk + ' /><label title="Create record" id="iconsRec-' + aData[0] + '" class="ui-state-default ui-corner-all"><span class="ui-icon ui-icon-play"></span></label><a href="#" id="icons-' + aData[0] + '" class="ui-state-default ui-corner-all"><span class="ui-icon ui-icon-gear"></span></a>');
            }
        });
   } else if (here("epgchart")) {
// ------------------------------------ EPG chart tab

        var zoom = $("#zoom_amount").attr("zoom");
        if (zoom==0) zoom=1;
        $( "#zoom_amount" ).val(Math.abs(zoom));
        var maxcnt=0;

        $( "#slider_zoom" ).slider({
            value: Math.abs(zoom),
            min: 1,
            max: 5,
            step: 0.2,
            slide: function( event, ui ) {
                $( "#zoom_amount" ).val( Math.abs(ui.value) );
            },
            stop: function( event, ui ) {
                var new_zoom = $( "#zoom_amount" ).val();
                if (zoom<0) {
                    zoom = -new_zoom;
                } else {
                    zoom = new_zoom;
                }
                post("setzoom", { zoom: zoom }, 1);
            }
        });

        $( "#flipepg" )
            .button()
            .click(function(event ) {
                post("setzoom", { zoom: -zoom }, 1);
                event.preventDefault();
            });

        $( "#date_prev, #date_next" )
            .button()
            .click(function(event ) {
                post("epg", { datepicker_epg: $.datepicker.formatDate("yy-mm-dd", $( "#datepicker_epg" ).datepicker( "getDate" ).addDays( $(this).is( $( "#date_prev" ) )?-1:1 ) ) }, 1);
                event.preventDefault();
            });

        $( "#datepicker_epg" ).datepicker({
            constrainInput: true,
            minDate: 0,
            defaultDate: 0,
            onSelect: function() {
                post("epg", { datepicker_epg: $.datepicker.formatDate("yy-mm-dd", $(this).datepicker( "getDate" )) }, 1);
            }
        });
        $( "#datepicker_epg" ).val( localDate( $( "#datepicker_epg" ).attr("dbvalue") ) );

        $( "[id^=event], [id=divider]" ).each(function(i) {
            w = +$(this).attr('width');
            x = +$(this).attr('x');
            cnt = +$(this).attr('cnt');
            rec = $(this).attr('recording');
            if(rec >= 0) $(this).css({"background":"#98FB98","color":"#000"}); // thx Pavol
            $(this).css("font-size", ((cnt==0?11:8)+Math.round(Math.abs(zoom*2))) + 'px');

            if (zoom>0) {
                $(this).css("height", cnt==0?'20px':'60px');
                $(this).css("margin-top", cnt==0?20:(20+(cnt-1)*100) + 'px');
                $(this).css("margin-left", x+'%');
                $(this).css("width", w+'%');
//                if (cnt==0) $(this).css("position", 'fixed');
            } else {
                $(this).css("left", cnt==0?0:((cnt-1) * 250 + 60) + 'px');
                $(this).css("top", x+'%');
                $(this).css("width", cnt==0?'50px':'240px');
                $(this).css("height", w + "%");
//                if (cnt==0) $(this).css("position", 'fixed');
            }
        });

        $( "[id^=epg_cname]" ).each(function(i) {
            cnt = +$(this).attr('cnt');
            if (cnt>maxcnt) maxcnt=cnt;
            if (zoom>0) {
                $(this).css("margin-top", (25+(cnt-1)*100) + 'px' );
            } else {
                $(this).css("width", cnt==0?'50px':'240px');
                $(this).css("margin-top", '-10px');
                $(this).css("margin-left", cnt==0?0:((cnt-1) * 250 + 60) + 'px');
                $(this).css("z-index", '1');
            }
        });

        if(!isNaN(zoom)) {
            if (zoom>0) {
                if(zoom!=1) {
                    $("body").css("width", (zoom*100)+"%");
                }
                $("#mybody").css("height", (maxcnt * 100 + 200) +"px");
                $("[id=channelgroup]").each(function(i) { $(this).css("clear", "left"); });
                $("[id=channelgroup][cnt=0]").css({"margin-top": "0px"});
                $("[id=channelgroup][cnt=0],#dividegroup").css({"width": ($("body").width()-42) + "px"}); // bad solution
                $("[id^=divider]").css("height", (maxcnt * 100) +"px");
                $("[id^=divider]").css("border-right-width", "1px");

                $(window).scroll(function() {epg_zoom_hor();}).resize(function() {epg_zoom_hor();});
            } else {
                $("[id=channelgroup],#dividegroup").each(function(i) {
                    $(this).css("float", "left");
                    $(this).css("height", (-zoom*800)+"px");
                });
                if (250*maxcnt+100<1200) {
                    $("body").css("width", "100%");
                } else {
                    $("body").css("width", (250*maxcnt+100)+"px");
                }
                $("#mybody").css("height", (-zoom*800+200)+"px");

                $("#dividegroup").css("margin-top", "20px");
                $("[id^=divider]").css("width", $("#mybody").width());
                $("[id^=divider]").css("border-bottom-width", "1px");
                $("[id^=divider]").css("box-sizing", "border-box");
                $("[id^=epg_cname]").css("margin-top", "0px");
                $("[id^=epg_cname]").addClass("ui-widget-header");
                $("[id^=epg_cname]").css("box-sizing", "border-box");

                $(window).scroll(function() {epg_zoom_vert();}).resize(function() {epg_zoom_vert();});

            }
        }

        $( "#searchepg" ).change(function(param) {
            var tofind = $(this).val().toLowerCase().trim();
            if(!param.hasOwnProperty("isTrigger")) {
                post("/setsearch", { search:tofind }, 0);
            }
            $( "[id=event]" ).each(function(i) {
                if ($(this).attr("cnt")!=="0") {
                    var text = $(this).text().toLowerCase() + " " + $(this).attr('fulltext').toLowerCase();
                    if(text.indexOf(tofind)!=-1 && tofind.length>0) {
                        $(this).addClass("ui-selected");
                    } else {
                        $(this).removeClass("ui-selected");
                    }
                }
            });
        });

        $( "#searchepgbutton" )
            .button()
            .click(function(event ) {
                event.preventDefault();
            });

        $("[id=event]").on("click", function(event) {
            if ($(this).attr("recording")>=0) { 
                dialognr = parseInt($(this).attr("recording"));
                $( "#dialog_remove" ).dialog( "open" );
            } else if ($(this).attr("cnt")!=="0") {

                var ft = "<b>" + $(this).text() + ": " + localDateTime($(this).attr("at")) + " - "
                       + localDateTime($(this).attr("till")) + "</b><BR><BR>" + $(this).attr("fulltext");
                ft = ft.replace(/\n/g, '<BR>');

                if (ft)  {
                    $("#ret").val($(this).attr("rid"));
                    $("#dialog_content").html ( ft );

                    recName = $(this).text();
                    recChannel = $(this).attr("cid");
                    recDate = $(this).attr("at").split(" ")[0];
                    var delta_before = $("#delta_before_epg").attr("delta");
                    var delta_after = $("#delta_after_epg").attr("delta");
                    recStart = new Date( parseDate($(this).attr("at")).valueOf() - delta_before*60000 ).toTimeString().substring(0, 5);
                    recEnd = new Date( parseDate($(this).attr("till")).valueOf() + delta_after*60000 ).toTimeString().substring(0, 5);
                    $( "#dialog_record_from_epg" ).dialog( "open" );
                }
            }
        });

        $( "#dialog_channel_disable" ).dialog({
            autoOpen: false,
            buttons: [{
                text: $( "#dialog_channel_disable" ).attr("disable"),
                click: function() {
                    post("list", { myid:dialognr, what:"0" }, 1);
                    $( this ).dialog( "close" );
                }
            },
            {
                text: $( "#dialog_channel_disable" ).attr("cancel"),
                click: function() {
                    $( this ).dialog( "close" );
                }
            }]
        });

        initIcons();
        initEpgState();
        
        var keyword_for_epg = $('#keyword_for_epg').attr('keyword_for_epg');
        if (keyword_for_epg!=="") {
            $( "#searchepg" ).val(keyword_for_epg);
            $( "#searchepg" ).change();            
        }
    } else if (here("epglist")) {
// ------------------------------------ EPG list tab only
        var serverSide = ($("#listmode").attr("value") == "1");

        $('#table_epglist').dataTable({
            "oLanguage": {"sUrl": "lang/dataTables." + language+ ".json"},
            "bJQueryUI": true,
            "sPaginationType": "full_numbers",
            "bProcessing": true,
            "bAutoWidth": false,
            "sAjaxSource": "/epglist_getter",
            "fnDrawCallback": function( oSettings ) {
                initIcons();
                paintTable();
            },
            "bServerSide": serverSide,
            "stateSave": true,
            "stateDuration": 60 * 60 * 60 * 24,
            "stateSaveCallback": function (oSettings, oData) {
                oData.search.search=''; // Don't save search text
                localStorage.setItem( 'DataTables_'+where(), JSON.stringify(oData) );
            },
            "stateLoadCallback": function (oSettings) {
                var oData = JSON.parse( localStorage.getItem('DataTables_'+where()) );
                var keyword_for_epg = $('#keyword_for_epg').attr('keyword_for_epg');
                if ( keyword_for_epg != '' ) {
                    oData.search.search=keyword_for_epg;
                }                
                return oData;
            },
            "fnRowCallback": function( nRow, aData, iDisplayIndex ) {
                $('td:eq(3)', nRow).html( localDateTime( aData[3] ) );
                $('td:eq(4)', nRow).html( localDateTime( aData[4] ) );
                if (aData[7]===null) { 
                    $('td:eq(5)', nRow).html('<label title="Create record" id="iconsERec-' + aData[6] + '" class="ui-state-default ui-corner-all"><span class="ui-icon ui-icon-play"></span></label>');
                } else {
                    $('td:eq(5)', nRow).html('<label title="Delete record" id="iconsEStop-' + aData[7] + '" class="ui-state-default ui-corner-all"><span class="ui-icon ui-icon-close"></span></label>');
                }
            }
        });
        
        initIcons();
        initEpgState();

    } else if (here("config")) {
// ------------------------------------ Configuration tab only
        var configdata = null;
        var passFields =  $( [] ).add( "#pass_old" ).add( "#pass_new_1" ).add( "#pass_new_2" );

        $( "#configtabs" ).tabs().addClass( "ui-tabs-vertical ui-helper-clearfix" );
        $( "#configtabs li" ).removeClass( "ui-corner-top" ).addClass( "ui-corner-left" );
        $("#cfg_purgedelta,#cfg_delta_before_epg,#cfg_delta_after_epg,#cfg_retry_count,#cfg_failsafe_delta,#cfg_xmltvtimeshift,#cfg_m3u_timer").spinner();
        $("#cfg_grab_zoom").spinner( { step: 0.1 } );
        $("#cfg_epg_max_events").spinner( { step: 1000 } );

        $("#cfg_switch_legacy").slickswitch();
        $("#cfg_switch_concurrent").slickswitch();
        $("#cfg_switch_epg_overlay").slickswitch();
        $("#cfg_switch_epglist_mode").slickswitch();
        $("#cfg_switch_xmltv_auto").slickswitch({
            toggledOn: function() {
                $("#cfg_xmltvinitpath").removeAttr("disabled");
                $("#cfg_xmltvinitpath").removeClass("ui-state-disabled");
                $("#cfg_xmltvtimeshift").removeAttr("disabled");
                $("#cfg_xmltvtimeshift").removeClass("ui-state-disabled");
                $("#cfg_xmltv_mc2xml").removeAttr("disabled");
                $("#cfg_xmltv_mc2xml").removeClass("ui-state-disabled");
            },
            toggledOff: function() {
                $("#cfg_xmltvinitpath").prop("disabled", "true");
                $("#cfg_xmltvinitpath").addClass("ui-state-disabled");
                $("#cfg_xmltvtimeshift").prop("disabled", "true");
                $("#cfg_xmltvtimeshift").addClass("ui-state-disabled");
                $("#cfg_xmltv_mc2xml").prop("disabled", "true");
                $("#cfg_xmltv_mc2xml").addClass("ui-state-disabled");
            }
        });
        $("#cfg_switch_postprocess").slickswitch({
            toggledOn: function() {
                $("#cfg_postprocess").removeAttr("disabled");
                $("#cfg_postprocess").removeClass("ui-state-disabled");
            },
            toggledOff: function() {
                $("#cfg_postprocess").prop("disabled", "true");
                $("#cfg_postprocess").addClass("ui-state-disabled");
            }
        });
        $("#cfg_switch_proxy").slickswitch({
            toggledOn: function() {
                $("#cfg_proxy").removeAttr("disabled");
                $("#cfg_proxy").removeClass("ui-state-disabled");
            },
            toggledOff: function() {
                $("#cfg_proxy").prop("disabled", "true");
                $("#cfg_proxy").addClass("ui-state-disabled");
            }
        });
        $("#cfg_dbpath").prop("disabled", "true");
        $("#cfg_dbpath").addClass("ui-state-disabled");
        if ($("#cfg_recordpath").prop("disabled")) {
            $("#cfg_recordpath").addClass("ui-state-disabled");
        }

        $.get( "/getconfig", function( data )  {
            var p = new Function('return ' + data + ';')();
            configdata = p.configdata;
            for (var i = 0; i < configdata.length; i++) {
                if (configdata[i][0].startsWith('cfg_switch')) {
                    switchMe( "#" + configdata[i][0], configdata[i][2]=='1');
                } else {
                    $("#" + configdata[i][0]).val(configdata[i][2]);
                }
            }
        });

        $( "#button_resetlog" )
        .button()
        .click(function(event ) {
            post("/resetlog", {}, 1);
            event.preventDefault();
        });

        $( "#button_setpass" )
        .button()
        .click(function(event ) {
            passFields.removeClass( "ui-state-error" );
            passFields.val("");
            $( "#dialog_password" ).dialog( "open" );
            event.preventDefault();
        });
        
        $( "#button_database" )
        .button()
        .click(function(event ) {            
            $('#input_dbpath').val($('#cfg_dbpath').val());
            $( "#dialog_database" ).dialog( "open" );
            event.preventDefault();
        });

        $( "#button_pathchooser" )
        .button()
        .click(function(event ) {
            $('#pathchooser').fileTree({ root: '/', script: '/gettree', multiFolder: false }, function(file) {});
            $( "#dialog_pathchooser" ).dialog( "open" );
            event.preventDefault();
        });

        $( "#button_removeepg" )
        .button()
        .click(function(event ) {
            $( "#dialog_remove" ).dialog( "open" );
            event.preventDefault();
        });

        $( "#submit_cfg" ).button().click(function(event ) {
            var my_config_data = new Array();
            var myalert = false;
            var reload = false;
            $("[id^=cfg_]").each(function() {
                var value = $(this).val();
                if ($(this).attr('id')=="cfg_server_port") {
                    var port = parseInt(value);
                    if (!checkRegexp("cfg_server_port", /^[0-9]{1,5}$/, "") || port<80 || isNaN(port) || port > 65535 ) {
                        alert( $(this).attr('alert') );
                        myalert = true;
                    }
                } else if ($(this).attr('id')=="cfg_server_bind_address") {
                    if ( value != "localhost") if ( !checkRegexp( "cfg_server_bind_address", /^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/, "" ) ) {
                        alert( $(this).attr('alert') );
                        myalert = true;
                    }
                } else if ($(this).attr('id')=="cfg_retry_count") {
                    if ( !checkRegexp( "cfg_retry_count", /^\d+$/, "" ) ) {
                        alert( $(this).attr('alert') );
                        myalert = true;
                    }
                } else if ($(this).attr('id')=="cfg_m3u_timer") {
                    if ( !checkRegexp( "cfg_m3u_timer", /^\d+$/, "" ) ) {
                        alert( $(this).attr('alert') );
                        myalert = true;
                    }
                } else if ($(this).attr('id')=="cfg_failsafe_delta") {
                    if ( !checkRegexp( "cfg_failsafe_delta", /^\d+$/, "" ) ) {
                        alert( $(this).attr('alert') );
                        myalert = true;
                    }
                } else if ($(this).attr('id')=="cfg_grab_time") {
                    if ( value.trim() != "0" ) if ( ! $.datepicker.parseTime("H:m", $( "#cfg_grab_time" ).val()) ) {
                        alert( $(this).attr('alert') );
                        myalert = true;
                    }
                /*} else if ($(this).attr('id')=="cfg_record_mask") {
                    if ( value.lastIndexOf("%date%")==-1 && value.lastIndexOf("%title%")==-1) {
                        alert( $(this).attr('alert') );
                        myalert = true;
                    }*/
                } else if ($(this).attr('id').startsWith('cfg_switch') && $(this).attr('type')!="checkbox") {
                    value = "null";
                } else if ($(this).attr('id').startsWith('cfg_switch')) {                    
                    value = ($(this).attr('checked')=="checked") ? "1" : "0";
                } else if ( // Reload page on this changes only 
                    ($(this).attr('id')=="cfg_theme") ||
                    ($(this).attr('id')=="cfg_language") ||
                    ($(this).attr('id')=="cfg_locale") 
                    ) {
                    for (var i = 0; i < configdata.length; i++) {
                        if ( configdata[i][0] == $(this).attr('id') ) {
                            if ( configdata[i][2] != value) reload = true;
                            break;
                        }
                    }
                }

                if(value != "null") my_config_data.push(new Array($(this).attr('id'), value));
            });

            if (!myalert) {
                var my_config_data_str = JSON.stringify(my_config_data);
                $("#label_config_saved").text($("#label_config_saved").attr("info"));
                $.post("/config",  {configdata:my_config_data_str}, function() {
                        $("#label_config_saved").text("");
                        if(reload) window.location.reload(false);
                    }, "json");
            }
        });

        $( "#dialog_password" ).dialog({
            autoOpen: false,
            buttons: [{
                text: $( "#dialog_password" ).attr("ok"),
                click: function() {
                    $.post("/setpass",
                        {
                            "pass_old": $("#pass_old").val(),
                            "pass_new_1": $("#pass_new_1").val(),
                            "pass_new_2": $("#pass_new_2").val()
                        },
                        function(data) {
                            ret = data.ret;
                            passFields.removeClass( "ui-state-error" );
                            if (ret == 0) {
                                $( "#dialog_password" ).dialog( "close" );
                                window.location.reload(false);
                            } else if (ret == 1) {
                                $( "#pass_old" ).addClass( "ui-state-error" );
                            } else {
                                $( "#pass_new_1" ).add( "#pass_new_2" ).addClass( "ui-state-error" );
                            }
                        }, "json");
                }
            },
            {
                text: $( "#dialog_password" ).attr("cancel"),
                click: function() {
                    $( this ).dialog( "close" );
                }
            }]
        });

        $( "#dialog_database" ).dialog({
            autoOpen: false,
            buttons: [{
                text: $( "#dialog_database" ).attr("ok"),
                click: function() {
                    $.post("/setdbpath",
                        {
                            "input_dbpath": $("#input_dbpath").val()
                        },
                        function(data) {
                            $( "#dialog_database" ).dialog( "close" );
                            window.location.reload(false);
                        }, "json");
                }
            },
            {
                text: $( "#dialog_database" ).attr("cancel"),
                click: function() {
                    $( this ).dialog( "close" );
                }
            }]
        });

        $( "#dialog_pathchooser" ).dialog({
            autoOpen: false,
            modal: true,
            width: 500,
            height: 500,
            buttons: [{
                text: $( "#dialog_pathchooser" ).attr("ok"),
                click: function() {
                    $('#cfg_recordpath').val($(".folderselected").attr("rel"));
                    $( this ).dialog( "close" );
                }
            },
            {
                text: $( "#dialog_pathchooser" ).attr("cancel"),
                click: function() {
                    $( this ).dialog( "close" );
                }
            }]
        });


    } else if (here("log")) {
// ------------------------------------ Log tab only
        $( "#downlog" )
        .button()
        .click(function(event ) {
            window.location = "./log.txt";
            event.preventDefault();
        });

        $('#table_loglist').dataTable({
            "oLanguage": {"sUrl": "lang/dataTables." + language + ".json"},
            "bJQueryUI": true,
            "sPaginationType": "full_numbers",
            "bAutoWidth": false,
            "bProcessing": true,
            "sAjaxSource": "/logget",
            "stateSave": true,
            "stateDuration": 60 * 60 * 60 * 24,
            "stateSaveCallback": function (oSettings, oData) {
                oData.search.search=''; // Don't save search text
                localStorage.setItem( 'DataTables_'+where(), JSON.stringify(oData) );
            },
            "stateLoadCallback": function (oSettings) {
                return JSON.parse( localStorage.getItem('DataTables_'+where()) );
            },
            "fnDrawCallback": function( oSettings ) {
                paintTable();
            }
        });
    }

    function localDate(sqldate) {
        var myday = $.datepicker.parseDate('yy-mm-dd', sqldate.substr(0,10));
        return $.datepicker.formatDate(mydateformat, myday);
    }
    function localTime(sqltime) {
        var mytime = $.datepicker.parseTime('HH:mm:ss', sqltime);
        return $.datepicker.formatTime(mytimeformat, mytime);
    }
    function localDateTime(sqldatetime) {
        return localDate(sqldatetime.substr(0,10)) + " " + localTime(sqldatetime.substr(11,19));
    }

});

function epg_zoom_hor() {
    if ($(window).scrollTop()>140) {
        $("[id=channelgroup][cnt=0]").css({"margin-top": ($(window).scrollTop()) -140 + "px"});
    } else {
        $("[id=channelgroup][cnt=0]").css({"margin-top": "0px"});
    }
    $("[id=channelgroup][cnt=0],#dividegroup").css({"width": ($("body").width()-42) + "px"});
    $("[id=epg_cname]").css({"margin-left": ($(window).scrollLeft()) });
}

function epg_zoom_vert() {
    $("[id=channelgroup][cnt=0]").css({"margin-left": ($(window).scrollLeft()) + "px"});
    $("#dividegroup").css({"height": ($("[id=channelgroup][cnt=0]").height()) + "px"});
    $("[id^=divider]").css("width", $("#mybody").width());
    if ($(window).scrollTop()>140) {
        $("[id=epg_cname]").css({"margin-top": ($(window).scrollTop()) - 140 + "px" });
    } else {
        $("[id=epg_cname]").css({"margin-top": "0px"});
    }
}
