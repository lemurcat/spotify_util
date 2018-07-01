import spotipy
import spotipy.util as util
import random
 
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

def merge_playlists(sp, user, name1, name2, filter_explicit, shuffle):
    src_pl1 = get_playlist_by_name(sp, name1)
    src_tracks1 = get_tracks_from_playlist(sp, user, src_pl1)

    src_pl2 = get_playlist_by_name(sp, name2)
    src_tracks2 = get_tracks_from_playlist(sp, user, src_pl2)
    src_tracks2 = [track for track in src_tracks2 if ((not filter_explicit)
                                                      or (not
                                                          track['explicit']))]
    if shuffle:
        random.shuffle(src_tracks2)

    merged_list = interleave(src_tracks1, src_tracks2)
    new_pl = sp.user_playlist_create(user['id'], 'merged '+name2)
    add_tracks_to_playlist(sp, user, new_pl, merged_list)
