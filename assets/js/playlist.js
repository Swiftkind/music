
  //ajax for adding songs
  $(document).on('submit', '#songForm' , function( event ){
    event.preventDefault();
    $('#songFormError').addClass('hidden');

    // submit new song on the playlist
    var data = $(this).serialize();
    $('#id_link').val('');
    $.ajax({
      method: 'POST',
      url: $(this).attr('action'),
      data: data
    }).done(function(response){
      // add videoID to player
      song_ids.push(response.link);
      // get id for song-state 
      var id = song_ids.length;
      // songEntry will be used to append on the songlist
      songEntry = '<li id="song-state-'+ id +'" class="">'
                    + '<div class="media" id="'+ response.id +'">'
                    + '<div class="media-left media-middle">'
                    + '<img class="media-object" src="'+ response.thumb_url +'">'
                    + '</div>'
                    + '<div class="media-body">'
                    +  '<h4 class="media-heading">'+ response.title +'</h4>'
                    + 'Duration: '+ response.duration +''
                    + '<br>'
                    + 'By:'+ response.user +''
                    + '<br>'
                    + '<a href="' 
                    + response.edit_url + '">Edit</a>'
                    + '<form method="post" class="deleteSong" action="'
                    + response.delete_url + '" class="deleteSong">'
                    + '<button type="submit">Delete</button>'
                    + '</form></div>'
                    + '</div></li>';
      $('#songlist').append(songEntry);
    }).fail(function(error){
      if(error.status === 400){
        $('#songFormError').removeClass('hidden');
      }
    });
  });

  $(document).on('submit', '#search_playlist', function(event){
    event.preventDefault();
    if ($(this).find('input#id_keyword').val()=="" )
      alert("Empty Fields!")
    $.ajax({
      type: 'POST',
      url: $(this).attr('action-url'),
      data: $(this).serialize()
    }).done(function(response){
      $('#playlists').html(response);
    });
  });

  $(document).on('click', '#all_playlist', function(event){
    event.preventDefault(); 
    $.ajax({
      type: 'Get',
      url: $(this).attr('url'),
      data: $(this).serialize()
    }).done(function(response){
      $('#playlists').html(response);
    });
  });

  // ajax for deleting songs
  $(document).on('submit', '.deleteSong', function( event ){
    event.preventDefault();
    $.ajax({
      method: 'POST',
      url: $(this).attr('action'),
      data: $(this).serialize()
    }).done(function(response){
      //remove song from the template
      $("#"+response.song_id).parent( "li" ).remove()
      song_ids.pop();
    });
  });

  // add playlist
  $(document).on('click', '#btn-add', function(event){
    event.preventDefault();
    var form = $('#add_playlist').serialize();
    var csrftoken = Cookies.get('csrftoken');

    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });

    $.ajax({
      method: 'post',
      url: $(this).attr('url'),
      data: form
    }).done(function(response){

     var request_user = $('div#playlists').attr('request-user');

     var append_request_user = '<button type="button" id="btn-edit-playlist" class="btn btn-info btn-lg">Edit</button>'
                               +'<button type="submit" id="btn-update-playlist" style="display:none;" class="btn btn-info">Update</button>'
                               +'<button type="submit" id="btn-cancel" style="display:none;" class="btn btn-info">Cancel</button>'
                               +'<form  method="post" csrfmiddlewaretoken="'+csrftoken+'" action="/music/api/playlist/delete/'+response.id+'/"  class="deletePlaylist">'
                                  +'<button type="submit">Delete</button>'
                               +'</form>';

     var playlist_tpl = '<div class="panel panel-default" id="'+response.id+'">'
                          +'<div class="panel-heading">'
                            +'<h3>'+ response.title +'</h3>'
                          +'</div>'
                          +'<div class="panel-body">'
                            +'<div class="col-md-6">'
                              +'<div class="row">'
                                  +'<img class="img-responsive" src="'+ response.get_thumb_url +'" width="120px" height="90px">'
                              +'</div>'
                            +'</div>'
                            +'<div class="col-md-6">'
                             +'<hr class="visible-sm visible-xs">'
                              +'<p>0 songs</p>'
                              +'<p>by <strong>'+ response.user_email +'</strong></p>'
                              +'<a id="'+response.id+'" class="btn btn-primary" href="/music/playlist/'+ response.id +'/">View Playlist</a>';
               
      if(request_user==response.user_email){
        playlist_tpl = playlist_tpl + append_request_user;
      }
      var playlist_tpl_append = '</div>'
                               +'</div>'
                               +'</div>';

      var playlist_tpl = playlist_tpl + playlist_tpl_append; 
      $('#playlists').append(playlist_tpl);
      $('#add_playlist')[0].reset();
    }).fail(function(response){
      alert("Something went wrong!")
    });
  });


  // deleting Playlist
  $(document).on('submit', 'form.deletePlaylist', function( event ){
    event.preventDefault();
    $.ajax({
      method: 'POST',
      url: $(this).attr('action'),
      data: $(this).serialize(),
      context: $(this)
    }).done(function(response){
      //remove playlist from the template
      $(this).closest("div.panel").remove();
    });
  });

  //edit playlist
  $(document).on('click', 'button#btn-edit-playlist', function(event){
    event.preventDefault();
    var text_title = $(this).closest('div.panel').find('h3').text();
    var id_title = $(this).closest('div.panel').attr('id');
    var csrftoken = Cookies.get('csrftoken');

    $(this).closest('div.panel').css('border-color','coral');
    $(this).closest('div.panel').find('h3').hide();
    $(this).closest('div.panel').find('button#btn-edit-playlist').hide();
    $(this).closest('div.panel').find('button#btn-update-playlist').show();
    $(this).closest('div.panel').find('button#btn-cancel').show();

    $(this).closest('div.panel').find('div.panel-heading').append(
                    '<form method="post" csrfmiddlewaretoken="'+csrftoken+'" class="update_playlist"  action="/music/api/playlist/update/'+id_title+'/'+'" > '
                   +'<input type="text" class="form-control" id="title" name="title" value="'+text_title+'" >'
                   +'</form>'        
    ) ;

  });

  //cancel playlist
  $(document).on('click', 'button#btn-cancel', function(event){
    event.preventDefault();

    $(this).closest('div.panel').css('border-color','#ddd');
    $(this).closest('div.panel').find('button#btn-edit-playlist').show();
    $(this).closest('div.panel').find('button#btn-update-playlist').hide();
    $(this).hide()
    $('form.update_playlist').remove();
    $(this).closest('div.panel').find('h3').show();
    
  });

  //update playlist
  $(document).on('click', 'button#btn-update-playlist', function(event){
    event.preventDefault();

    var csrftoken = Cookies.get('csrftoken');
    var form = $('form.update_playlist').serialize();

    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });
         
    $.ajax({
      type: 'post',
      url: $('form.update_playlist').attr('action'),
      data: form,
      context: $(this),
     
    }).done(function(response){
      $('form.update_playlist').remove();
      $(this).closest('div.panel').css('border-color','#ddd');
      $(this).closest('div.panel').find('button#btn-edit-playlist').show();
      $(this).closest('div.panel').find('button#btn-cancel').hide();
      $(this).closest('div.panel').find('h3').remove();
      $(this).closest('div.panel').find('div.panel-heading').append(
                    '<h3>'+ response.title +'</h3>'
      );
      $(this).hide()

    });

  });