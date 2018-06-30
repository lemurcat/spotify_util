
import random
import pprint
import sys
import spotipy
import spotipy.util as util

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


scope = 'playlist-modify-public'

if len(sys.argv) > 2:
    username = sys.argv[1]
    other_name = sys.argv[2]
    shuffle = len(sys.argv) > 3 and sys.argv[3] != '0'
else:
    print("Usage: %s username playlist" % (sys.argv[0],))
    sys.exit()

token = util.prompt_for_user_token(username, scope)

g_playlists = {}

if token:
    sp = spotipy.Spotify(auth=token)
    me = sp.me()
    #print (me)

    playlists = sp.current_user_playlists(limit=50)
    for playlist in playlists['items']:
        # print(playlist['name'])
        # print(playlist['id'])
        if playlist['name'] in ('beebs', other_name):
            lst = []
            g_playlists[playlist['name']] = lst
            i = 0
            tracks = sp.user_playlist_tracks(me['id'],
                                             playlist_id = playlist['id'])
            while True:
                for track_wrap in tracks['items']:
                    i+=1
                    track = track_wrap['track']
                    print('  '+ str(i) + ' '+track['name'])
                    print('    Explicit: '+str(track['explicit']))
                    if (not FILTER_EXPLICIT) or (not track['explicit']):
                        lst.append((track['name'], track['id']))
                # Get next set of tracks, if there are still some to
                # retrieve.
                if tracks['next']:
                    tracks = sp.next(tracks)
                else:
                    break

    if len(g_playlists.keys()) == 2:
        for (k,v) in g_playlists.items():
            print(k)
            print(v)

    if shuffle:
        random.shuffle(g_playlists[other_name])

    new_tracks = interleave(g_playlists['beebs'], g_playlists[other_name])
    pprint.pprint(new_tracks)

    new_pl = sp.user_playlist_create(me['id'], 'merged '+other_name)
    pprint.pprint(new_pl)
    new_track_ids = [i[1] for i in new_tracks]
    
    num_tracks = len(new_track_ids)
    idx = 0
    while idx < num_tracks:
        # add 100 at a time
        sp.user_playlist_add_tracks(me['id'], new_pl['id'], 
                                    new_track_ids[idx:idx+100])
        idx += 100
    
else:
    print("Can't get token for", username)


# get_tracks_from_playlist
# create new playlist with new name
# add all tracks

def 

def copy_playlist(sp, user, src, dst):
    tracks = get_tracks_from_playlist(src)
    new_pl = sp.user_playlist_create(me['id'], dst)    
    new_track_ids = [i[1] for i in tracks]
    
    num_tracks = len(new_track_ids)
    idx = 0
    while idx < num_tracks:
        # add 100 at a time
        sp.user_playlist_add_tracks(me['id'], new_pl['id'], 
                                    new_track_ids[idx:idx+100])
        idx += 100
    

