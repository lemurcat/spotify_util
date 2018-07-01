
import random
import pprint
import sys
import spotipy
import spotipy.util as util
import util

FILTER_EXPLICIT = True

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

    util.merge_playlists(sp, me, 'beebs', other_name, FILTER_EXPLICIT, shuffle)
    
if __name__ == "__main__":
    main()
