import moviepy 
import whisper

def VideoEditor():
    takes = {"take 1": []}
    actualTake = "take 1"
    
    videoClip = moviepy.VideoFileClip("video1.mp4")
    videoClip.audio.write_audiofile("audio1.mp3")

    audioClip = moviepy.AudioFileClip("audio1.mp3")

    model = whisper.load_model("turbo")
    result = model.transcribe("audio1.mp3", fp16=False)

    for segments in result["segments"]:
        words = segments["text"].lower().split()
        print(words)
        isAtake = False
        if "take" in words:
            idx = words.index("take")
            take_number = words[idx + 1]
            actualTake = f"take {take_number}"

            if actualTake not in takes:
                takes[actualTake] = []
            isAtake = True

        if isAtake == True:
            takes[actualTake].clear()
            takes[actualTake] = []
        else: 
            takes[actualTake].append([segments["start"], segments["end"]])

    clips = []
    for tk in takes.values():
        for start, end in tk:
            start = max(0, start)
            end = min(end, videoClip.duration)

            if start < end: 
                clips.append(videoClip.subclipped(start, end))

    finalVideo = moviepy.concatenate_videoclips(clips)
    finalVideo.write_videofile("final_clip.mp4")  

def main():
    VideoEditor()

if __name__ == "__main__":
    main()