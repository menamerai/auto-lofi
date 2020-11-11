from lofigen import LofiSynthesize

try:
    audio = LofiSynthesize("./main.mp3")
    audio.treat_audio("lofied", sound_amplification=9, music_path={
        "melody": "Lofi-Samples/Lofi/Melody Loops/looperman-l-1890396-0121725-mondlichtrecords-lofi-sample-85-bpm.wav",
        "drums": "Lofi-Samples/Lofi/Drums Loops/Cymatics - Lofi Full Drum Loop 9 - 85 BPM.wav",
        "ambience": "Lofi-Samples/Ambience/Crackle-Old-Tape-White-Noise-D-www.fesliyanstudios.com.mp3"
    })
except:
    print("Please add audio file in.")