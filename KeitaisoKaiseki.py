# coding: utf-8
import MeCab

mecab = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

INPUT_FILE_PATH = "./scraping.csv"
OUTPUT_FILE_PATH = "./mecab.txt"

with open(INPUT_FILE_PATH) as f:
    text = f.read()

# mecab.parse('')#文字列がGCされるのを防ぐ
node = mecab.parseToNode(text)
while node:
    #単語を取得
    word = node.surface
    #品詞を取得
    pos = node.feature.split(",")[1]
    tmp_str = '{0} , {1}\n'.format(word, pos)

    with open(OUTPUT_FILE_PATH, mode='a') as f:
        f.write(tmp_str)
    
    #次の単語に進める
    node = node.next
