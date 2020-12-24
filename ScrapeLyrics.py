import pandas as pd
import time
import lyricsgenius

client_access_token = 'enter your client access token that you just generated'
genius = lyricsgenius.Genius(client_access_token, remove_section_headers=True,
                             skip_non_songs=True, excluded_terms=["Remix", "Live", "Edit", "Mix", "Club"])

# Create list of sample artists
sample_artists = ['J. Cole']
# you can also add multiple artists by separating with a comma:
# sample_artists = ['J. Cole', 'Drake', 'Kendrick Lamar', 'Lil Wayne', 'Nicki Minaj']

# Starting the song search for the artists in question and seconds count
query_number = 0
time1 = time.time()
# Empty list for dataframes to be created
tracks = []
for artist in sample_artists:
    query_number += 1
    # Empty lists for artist, title, album and lyrics information
    artists = []
    titles = []
    albums = []
    years = []
    lyrics = []
    print('\nQuery number:', query_number)
    # Search for max_songs = n and sort them by popularity
    artist = genius.search_artist(artist, max_songs=10, sort='popularity')
    songs = artist.songs
    song_number = 0
    # Append all information for each song in the previously created lists
    for song in songs:
        if song is not None:
            song_number += 1
            print('\nSong number:', song_number)
            print('\nNow adding: Artist')
            artists.append(song.artist)
            print('Now adding: Title')
            titles.append(song.title)
            print('Now adding: Album')
            albums.append(song.album)
            print('Now adding: Year')
            years.append(song.year[0:4])
            print('Now adding: Lyrics')
            lyrics.append(song.lyrics)
    # Create a dataframe for each song's information and add it to the tracks lists
    df = pd.DataFrame({'artist': artists, 'title': titles, 'album': albums, 'year': years, 'lyrics': lyrics})
    tracks.append(df)
    time2 = time.time()
    print('\nQuery', query_number, 'finished in', round(time2 - time1, 2), 'seconds.')
time3 = time.time()
# Concatenate our tracks in the final tracklist
tracklist = pd.concat(tracks, ignore_index=True)
print('\nFinal tracklist of', query_number, 'artists finished in', round(time3 + time2, 2), 'seconds.')
# Save the final tracklist to csv format
tracklist.to_csv('lyricsrealcoleworld.csv', encoding='utf-8', index=False)
