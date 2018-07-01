
import random
import pprint
import sys
import spotipy
import spotipy.util as util
import copy

FILTER_EXPLICIT = True

def interleave(lst1, lst2):
    len1 = len(lst1)
    len2 = len(lst2)
    longest_len = max(len1, len2)
    if len1 == 0:
        return list(lst2)
    if len2 == 0:
        return list(lst1)

    res = []
    for i in range(longest_len):
        res.append(lst1[i%len1])
        res.append(lst2[i%len2])
    return res

#print interleave([1,2,3,4,5,6,7,8],[11,12])
#print interleave([11,12], [1,2,3,4,5,6,7,8])

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

    src_pl1 = copy.get_playlist_by_name(sp, 'beebs')
    src_tracks1 = copy.get_tracks_from_playlist(sp, me, src_pl1)

    src_pl2 = copy.get_playlist_by_name(sp, other_name)
    src_tracks2 = copy.get_tracks_from_playlist(sp, me, src_pl2)
    src_tracks2 = [track for track in src_tracks2 if ((not FILTER_EXPLICIT)
                                                      or (not
                                                          track['explicit']))]
    if shuffle:
        random.shuffle(src_tracks2)

    merged_list = interleave(src_tracks1, src_tracks2)
    new_pl = sp.user_playlist_create(me['id'], 'merged '+other_name)
    copy.add_tracks_to_playlist(sp, me, new_pl, merged_list)
    
if __name__ == "__main__":
    main()
