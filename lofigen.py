from pydub import AudioSegment
from os import listdir
from os.path import join, isfile
import random


class LofiSynthesize:

    def __init__(self, filepath, format="mp3"):
        self.filepath = filepath
        print("Loading audio...")
        if format == "mp3":
            self.audio = AudioSegment.from_mp3(filepath)
        elif format == "wav":
            self.audio = AudioSegment.from_wav(filepath)
        else: 
            print("Audio not supported. Please use .mp3 or .wav")
            raise ValueError
        print("Audio loaded.")
        self.lofi_samples = {
            "drums": "Lofi-Samples/Lofi/Drums Loops/",
            "melody": "Lofi-Samples/Lofi/Melody Loops/",
            "ambience": "Lofi-Samples/Ambience/"
        }
        self.lofied = AudioSegment.empty()

    def randomize_lofi(self):
        print("=" * 15)
        print("Randomizing lofi samples...")
        lofi_samples = self.lofi_samples
        dict_keys = list(lofi_samples.keys())
        for i in range(len(dict_keys)):
            rel_dir = lofi_samples[dict_keys[i]]
            try:
                files = [f for f in listdir(rel_dir) if isfile(join(rel_dir, f))]
                choice = random.randint(0, len(files) - 1)
                lofi_samples[dict_keys[i]] += files[choice]
                print("Chosen {choice} for {aspect}.".format(
                    choice=files[choice], aspect=dict_keys[i]))
            except Exception as err:
                print("Error whilst randomizing effects. Please check the folders for correct hierachy.")
                print("It should be:")
                print("Lofi-Samples\n\tAmbience\n\tLofi\n\t\tDrums Loops\n\t\tMelody Loops")
                print(err)
        print("Ramdomization completed.")
        return lofi_samples

    def treat_audio(self, output_name, fade_duration=3, sound_amplification=1):
        fade_duration *= 1000
        main_vid = self.audio + sound_amplification
        main_vid = main_vid.fade_in(fade_duration).fade_out(fade_duration)
        try:
            lofied_vid = self.apply_lofi(main_vid)
            print("=" * 15)
            print("Exporting video...")
            lofied_vid.export(output_name + ".mp3", format="mp3")
            print("Done!")
        except Exception as err:
            print("Error occured whilst trying to lofize, please try again.")
            print(err)

    def apply_lofi(self, audio, drums=True, melody=True, ambience=True, fade_duration=3, emphasize=5):
        fade_duration *= 1000
        lofi_randomized = self.randomize_lofi()
        lofied = self.lofied
        if melody:
            print("=" * 15)
            print("Adding melody...")
            try:
                melody_audio = AudioSegment.from_wav(
                    lofi_randomized["melody"]).fade_in(emphasize * 100) + emphasize
                lofied = audio.overlay(melody_audio, loop=True)
                print("Melody added.")
                if drums:
                    print("=" * 15)
                    print("Adding drums...")
                    try:
                        drums_audio = AudioSegment.from_wav(lofi_randomized["drums"])
                        lofied = lofied.overlay(
                            drums_audio, loop=True, position=(len(melody_audio)))
                    except Exception as err:
                        print("Problems whilst adding drums.")
                        print(err)
                    print("Drums added.")
                if ambience:
                    print("=" * 15)
                    print("Adding ambience...")
                    try:
                        ambience_audio = AudioSegment.from_mp3(
                            lofi_randomized["ambience"])
                        lofied = lofied.overlay(
                            ambience_audio - int(emphasize * 1.5), loop=True)
                    except Exception as err:
                        print("Problems whilst adding ambience.")
                        print(err)
                    print("Ambience added.")
            except Exception as err:
                print("Problem whilst adding melody.")
                print(err)
            

        print("\nLofi-zation completed.")
        return lofied.fade_out(fade_duration)
