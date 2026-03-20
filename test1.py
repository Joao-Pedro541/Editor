import moviepy 
import whisper





def audioEditor():
    takes = {"take 1": []}
    actualTake = "take 1"
    audio = moviepy.AudioFileClip("audio1.mp3") 

    model = whisper.load_model("turbo")
    result = model.transcribe("audio1.mp3", fp16=False)

    for segments in result["segments"]:
        print(segments["text"] + " " + str(segments["start"]) + " " + str(segments["end"]))
        words = segments["text"].lower().split()
        isAtake = False
        if "take" in words:
            
            try:
                idx = words.index("take")
                take_number = words[idx + 1]
                actualTake = f"take {take_number}"

                if actualTake not in takes:
                    takes[actualTake] = []
                isAtake = True
            except:
                pass

        if isAtake == True:
            takes[actualTake].clear()
            takes[actualTake] = []
        else: 
            takes[actualTake].append([segments["start"], segments["end"]])

    clips = []
    for tk in takes.values():
        for start, end in tk:
            start = max(0, start)
            end = min(end, audio.duration)

            if start < end: 
                clips.append(audio.subclipped(start, end))

    finalAudio = moviepy.concatenate_audioclips(clips)
    finalAudio.write_audiofile("final_clip.mp3")
                

def main():
    audioEditor()


if __name__ == "__main__":
    main()