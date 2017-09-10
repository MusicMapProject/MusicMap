from pydub import AudioSegment

def mp3toWav(path_music):
    sound = AudioSegment.from_mp3(path_music)
    sound.export(path_music + ".wav", format="wav")
    return path_music + ".wav"