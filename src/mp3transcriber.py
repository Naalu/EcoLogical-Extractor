import whisper

def audio_transcriber(infile, outfile):
    model = whisper.load_model("turbo")
    result = model.transcribe(infile)
    with open(outfile, "w", encoding="utf-8") as file:
        file.write(result["text"])

## Example Usage
# for num in [244, 268, 337, 374, 442, 450, 527]:
#     infile = str(num) + ".mp3"
#     outfile = str(num) + "out.txt"
#     audio_transcriber(infile, outfile)