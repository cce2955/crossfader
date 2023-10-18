import os
from pydub import AudioSegment
from tqdm import tqdm

def download_songs_from_url(playlist_url):
    os.system(f'yt-dlp -f bestaudio -x --audio-format mp3 "{playlist_url}" -o "downloaded_songs/%(playlist_index)s. %(title)s.%(ext)s"')

# Ensure the directory exists before downloading songs
if not os.path.exists('downloaded_songs'):
    os.makedirs('downloaded_songs')

# Check for existing songs on startup
if os.listdir('downloaded_songs'):
    print("Existing songs detected.")
    choice = input("Enter 'url/u' to provide a new playlist URL, 'process/p' to process existing songs without downloading, or 'delete/d' to remove existing songs: ").lower()
    
    if choice in ['url', 'u']:
        playlist_url = input("Please enter the YouTube playlist URL: ")
        download_songs_from_url(playlist_url)
    elif choice in ['delete', 'd']:
        for file in os.listdir('downloaded_songs'):
            os.remove(f"downloaded_songs/{file}")
        exit()
    elif choice not in ['process', 'p']:
        print("Invalid option.")
        exit()
else:
    playlist_url = input("Please enter the YouTube playlist URL: ")
    download_songs_from_url(playlist_url)

# Load and Crossfade Songs
songs = sorted(os.listdir("downloaded_songs/"), key=lambda x: int(x.split(".")[0]))  # Sort songs based on their playlist index
final_audio = AudioSegment.empty()

print("Processing songs...")
for i in tqdm(range(len(songs) - 1), desc="Crossfading songs", unit="song"):
    song1 = AudioSegment.from_mp3(f"downloaded_songs/{songs[i]}")
    song2 = AudioSegment.from_mp3(f"downloaded_songs/{songs[i+1]}")
    
    end_song1 = song1[-6000:]
    start_song2 = song2[:6000]
    crossfaded_segment = end_song1.append(start_song2, crossfade=6000)

    # Concatenate song1 without the last 6 seconds, then the crossfaded segment
    final_audio += song1[:-6000] + crossfaded_segment

# After all songs have been crossfaded, append the last song in its entirety
final_audio += song2

# Saving the final mix
print("\nSaving final mix. This may take a while...")
final_audio.export("final_crossfaded_mix.mp3", format="mp3")
print("Final mix saved as 'final_crossfaded_mix.mp3'.")

# After downloading, ask the user about song retention
choice = input("Do you want to keep the individual songs (songs/s) or just the mix (mix/m)?: ").lower()
if choice in ['mix', 'm']:
    for file in os.listdir('downloaded_songs'):
        os.remove(f"downloaded_songs/{file}")
