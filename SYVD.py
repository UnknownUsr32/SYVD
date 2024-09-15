from pytubefix import YouTube
import os
from moviepy.editor import VideoFileClip, AudioFileClip
import time

def download_streams(youtube_obj, output_path, filename):
    video_stream = youtube_obj.streams.filter(adaptive=True, only_video=True).order_by('resolution').desc()
    audio_stream = youtube_obj.streams.filter(adaptive=True, only_audio=True).order_by('abr').desc().first()

    seen_resolution = {}
    unique_video_stream = []
    for stream in video_stream:
        if stream.resolution not in seen_resolution:
            seen_resolution[stream.resolution] = True
            unique_video_stream.append(stream)

    print("Available Resolutions: ")
    for i, stream in enumerate(unique_video_stream):
        print(f"{i+1}. {stream.resolution}")

    q3 = int(input("Choose the resolution number: ")) - 1
    if q3 < 0 or q3 >= len(unique_video_stream):
        print("Invalid selection")
        return None, None, None

    video_stream = video_stream[q3]
    if video_stream and audio_stream:

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
    input('Press enter to continue...')


def Download(link, output_path, filename):
    youtubeObj = YouTube(link)
    choose = input("Only Audio?(y/N) ").strip().lower()

    try:
        if choose.lower() == 'y':
            print("Fetching audio stream...")
            stream = youtubeObj.streams.filter(only_audio=True).order_by('abr').desc().first()
            print("Downloading audio...")
            out_file = stream.download(output_path=output_path, filename=filename)

            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            print("Audio file downloaded!")
        else:
            q2 = '''Choose download mode:
1.Adaptive Mode(High Quality,Resource Heavy)
2.Progressive Mode(Terrible Quality,Faster)'''
            print(q2)
            selection = input("===>").strip().lower()
            if selection == '1':
                print('Fetching video stream...')
                video_path, audio_path, output_path = download_streams(youtubeObj, output_path, filename)
                merge(video_path, audio_path, output_path)
            elif selection == '2':
                print('Fetching video stream...')
                video_stream = youtubeObj.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
                seen_resolution = {}
                unique_video_stream = []
                for stream in video_stream:
                    if stream.resolution not in seen_resolution:
                        seen_resolution[stream.resolution] = True
                        unique_video_stream.append(stream)

                print("Available Resolutions: ")
                for i, stream in enumerate(unique_video_stream):
                    print(f"{i + 1}. {stream.resolution}")

                q3 = int(input("Choose the resolution number: ")) - 1
                if q3 < 0 or q3 >= len(unique_video_stream):
                    print("Invalid selection")
                    return None, None, None

                video_stream = video_stream[q3]
                if video_stream:
                    print('Downloading video...')
                    video_stream.download(output_path=output_path, filename=filename + '.mp4')
                    print("Video downloaded!")
            else:
                print('Invalid input!')
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
    clear = lambda: print('\033c', end='', flush=True)
    t1 = '       Simple Youtube Video Downloader'
    t2 = '                By Unknown_32'

    try:
        clear()
        print(ascii)
        print(f'{bold}{t1}{reset}')
        print(f'{bold}{t2}{reset}')
        while True:

            link = input("Enter YouTube URL: ").strip()
            if not link:
                print("URL cannot be empty")
            else:
                break
        validation = YouTube(link)
        clear()
        print(ascii)
        while True:
            path = input("Enter path to which the downloaded file will be saved(Press enter to save on current directory): ").strip()
            if not path:
                path = os.getcwd()
                break

            if not os.path.isdir(path):
                print("Path is not a directory")
                continue

            if not os.path.exists(path):
                create_dir = input("Path does not exist, do you want to create it?(y/n)").strip().lower()
                if create_dir == 'y':
                    os.makedirs(path)
                else:
                    print("Exiting...")
                    return

            if not check_path_access(path):
                time.sleep(1)
                pass
            else:
                break

        clear()
        print(ascii)
        while True:

            name = input("Enter output name(Press enter for default name): ").strip().replace(' ', '_').replace('.mp4',
                                                                                                                '')
            if not name:
                name = validation.title.strip().replace(' ', '_')

            if os.path.isfile(os.path.join(path, name + '.mp4')):
                print("File already exists")
                time.sleep(1.5)
                print('''
1.Replace
2.Rename
3.Exit''')
                Action = input('===>')
                if Action == '1':
                    os.remove(os.path.join(path, name + '.mp4'))
                elif Action == '2':
                    continue
                elif Action == '3':
                    print("Exiting...")
                    return
                else:
                    print('Invalid input')
            break
        clear()
        print(ascii)
        Download(link, path, name)
    except KeyboardInterrupt as a:
        print(f'\nProcess interrupted by user. Exiting...{a}')

if __name__ == '__main__':
    main()
