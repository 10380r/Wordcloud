import urllib.request
from bs4 import BeautifulSoup
import MeCab
from collections import Counter
from wordcloud import WordCloud

url = 'https://tech-camp.in/note/technology/226/'

html = urllib.request.urlopen(url)

soup = BeautifulSoup(html, 'html.parser')

section = soup.find('section', class_='post-content single-post-content')
p = section.findAll('p')

text = ''
for i in p:
    w = i.text
    text += w

# 形態素解析
m = MeCab.Tagger()
keywords = m.parse(text)

output_words = []

for row in keywords.split('\n'):
    word = row.split('\t')[0]  # word:単語
    if word == 'EOS':  # EOS：mecabで終了時出力される
        break
    else:
        pos = row.split('\t')[1].split(',')[0]  #pos: 品詞名
        if pos == '名詞' or pos == '形容詞':  # 名詞と形容詞のみ抽出
            output_words.append(word)

counter = Counter(output_words)

wl = []

for i in counter.most_common():
    wl.append(i)

texts = ''
for i in wl:
    texts += i[0] + ' '


# wordcloud
def create_wordcloud(text):
    fpath = "/Library/Fonts/Ricty-Regular.ttf"

    # ノイズが多すぎたので、ストップワードの設定
    stop_words = ['よう', 'こと', 'の', '方', 'たち', 'ため', 'ー', '>', ':', '<', \
                  '中', '者', 'やす', '-', 'やすい', 'h', '思う', 'こちら']

    wordcloud = WordCloud(background_color="white", font_path=fpath, width=900, height=500, \
                          stopwords=set(stop_words)).generate(text)

    # 画像の生成
    wordcloud.to_file("results/wordcloud.png")
    print('Done!')


create_wordcloud(texts)
