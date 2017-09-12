$( document ).ready(function() {

/*
Date Picker for Add events
*/

    $('.datestart').datepicker({
        format: 'mm/dd/yyyy',
        startDate: '-3d'
    });
    $('.dateend').datepicker({
        format: 'mm/dd/yyyy',
        startDate: '-3d'
    });
});

/*
Date Picker for Add events
*/

/*
Show comment on Post
*/
    function ShowComment(related_id){

        var proper_url = "{% url 'getcomments' 789 %}".replace("789", parseInt(related_id));
        $.get( proper_url, function( data ) {
            var post_path = "#comments" + related_id ;
            var print = "";
            var i = 0;
            for(;i<data.length;i++) {
                var proper_url_user = "{% url 'userprofile' 999 %}".replace("999", data[i].user__id);
                print += "<div class='panel panel-default'><div class='panel-body'>" +  data[i].comment+"<br><a href='"+proper_url_user+"'>"+ data[i].user__username +"</a></div></div>";
            }
            if (i<1)
                $(post_path ).html("There are no existing comments.");
            else
                $( post_path ).html( print );
        });
    }
/*
Show comment per Post
*/

/* Autocomplete Message Send To */
        
    //populate users
    var user_autocomplete_data = [];
    var user_autocomplete_data_id = [];
    $.get( "{% url 'getusers' %}", function( data ) {
        for(i = 0;i<data.length;i++){
            user_autocomplete_data.push(data[i].username);
            user_autocomplete_data_id.push(data[i].id);
        }
    });

    //change value of the input field
    $( "#message_user_autocomplete" ).autocomplete({
      source: user_autocomplete_data,
      select: function(event, ui) {
        var index = $.inArray(ui.item.value, user_autocomplete_data);
        $('#to_user').val(user_autocomplete_data_id[index]);
        }
    });

    //change value of the input field
    $( "#event_user_autocomplete" ).autocomplete({
      source: user_autocomplete_data,
      select: function(event, ui) {
        var index = $.inArray(ui.item.value, user_autocomplete_data);
        $('#event_user_autocomplete_val').val(user_autocomplete_data_id[index]);
        }
    });

/* Autocomplete Message Send To */
    $.get( "{% url 'getusers' %}", function( data ) {
        for(i = 0;i<data.length;i++){
            user_autocomplete_data.push(data[i].username);
            user_autocomplete_data_id.push(data[i].id);
        }
    });


/* Add More Topics */
    // add multiple fields

var topics = 0;
    
    //populate topics
    $( "#id_topic" ).addClass( "topic_autocomplete" );
    var topic_autocomplete_data = [];

    $.get( "{% url 'gettopics' %}", function( data ) {
        for(i = 0;i<data.length;i++){
            topic_autocomplete_data.push(data[i].topic);
        }
    });

    //put topics to fields
    $( ".topic_autocomplete" ).autocomplete({
      source: topic_autocomplete_data
    });
    $( ".topic_autocomplete" ).autocomplete("option", "appendTo", ".form");


    function AddPostTopicFieldPost(){
        topics++;
        $("#topic_look").append("<span style = 'border-style: solid;margin-left:3px;' >"+$("#id_topic").val() + "</span>");
        var prev_topics =  $("#more_topic_container").val();
        if(topics != 0)
            var new_topics = prev_topics +","+ $("#id_topic").val();
        else
            var new_topics = $("#id_topic").val();
        $("#more_topic_container").val(new_topics);
        console.log($("#more_topic_container").val(new_topics));
        $( ".topic_autocomplete" ).autocomplete({
          source: topic_autocomplete_data
        });
        $( ".topic_autocomplete" ).autocomplete("option", "appendTo", ".form");
    }

/* Add More Topics */

/*  Populate Notification with Unseen Stuff  */

setInterval(function(){
    var insert_into_notification_list = "";
    var noti_count  = 0;

//For Post Notification

    $.get( "{% url 'getunseen_posts' %}", function( data ) {
        for(i = 0;i<data.length;i++){
            var post_id = data[i].post__id;
            var proper_post_url = "{% url 'post' 123 %}".replace("123", post_id);
            insert_into_notification_list += "<li><a href='"+ proper_post_url +"'> Post: <span style = 'font-weight: bold;'>"+data[i].post__title+"</span> has a new update.</a> </li>";
            noti_count++;
        }
    });

//For Event Notification
    
    $.get( "{% url 'getunseen_events' %}", function( data ) {
        for(i = 0;i<data.length;i++){
            var event_id = data[i].event__id;
            var proper_event_url = "{% url 'event' 234 %}".replace("234", event_id);
            insert_into_notification_list += "<li><a href='"+ proper_event_url +"'> Event: <span style = 'font-weight: bold;'>"+data[i].event__title+"</span> has a new update.</a> </li>";
            noti_count++;
        }
    if(insert_into_notification_list != "")
        $("#notification_list").html(insert_into_notification_list);
    else
        $("#notification_list").html("<div class = 'fluid-container'> Nothing New</div>");

    if (noti_count != 0)
        $("#noti_count").html("<span class='badge' style = 'background-color: #FF4500;'>"+noti_count+"</span>");
    });

},15000)

/*  Populate Notification with Unseen Stuff  */
