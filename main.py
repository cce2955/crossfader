import os
import subprocess
import re
from pydub import AudioSegment
from tqdm import tqdm

def download_songs_from_url(playlist_url):
    os.system(f'yt-dlp -f bestaudio -x --audio-format mp3 "{playlist_url}" -o "downloaded_songs/%(playlist_index)s. %(title)s.%(ext)s"')

def get_playlist_name(playlist_url):
    result = subprocess.run(['yt-dlp', '--yes-playlist', '--get-title', playlist_url], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8').strip().split('\n')[0]

def sanitize_filename(filename):
    s = re.sub(r'[\\/*?:"<>|]', "", filename)
    return s[:250]

def main():
    if not os.path.exists('downloaded_songs'):
        os.makedirs('downloaded_songs')

    if os.listdir('downloaded_songs'):
        print("Existing songs detected.")
        choice = input("Enter 'url/u' to provide a new playlist URL, 'process/p' to process existing songs without downloading, 'append/a' to append a new playlist to the existing songs, or 'delete/d' to remove existing songs: ").lower()
        
        if choice in ['url', 'u']:
            playlist_url = input("Please enter the YouTube playlist URL: ")
            download_songs_from_url(playlist_url)
        elif choice in ['delete', 'd']:
            for file in os.listdir('downloaded_songs'):
                os.remove(f"downloaded_songs/{file}")
            return
        elif choice in ['append', 'a']:
            playlist_url = input("Please enter the YouTube playlist URL to append: ")
            download_songs_from_url(playlist_url)
        elif choice not in ['process', 'p']:
            print("Invalid option.")
            exit()
    else:
        playlist_url = input("Please enter the YouTube playlist URL: ")
        download_songs_from_url(playlist_url)

    try:
        crossfade_length_seconds = float(input("Please enter the desired crossfade length in seconds (e.g., 6 for 6 seconds): "))
        crossfade_length_milliseconds = int(crossfade_length_seconds * 1000)
    except ValueError:
        print("Invalid input. Using default crossfade length of 6 seconds.")
        crossfade_length_milliseconds = 6000

    songs = sorted(os.listdir("downloaded_songs/"), key=lambda x: int(x.split(".")[0]))
    final_audio = AudioSegment.empty()

    print("Processing songs...")
    for i in tqdm(range(len(songs) - 1), desc="Crossfading songs", unit="song"):
        song1 = AudioSegment.from_mp3(f"downloaded_songs/{songs[i]}")
        song2 = AudioSegment.from_mp3(f"downloaded_songs/{songs[i+1]}")

        end_song1 = song1[-crossfade_length_milliseconds:]
        start_song2 = song2[:crossfade_length_milliseconds]
        crossfaded_segment = end_song1.append(start_song2, crossfade=crossfade_length_milliseconds)

        # Add song1 without the crossfade portion
        final_audio += song1[:-crossfade_length_milliseconds]

        # Add the crossfaded segment
        final_audio += crossfaded_segment

        # After the crossfade, the next song should start from where the crossfade ended
        song2 = song2[crossfade_length_milliseconds:]

        # Add the rest of song2
        final_audio += song2

    playlist_name = "Default_Mix_Name"
    if 'playlist_url' in locals():
        playlist_name = sanitize_filename(get_playlist_name(playlist_url))
    output_filename = f"{playlist_name}.mp3"
    print(f"\nSaving final mix as {output_filename}. This may take a while...")
    final_audio.export(output_filename, format="mp3")
    print(f"Final mix saved as '{output_filename}'.")

    choice = input("Do you want to keep the individual songs (songs/s) or just the mix (mix/m)?: ").lower()
    if choice in ['mix', 'm']:
        for file in os.listdir('downloaded_songs'):
            os.remove(f"downloaded_songs/{file}")

while True:
    main()
    
    rerun_choice = input("Do you want to run the process again? (yes/y or no/n): ").lower()
    if rerun_choice not in ['yes', 'y']:
        break
