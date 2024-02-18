import pygame
import requests
from io import BytesIO
import json
import random
from moviepy.editor import *
import os
import multiprocess

# Initialize pygame
pygame.init()

# Set up the screen
screen_width = 1024
screen_height = 576
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shitty VGMV")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load font
font = pygame.font.Font(None, 36)

# Function to display text
def display_text(text, x, y):
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

# Function to load image from URL
def load_image_from_url(url):
    response = requests.get(url)
    image = pygame.image.load(BytesIO(response.content))
    return image

# Function to play music
def play_music(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    
# Function to download YouTube video
def download_video(url, output_path):
    from pytube import YouTube
    yt = YouTube(url)
    stream = yt.streams.filter().first()
    stream.download(filename=video_output_path)

def getSurface(clip, t, srf=None):
    frame = clip.get_frame(t=t)  # t is the time in seconds
    
    if srf is None:
        # Transpose the array and create the Pygame surface
        return pygame.surfarray.make_surface(frame.swapaxes(0, 1))
    else:
        pygame.surfarray.blit_array(srf, frame.swapaxes(0, 1))
        srf = pygame.transform.scale(srf, (screen_width / 1.3, screen_height / 1.3))
        return srf
    

def play_audio(video_file):
    from moviepy.editor import VideoFileClip, preview
    
    videoclip = VideoFileClip(video_file)
    videoclip.volumex(0.2)
    
    audioclip = videoclip.audio

    audioclip.preview()
    
show_image = False
show_text = False
stop = False

# Function to play video using Pygame
def play_video(video_file, ALLSONGS, display=True):
    videoclip = VideoFileClip(video_file)
    videoclip.volumex(0.5)
    videoclip = videoclip.resize(newsize=(screen_width,screen_height))
    
    audioclip = videoclip.audio
    audio_thread = multiprocess.Process(target=play_audio, args=(video_file,))
    audio_thread.start()
    
    surface = getSurface(videoclip, 0)
    screen = pygame.display.set_mode(surface.get_size(), 0, 32)
    
    Img = False
    Txt = False
    running = True
    t = 0
    text_to_display = ""
    while running:
        screen.fill(WHITE)

        if Img:
            screen.blit(getSurface(videoclip, t, surface), (100, 100))
        if Txt:
            display_text(text_to_display, 20, 20)


        pygame.display.flip() 
        t += 1/60 # use actual fps here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN: #next song!
                    audio_thread.terminate()
                    Img = False
                    Txt = False
                    running = False
                if event.key == pygame.K_UP: #show image/song
                    text_to_display = ALLSONGS[i]['title']
                    
                    Img = True
                    Txt = True
                if event.key == pygame.K_s: #stop
                    audio_thread.terminate()

                    return True
    return False


                    
if __name__ == "__main__":
    # Main loop
    running = True

    image_url = "https://example.com/image.png"
    text_to_display = "Hello, Pygame!"

    video_output_path = "video.mp4"  # Save video in the current directory


    file_path = 'videos.json' 
    ALLSONGS = []

    with open(file_path, 'r') as file:
        ALLSONGS = json.load(file)
    random.shuffle(ALLSONGS)
    i = 0
    screen.fill(WHITE)

    download_video(ALLSONGS[i]['url'], video_output_path)
    stop = play_video(video_output_path, ALLSONGS, display=False)

    while running:
        screen.fill(WHITE)
        print(stop)
        if(stop):
            running = False
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        i+=1
        download_video(ALLSONGS[i]['url'], video_output_path)
        stop = play_video(video_output_path, ALLSONGS, display=False)


    pygame.quit()
