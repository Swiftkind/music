/*  Ajax Create Playlist and it's form validation */
$(document).on('submit','#CreatePlaylist', function(event){
      event.preventDefault();
          $.ajax({
            method: 'POST',
            url:create_playlist_url,
            data: $(this).serialize()
          }).done(function(response){
            //Check if there is a form returned from the JsonResponse
            if (response.form == null){
               APPEND_TO_PLAYLISTS = "<li><a href ='" + response.view_url + "'>"
                         +response.title+"</a><br><small>"
                         +"<a href ='"+response.edit_url+"'>Edit</a>"
                         +"</small>|<small> <a href = '"+response.delete_url+"'"
                         +">Delete</a></small></li>";
              $("#PlayLists").prepend(APPEND_TO_PLAYLISTS);
              }
            else
            // tells the users what the form error is
            $("#playlist_add_error").html(response.form[0]);
      }).fail(function(error, x){
                // validate form errors
                if(error.status === 400) {
                    $('#playlist_add_error').append(error.responseJSON.title[0]);
        }
    });
});
/*  Ajax Create Playlist and it's form validation */
