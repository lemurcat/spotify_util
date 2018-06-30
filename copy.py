
import sys
import spotipy
import spotipy.util


# Get the first playlist of the current user with a matching name.
# If two playlists have the matching name, it may not return the
# one you expect.
# Only checks the first 50 playlists.
def get_playlist_by_name(sp, name):
    playlists = sp.current_user_playlists(limit=50)
    for playlist in playlists['items']:
        if playlist['name'] == name:
            return playlist
    return None

def get_tracks_from_playlist(sp, me, playlist):
    lst = []
    i = 0
    tracks = sp.user_playlist_tracks(me['id'],
                                     playlist_id = playlist['id'])
    while True:
        for track_wrap in tracks['items']:
            i+=1
            track = track_wrap['track']
            lst.append(track)
        # Get next set of tracks, if there are still some to
        # retrieve.
        if tracks['next']:
            tracks = sp.next(tracks)
        else:
            break
    return lst
        
def add_tracks_to_playlist(sp, user, new_pl, tracks):
    new_track_ids = [i['id'] for i in tracks]
    
    num_tracks = len(new_track_ids)
    idx = 0
    while idx < num_tracks:
        # add 100 at a time
        sp.user_playlist_add_tracks(user['id'], new_pl['id'], 
                                    new_track_ids[idx:idx+100])
        idx += 100


def copy_playlist(sp, user, src, dst):
    tracks = get_tracks_from_playlist(sp, user, src)
    new_pl = sp.user_playlist_create(user['id'], dst)    
    add_tracks_to_playlist(sp, user, new_pl, tracks)
    

def main():
    scope = 'playlist-modify-public'

    if len(sys.argv) > 2:
        username = sys.argv[1]
        other_name = sys.argv[2]
        shuffle = len(sys.argv) > 3 and sys.argv[3] != '0'
    else:
        print("Usage: %s username playlist" % (sys.argv[0],))
        sys.exit(1)

    token = spotipy.util.prompt_for_user_token(username, scope)
    if not token:
        print('Failed to get token')
        sys.exit(2)

    sp = spotipy.Spotify(auth=token)
    me = sp.me()

    src_list = get_playlist_by_name(sp, other_name)
    copy_playlist(sp, me, src_list, 'Backup')
    
if __name__ == "__main__":
    main()
