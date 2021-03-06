#!/usr/bin/env python

import spotifier
import time
import provider_soma
import provider_wprb
import provider_wxdu
import provider_wxyc
import provider_skinny
import provider_doa
import provider_pitchfork
import provider_blackcat
import provider_dc9
import provider_rock_hotel
import provider_velvet
import provider_ustreet
import provider_comet
import provider_kexp
import provider_ohmyrockness
import provider_sxsw
import provider_catscradle

TEST = [
  provider_catscradle,
]

GENERAL = [
  provider_ohmyrockness,
#  provider_sxsw,
]

RADIO = [
  provider_kexp,
  provider_wxdu,
  provider_wxyc,
  provider_wprb,
  provider_soma,
]
SHOWS = [
#   provider_rock_hotel,
#   provider_blackcat,
provider_dc9,
provider_ustreet,
# #  provider_velvet,
#   provider_comet,
# #  provider_catscradle,
]
REVIEWS = [
  provider_pitchfork,
  # provider_doa,
  # provider_skinny,
]

PROVIDERS = set (
#  TEST +
#  GENERAL +
  # SHOWS +
  REVIEWS +
  RADIO +
  []
  )
spotifier.login_user_to_spotify()

for provider in PROVIDERS:
  playlist_name = provider.get_playlist_name()
  playlist_id = spotifier.get_playlist(playlist_name)

  if playlist_id == -1:
    print 'ERROR: COULD NOT FIND PLAYLIST "{}"'.format(playlist_name)
    continue
#  print "Found playlist", playlist_name, playlist_id, playlist

  existing_playlist_track_uris = spotifier.get_playlist_tracks(playlist_id)

  urls = provider.get_urls()
  for url in urls:
    songs, page_title = provider.parse_for_songs(url)
    # for all songs that already have URI defined, grab em
    song_provided_uris = [song['uri'] for song in songs if 'uri' in song]
    spotifier.add_tracks_to_playlist(song_provided_uris, playlist_id, existing_playlist_track_uris)
    existing_playlist_track_uris |= set(song_provided_uris)

    # for all songs that DON'T already have URIs
    songs_without_uris = [song for song in songs if 'uri' not in song]
    for song in songs_without_uris:
      artists = spotifier.fetch_artist(song['artist'])
      time.sleep(.5)
      artists = [artist for artist in artists if 'name' in artist and artist['name'].lower() == song['artist'].lower()]
      if len (artists) == 0:
        continue
      follows = spotifier.follows([artists[0]['id']])
      if follows[0]:
        time.sleep(1)
        print ('\tALREADY FOLLOWING {}').format (song['artist'])
#        songs_without_uris.remove(song)
    song_and_album_matches = spotifier.get_songs(songs_without_uris)
    song_matches = song_and_album_matches['matches']
    song_uris = [song['uri'] for song in song_matches]
    spotifier.add_tracks_to_playlist(song_uris, playlist_id, existing_playlist_track_uris)
    existing_playlist_track_uris |= set(song_uris)

