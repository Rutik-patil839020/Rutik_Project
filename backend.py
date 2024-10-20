from youtube_transcript_api import YouTubeTranscriptApi
from deepmultilingualpunctuation import PunctuationModel
from transformers import pipeline

def sentiment_analyse(url):
    video_id = url

    #transcripts = YouTubeTranscriptApi.get_transcript(video_id, languages=('en-US',))
    transcripts = YouTubeTranscriptApi.get_transcript(video_id)

    text = []
    for transcript in transcripts:
        current_line = transcript['text']
        if "[Music]" not in current_line:
            text.append(current_line)

    data = PunctuationModel().restore_punctuation(" ".join(text))
    data = data.split(".")

    print(data)
    score= 0
    line_no = 1
    classifier = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
    results = classifier(data)
    for result in results:
    #    print(result)
        if result['label'] == 'POSITIVE':
            score = score + result['score']
        else:
            score = score - result['score']
        print(f"label: {result['label']} with score : {round(result['score'], 4)} line : {data[line_no-1]}")
        line_no = line_no + 1

    print(f"Total lines : {len(results)}")
    #print(f"Final Result = {final_result}")

    if score > 0:
        return "Positive",score
    else:
        return "Negative",score



    #return final_result
  #   final_result = final_result / len(results)

  #   print(f"Avg result = {final_result}")

