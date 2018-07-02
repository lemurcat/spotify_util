import spotipy
import spotipy.util as util
import random
import datetime
import pprint

# Get the first playlist of the current user with a matching name.
# If two playlists have the matching name, it may not return the
# one you expect.
def get_playlist_by_name(sp, name):
    playlists = sp.current_user_playlists(limit=50)
    while True:
        for playlist in playlists['items']:
            if playlist['name'] == name:
                return playlist

        if not playlists['next']:
            break
        playlists = sp.next(playlists)
    return None


# playlist = a playlist object
def get_tracks_from_playlist(sp, me, playlist):
    lst = get_track_info_from_playlist(sp, me, playlist)
    return track_infos_to_tracks(lst)


def get_track_info_from_saved(sp):
    lst = []
    tracks = sp.current_user_saved_tracks()
    while True:
        lst.extend(tracks['items'])
        if not tracks['next']:
            break
        tracks = sp.next(tracks)
    return lst


# playlist = a playlist object
def get_track_info_from_playlist(sp, me, playlist):
    lst = []
    tracks = sp.user_playlist_tracks(me['id'],
                                     playlist_id = playlist['id'])
    while True:
        lst.extend(tracks['items'])
        # Get next set of tracks, if there are still some to
        # retrieve.
        if not tracks['next']:
            break
        tracks = sp.next(tracks)
    return lst

def track_infos_to_tracks(track_infos):
    return [track_info['track'] for track_info in track_infos]    

def remove_old_track_infos(track_infos, num_of_days):
    threshold = datetime.datetime.today() - datetime.timedelta(num_of_days)
    threshold_str = threshold.isoformat()
    lst = [ti for ti in track_infos if threshold_str < ti['added_at']]
    return lst
    
def get_recently_added_track_infos(sp, me, playlist, num_of_days):
    track_infos = get_track_info_from_playlist(sp, me, playlist)
    return remove_old_track_infos(track_infos, num_of_days)

def get_recently_added_track_infos_from_saved(sp, me, num_of_days):
    track_infos = get_track_info_from_saved(sp)
    return remove_old_track_infos(track_infos, num_of_days)

def add_tracks_to_playlist(sp, user, new_pl, tracks):
    if len(tracks) == 0:
        return
    # get track ids if that's not what was given
    if isinstance(tracks[0], dict):
        new_track_ids = [i['id'] for i in tracks]
    else:
        new_track_ids = tracks
        
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

    
def delete_all_tracks(sp, user, playlist):
    tracks = get_tracks_from_playlist(sp, user, playlist)
    track_ids = [track['id'] for track in tracks]
    pprint.pprint(playlist['id'])
    pprint.pprint(track_ids)
    if len(track_ids) > 0:
        i = 0
        while i < len(track_ids): 
            sp.user_playlist_remove_all_occurrences_of_tracks(user['id'],
                                                              playlist['id'],
                                                              track_ids[i:
                                                                        i+100])
            i += 100
