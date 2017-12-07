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

  $(document).on('click', '#btn-add', function(event){
    event.preventDefault();
    var form = $('#add_playlist').serialize();
    $.post({
      url: $(this).attr('url'),
      data: form
    }).done(function(response){

     var playlist_tpl = '<div class="panel panel-default">'
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

                              +'<a class="btn btn-primary" href="/music/playlist/'+ response.id +'/">View Playlist</a>'
                            +'</div>'
                          +'</div>'
                        +'</div>';
      $('#playlists').append(playlist_tpl);
      $('#add_playlist')[0].reset();
    }).fail(function(response){
      alert("Something went wrong!")
    });
  });
