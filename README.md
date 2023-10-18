# Twitch Background Mix Creator

A simple Python tool to create an offline audio mix from a YouTube playlist. Designed for Twitch streamers to have a background music mix without requiring online streaming or using excessive resources.

## Features

- Download songs from a YouTube playlist using `yt-dlp`.
- Crossfade songs to create a seamless audio mix.
- Produce a single mixed audio file for easy playback during streams.
- Flexibility to specify crossfade duration.
- Option to retain individual songs or just the final mix.
- Automated setup and execution using a `.bat` file.

## Usage

1. Clone or download this repository.
2. Run the `run.bat` file. This will:
    - Check for a virtual environment in the `.venv` directory.
    - Create the virtual environment if it doesn't exist.
    - Install the required packages from `requirements.txt`.
    - Execute the main script.
3. Follow the on-screen prompts:
    - Provide a YouTube playlist URL to download songs.
    - Specify your desired crossfade length.
    - Decide if you want to keep the individual downloaded songs or just the mixed track.

## Requirements

- Python 3.x
- `yt-dlp` for downloading songs from YouTube.
- `pydub` for audio processing and mixing.
- `tqdm` for displaying progress bars.

## Contribution

Feel free to fork, improve, make pull requests or fill issues. I'd be happy to get feedback or provide help if needed.

## License

This project is open-source. Feel free to use, modify, distribute, and enjoy!

## Disclaimer

Please ensure you have the right to download and use the music from YouTube. I am not responsible for DMCAs.
