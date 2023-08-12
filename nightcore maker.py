# EN MI MENTE ESTAS COMO UNA ADICCION
import os 
import unicodedata
from os import path
from pydub import AudioSegment
import numpy as np
from moviepy.editor import AudioFileClip, ImageClip
import sys

# Insert directory path
mp3_dir = r'mp3ss'
wav_dir = r'wav'
mp3_list = []
wav_list = []
nightcore_dir = r'nightcore temple'
song_info = {}
nightcore_magic_number = 0.35
imgs_dir = r'imgs'
used_imgs_dir = r'used imgs'
mp4_dir = r'mp4'

#Enviorment check for new users
def env_check():
    mp4f, mp3f, wavf, nightcoref = 0, 0, 0, 0
    for file in os.listdir():
        if file == 'mp3ss':
            mp3f = 1
        elif file == 'mp4':
            mp4f = 1
        elif file == 'wav':
            wavf = 1
        elif file == 'nightcore temple':
            nightcoref = 1
    
    if mp3f == 0:
        os.mkdir('mp3ss')
        mp3f = 1
    if mp4f == 0:
        os.mkdir('mp4')
        mp4f = 1
    if wavf == 0:
        os.mkdir('wav')
        wavf = 1
    if nightcoref == 0:
        os.mkdir('nightcore temple')
        nightcoref = 1
    
    total = mp3f + mp4f + wavf + nightcoref

    if total == 4:
        print('Enviorment is ready :)')

env_check()  #Optional

#Creates a dictionary of the songnames and artists ('songname' : 'artist')
try:
    for raw in os.listdir():
        if raw.endswith('.mp3'):
            raw = str(raw)
            artist = raw.split(" - ")[0]
            songname = raw.split(" - ")[1]
            songname = songname[:-4]
            song_info[songname] = artist
except:
    print('One or more songs does not meet the name requirments to create a dictionary of songname and artist')   

# mp3 to wav converter
for mp3 in os.listdir():
    if mp3.endswith('.mp3'):
        print('Converting ' + mp3 + ' to wav...')
        song = AudioSegment.from_mp3(mp3)
        song.export(mp3[:-4] + '.wav', format = 'wav')
        print('Done!')

#Calling the wizard to do the magic
for file in os.listdir():
    if file.endswith('.wav') and file.endswith('Nightcore.wav') == False:
        print('The wizard is fixing ' + file[:-4])
        sound = AudioSegment.from_file(file, format=file[-3:])
        new_sample_rate = int(sound.frame_rate * (2.0 ** nightcore_magic_number))
        pitched = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        pitched = pitched.set_frame_rate(44100)
        pitched.export(file[:-4] + "_Nightcore.wav", format="wav")
        print('The wizard made it!')

#Now its time to create a video and put the used imgs into the used imgs folder to prevent reusing them
for nightcore_song in os.listdir():
    if nightcore_song.endswith('Nightcore.wav'):
        audio_c = AudioFileClip(nightcore_song)
        image_c = ImageClip(imgs_dir + '\\' + os.listdir(imgs_dir)[0])
        video_c = image_c.set_audio(audio_c)
        video_c.duration = audio_c.duration
        video_c.fps = 30
        video_c.write_videofile(nightcore_song[:-4] + '.mp4')
        os.replace(imgs_dir + '\\' + os.listdir(imgs_dir)[0], used_imgs_dir + '\\' + os.listdir(imgs_dir)[0])

#Final sorter
for item in os.listdir():
    if item.endswith('Nightcore.wav'):
        os.replace(item, nightcore_dir + '\\' + item)
    elif item.endswith('.mp4'):
        os.replace(item, mp4_dir + '\\' + item)
    elif item.endswith('.wav'):
        os.replace(item, wav_dir + '\\' + item)
    elif item.endswith('mp3'):
        os.replace(item, mp3_dir + '\\' + item)