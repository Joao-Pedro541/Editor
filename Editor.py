import moviepy 
import whisper


class Editor():

    def __init__(self):
        self.clips = []

        self.takes = {f"take {1}": []}
        self.actualTake = f"take {1}"
        self.takesRange = 2

    def trascription(self):
        
        
        videoClip = moviepy.VideoFileClip("video1.mp4")
        videoClip.audio.write_audiofile("audio1.mp3")

        audioClip = moviepy.AudioFileClip("audio1.mp3")

        model = whisper.load_model("turbo")
        result = model.transcribe("audio1.mp3", fp16=False)

        isAPause = False

        for i in range(len(result["segments"])):
            words = result["segments"][i]["text"].lower().split()
            
            actualWords = []
            for w in words:
                actualWords.append(w.replace(",", ""))
            print(f"{result['segments'][i]['start']}: {actualWords} end: {result['segments'][i]['end']}")

            if "pause" in actualWords:
                isAPause = True
                continue
            elif "return" in actualWords:
                isAPause = False
                continue
            elif "take" in actualWords:
                idx = actualWords.index("take")
                take_number = actualWords[idx + 1]
                self.actualTake = f"take {take_number}"

                if self.actualTake not in self.takes:
                    self.takes[self.actualTake] = []
                self.takes[self.actualTake].clear()
                continue

            elif "silence" in actualWords:
                self.takes[self.actualTake].append([result["segments"][i]["end"],result["segments"][i + 1]["start"]])
                continue
            if isAPause:
                continue
                
            if not isAPause: 
                self.takes[self.actualTake].append([result["segments"][i]["start"], result["segments"][i]["end"]])
    

    def audioEditor(self, audio: moviepy.AudioClip):

        self.trascription()

        for tk in self.takes.values():
            for start, end in tk:
                start = max(0, start)
                end = min(end, audio.duration)

                if start < end: 
                    self.clips.append(audio.subclipped(start, end))

        finalAudio = moviepy.concatenate_audioclips(self.clips)
        finalAudio.write_audiofile("finalAudioClip.mp3")

    def VideoEditor(self, videoClip: moviepy.AudioClip):
        self.trascription()

        clips = []
        for tk in self.takes.values():
            for start, end in tk:
                print(f"{start} + end: + {end}")
                start = max(0, start)
                end = min(end, videoClip.duration)

                if start < end: 
                    clips.append(videoClip.subclipped(start, end))

        finalVideo = moviepy.concatenate_videoclips(clips)
        finalVideo.write_videofile("finalVideoClip.mp4")  

editor = Editor()

if __name__ == "__main__":
    editor.VideoEditor(moviepy.VideoFileClip("video1.mp4"))