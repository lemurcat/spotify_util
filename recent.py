
import sys
import spotipy
import spotipy.util
import util
import pprint

def main():
    scope = 'playlist-modify-public'

    if len(sys.argv) > 2:
        username = sys.argv[1]
        other_name = sys.argv[2]
    else:
        print("Usage: %s username playlist" % (sys.argv[0],))
        sys.exit(1)

    token = spotipy.util.prompt_for_user_token(username, scope)
    if not token:
        print('Failed to get token')
        sys.exit(2)

    sp = spotipy.Spotify(auth=token)
    me = sp.me()

    pl = util.get_playlist_by_name(sp, other_name)
    if not pl:
        print('playlist not found:'+ other_name)
        sys.exit(3)
    tis = util.get_recently_added_track_infos(sp, me, pl, 30)
    for ti in tis:
        print ti['track']['name']
    
if __name__ == "__main__":
    main()
