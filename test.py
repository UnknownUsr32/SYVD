from pytube import YouTube
import os
from moviepy.editor import VideoFileClip, AudioFileClip

def download_streams(youtube_obj, output_path, filename):
    video_stream = youtube_obj.streams.filter(adaptive=True, only_video=True).order_by('resolution').desc().first()
    audio_stream = youtube_obj.streams.filter(adaptive=True, only_audio=True).order_by('abr').desc().first()
    if not filename:
        filename = video_stream.title
        filename.strip().replace(" ", "_")

    video_path = os.path.join(output_path, f"{filename}_video.mp4")
    audio_path = os.path.join(output_path, f"{filename}_audio.mp4")

    video_stream.download(output_path=output_path, filename=f"{filename}_video.mp4")
    audio_stream.download(output_path=output_path, filename=f"{filename}_audio.mp4")

    return video_path, audio_path, os.path.join(output_path, f"{filename}.mp4")

def merge(video_path, audio_path, output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

    os.remove(video_path)
    os.remove(audio_path)
    print("Video downloaded and merged!")

def Download(link, output_path, filename):
    youtubeObj = YouTube(link)
    choose = input("Only Audio?(y/N) ").strip().lower()

    try:
        if choose.lower() == 'y':
            print("Fetching audio stream...")
            stream = youtubeObj.streams.filter(only_audio=True).first()
            print("Downloading audio...")
            out_file = stream.download(output_path=output_path, filename=filename)

            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            print("Audio file downloaded!")
        else:
            q2 = '''Choose download mode:
    1.Adaptive Mode(Recommended,REQUIRES FFMPEG!)
    2.Progressive Mode(Terrible quality)'''
            print(q2)
            selection = input("===>").strip().lower()
            if selection == '1':
                print('Fetching highest resolution video stream...')
                video_path, audio_path, output_path = download_streams(youtubeObj, output_path, filename)
                merge(video_path, audio_path, output_path)
            elif selection == '2':
                print('Fetching highest resolution video stream...')
                video_stream = youtubeObj.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                if video_stream:
                    print('Downloading video...')
                    video_stream.download(output_path=output_path, filename=filename)
                    print("Video downloaded!")
            else:
                print('Invalid selection!')
                return

    except Exception as e:
        print(f'Error downloading video: {e}')

def check_path_access(path):
    if not os.access(path, os.R_OK):
        print("Access denied")
        return False
    return True

def main():
    ascii = r'''
      .--.--.                              ,---,     
     /  /    '.      ,---,       ,---.  .'  .' `\   
    |  :  /`. /     /_ ./|      /__./|,---.'     \  
    ;  |  |--`,---, |  ' : ,---.;  ; ||   |  .`\  | 
    |  :  ;_ /___/ \.  : |/___/ \  | |:   : |  '  | 
     \  \    `.  \  \ ,' '\   ;  \ ' ||   ' '  ;  : 
      `----.   \  ;  `  ,' \   \  \: |'   | ;  .  | 
      __ \  \  |\  \    '   ;   \  ' .|   | :  |  ' 
     /  /`--'  / '  \   |    \   \   ''   : | /  ;  
    '--'.     /   \  ;  ;     \   `  ;|   | '` ,/   
      `--'---'     :  \  \     :   \ |;   :  .'     
                    \  ' ;      '---" |   ,.'       
                     `--`             '---'  '''
    bold = '\033[1m'
    reset = '\033[0m'
    t1 = "       Simple Youtube Video Downloader"
    t2 = "                By Unknown_32"
    print(ascii)
    print(f'{bold}{t1}{reset}')
    print(f'{bold}{t2}{reset}')
    try:
        link = input("Enter YouTube URL: ").strip()
        if not link:
            print("URL cannot be empty")
            return
        path = input("Enter path to which the downloaded file will be saved(Press enter to save on current directory): ").strip()
        if not path:
            path = os.getcwd()
        if not os.path.isdir(path):
            print("Path is not a directory")
            return
        if not os.path.exists(path):
            create_dir = input("Path does not exist, do you want to create it?(y/n)").strip().lower()
            if create_dir == 'y':
                os.makedirs(path)
            else:
                print("Exiting....")
                return

        if not check_path_access(path):
            return

        name = input("Enter output name(Press enter for default name): ")
        if not name:
            name = None

        Download(link, path, name)
    except KeyboardInterrupt as a:
        print(f'\nProcess interrupted by user. Exiting...{a}')

if __name__ == '__main__':
    main()
