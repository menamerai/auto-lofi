from lofigen import LofiSynthesize

try:
    audio = LofiSynthesize("./main.mp3")
    audio.treat_audio("lofied", sound_amplification=8)
except:
    print("Please add audio file in.")