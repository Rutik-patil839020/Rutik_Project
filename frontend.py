import youtube_transcript_api
from taipy.gui import Gui
import taipy.gui.builder as tgb
from backend.backend import sentiment_analyse
from pytube import YouTube
import pandas as pd

video_id = " "
result = " "
data_file = "data_file.csv"
score = 0
result_records = pd.read_csv(data_file)


def extract_video_id(url):
    # Extract video id from Youtube url
    after_equal_sign = url.split('=')[-1]
    video_id = after_equal_sign.split('&')[0]
    return video_id


def extract_video_title(url):
    # Extract video title from YouTube URL
    yt = YouTube(url)
    title = yt.title.replace(",", " ")
    return title


def submit_url(state):
    # Extract video ID from user input URL
    video_id = extract_video_id(state.video_id)
    print("Video ID:", video_id)

    # Extract video title
    title = extract_video_title(state.video_id)
    print("Video Title:", title)

    # Perform sentiment analysis using the extracted video ID
    try:
        state.result,state.score = sentiment_analyse(video_id)
        state.score = round(float(state.score), 2)

        # Step 1 - Save result in CSV file
        save_result(video_id,state.video_id,title,state.result,state.score)

        # Step 2 - Update table with new record
        state.result_records = pd.read_csv(data_file)
    except youtube_transcript_api.TranscriptsDisabled as e:
        state.result = "Subtitles are disabled for this video"



def save_result(video_id,link, title, result,score):
    # Open CSV file with write and append mode and write record ending with \n
    with open(data_file, 'a') as file1:
        file1.write(f"{video_id},{link},{title},{result},{score}\n")


page = """
# Sentimental Analysis **On**{: .color-primary} **Youtube Video**{: .color-primary}
### **<font color ="Coral" >Enter The  Youtube Url</font>** <|{video_id}|input|> <|submit|button|on_action=submit_url|>

### **<font color = "Plum">Sentiment Analysis Result :</font>** <|{result}|text|>

### **<font color = "Salmon">Score :</font>** <|{score}|text|>

### **<font color = " LightPink">Sentiment History</font>** 

<|{result_records}|table|>

 
### **<font color="LightGreen">Sentiment Chart</font>**

<|{result_records}|chart|type=line|x=Youtube_id|y=Score|color[positive]=green|color[negative]=red|>


"""


Gui(page).run(debug=True)
