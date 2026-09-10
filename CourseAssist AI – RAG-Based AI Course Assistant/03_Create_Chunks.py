import whisper
import os
import json

model = whisper.load_model("large-v2")
audios = os.listdir("audios")
# print(audios)

for audio in audios:
    if "_" in audio:
        title_no = audio.split("_")[0]
        title = audio.split("_")[1].split(".")[0]
        # print(title_no, title) 
        result = model.transcribe(audio=f"audios/{audio}",
         language="hi",
         task="translate",
         word_timestamps= False)

    
        chunks = []    
        for segment in result["segments"]:
            chunks.append({"Lecture": title_no, "Title": title, "Start": segment["start"], "End": segment["end"], "Text": segment['text']})

        chunk_with_metadata = {"chunks": chunks, "text": result["text"]}

        with open (f"json/{title_no + title}.json", "w") as f:
            json.dump(chunk_with_metadata, f)






