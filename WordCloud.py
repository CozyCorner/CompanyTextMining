# coding: utf-8
from wordcloud import WordCloud

FONT_PATH = "/System/Library/Fonts/ヒラギノ角ゴシック W9.ttc"

INPUT_FILE_PATH = "./mecab_edited.txt"
OUTPUT_FILE_PATH = "./wordcloud.png"

with open(INPUT_FILE_PATH) as f:
    text = f.read()

stop_words = ["出力画像から", "除外したい", "単語を", "お好みで", "設定してください"]

wordcloud = WordCloud(background_color="white",
    font_path=FONT_PATH,
    width=800,height=600,
    stopwords=set(stop_words)).generate(text)  

wordcloud.to_file(OUTPUT_FILE_PATH)
