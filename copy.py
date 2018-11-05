
import sys
import spotipy
import spotipy.util
import util
    

def main():
    scope = 'playlist-modify-public'

    if len(sys.argv) > 3:
        username = sys.argv[1]
        other_name = sys.argv[2]
        backup_name = sys.argv[3]
    else:
        print("Usage: %s username playlist new_playlist" % (sys.argv[0],))
        sys.exit(1)

    token = spotipy.util.prompt_for_user_token(username, scope)
    if not token:
        print('Failed to get token')
        sys.exit(2)

    sp = spotipy.Spotify(auth=token)
    me = sp.me()

    src_list = util.get_playlist_by_name(sp, other_name)
    util.copy_playlist(sp, me, src_list, backup_name)
    
if __name__ == "__main__":
    main()
