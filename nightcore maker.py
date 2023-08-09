# EN MI MENTE ESTAS COMO UNA ADICCION
import os 
import unicodedata
from os import path
from pydub import AudioSegment
import numpy as np
from moviepy.editor import AudioFileClip, ImageClip

# Insert directory path
mp3_dir = r'mp3'
wav_dir = r'wav'
mp3_list = []
wav_list = []
nightcore_dir = r'nightcore temple'
song_info = {}
nightcore_magic_number = 0.3
imgs_dir = r'imgs'
used_imgs_dir = r'used imgs'
mp4_dir = r'mp4'

#Creates a dictionary of the songnames and artists ('songname' : 'artist')
for raw in os.listdir():
    if raw.endswith('.mp3'):
        raw = str(raw)
        artist = raw.split(" - ")[0]
        songname = raw.split(" - ")[1]
        songname = songname[:-4]
        song_info[songname] = artist

# mp3 to wav converter (List creator)
for file in os.listdir():
    if file.endswith('.mp3'):
        name = str(file)
        mp3_list.append(name)

#mp3 to wav converter (conversion)
for i in range(len(mp3_list)):
    mp3_name = mp3_list[i]
    song = AudioSegment.from_mp3(mp3_name)
    wav_name =mp3_name[:-3] + 'wav'
    song.export(wav_name, format = 'wav')

#creates a list of all wav output files
for file in os.listdir(mp3_dir):
    if file.endswith('.wav'):
        name = str(file)
        wav_list.append(name)

#put songs into each folder
for mp3 in os.listdir():
    if mp3.endswith('.mp3'):
        os.replace(mp3, mp3_dir + '\\' + mp3)
        
for wav in os.listdir():
    if wav.endswith('.wav'):
        os.replace(wav, wav_dir + '\\' + wav)

#Calling the wizard to do the magic
for file in os.listdir(r'wav'):
    if file.endswith('.wav'):
        filename = wav_dir + '\\' + file
        sound = AudioSegment.from_file(filename, format=filename[-3:])
        new_sample_rate = int(sound.frame_rate * (2.0 ** nightcore_magic_number))
        pitched = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        pitched = pitched.set_frame_rate(44100)
        pitched.export(file[:-4] + "_Nightcore.wav", format="wav")

#Put the output song into the nightcore temple
for nc in os.listdir():
    if nc.endswith('.wav'):
        os.replace(nc, nightcore_dir + '\\' + nc)

#Now its time to create a video and put the used imgs into the used imgs folder to prevent reusing them
for file in os.listdir(nightcore_dir):
    working_song = file
    working_img = os.listdir(imgs_dir)[0]
    audio_c = AudioFileClip(nightcore_dir + '\\' + working_song)
    image_c = ImageClip(imgs_dir + '\\' + working_img)
    video_c = image_c.set_audio(audio_c)
    video_c.duration = audio_c.duration
    video_c.fps = 30
    video_c.write_videofile(working_song[:-4] + '.mp4')
    os.replace(imgs_dir + '\\' + working_img, used_imgs_dir + '\\' + working_img)

    #Now put the videos into the mp4 folder
    for vid in os.listdir():
        if vid.endswith('.mp4'):
            os.replace(vid, mp4_dir + '\\' + vid)
