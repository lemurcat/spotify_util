
import sys
import spotipy
import spotipy.util
import util
import pprint

def clear_and_get_playlist(sp, user, playlist_name):
    pl = util.get_playlist_by_name(sp, playlist_name)
    if not pl:
        pl = sp.user_playlist_create(user['id'], playlist_name)    
    else:
        util.delete_all_tracks(sp, user, pl)
    return pl

def update_recent(sp, user):
    print('clearing Recent')
    recent_pl = clear_and_get_playlist(sp, user, 'Recent')
    print('clearing Recent to listen')
    recent_to_listen_pl = clear_and_get_playlist(sp, user, 'Recent to listen')
    print('clearing Recent saved')
    recent_saved_pl = clear_and_get_playlist(sp, user, 'Recent saved')

    print('getting recent tracks from to listen')
    to_listen = util.get_playlist_by_name(sp, 'to listen')
    to_l_trks = util.track_infos_to_tracks(
        util.get_recently_added_track_infos(sp,
                                            user,
                                            to_listen,
                                            60))

    print('getting recent saved tracks')
    saved_trks = util.track_infos_to_tracks(
        util.get_recently_added_track_infos_from_saved(sp,
                                            user,
                                            60))

    print('adding to Recent to listen')
    util.add_tracks_to_playlist(sp, user, recent_to_listen_pl, to_l_trks)
    print('adding to Recent saved')
    util.add_tracks_to_playlist(sp, user, recent_saved_pl, saved_trks)

    # take union of the two
    all_recent_trks = list(set([tr['id'] for tr in (saved_trks + to_l_trks)]))
    print('adding to Recent')
    util.add_tracks_to_playlist(sp, user, recent_pl, all_recent_trks)
    
    
def main():
    scope = 'playlist-modify-public user-library-read'

    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username playlist" % (sys.argv[0],))
        sys.exit(1)

    token = spotipy.util.prompt_for_user_token(username, scope)
    if not token:
        print('Failed to get token')
        sys.exit(2)

    sp = spotipy.Spotify(auth=token)
    me = sp.me()

    update_recent(sp, me)
    
if __name__ == "__main__":
    main()
