#coding:utf8
import jieba
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np

def build_word_cloud(file_path):
    with open(file_path) as fp:
        file_content = fp.read()
    # 结巴切词
    x = jieba.cut(file_content)
    # 存储切完的词
    segment = [cut for cut in x if len(cut) > 1 and cut != '\r\n']
    # 分词完初步筛选后的df
    words_df = pd.DataFrame(dict(segment=segment))
    # 停用词
    stopwords = pd.read_csv(r'stopwords.txt',encoding='utf-8', index_col=False, quoting=3,
                            sep='\t', names=['stopword'])
    # 去停用词
    words_df = words_df[~words_df['segment'].isin(stopwords['stopword'])]
    words_stat = words_df.groupby(['segment'])['segment'].agg({'计数': np.size})
    # 将索引编程一个列, 然后索引改成整数
    words_stat = words_stat.reset_index().sort_values(by='计数', ascending=False)
    wc = WordCloud(font_path=r'STXINWEI.TTF')
    wc = wc.fit_words(dict(zip(words_stat['segment'], words_stat['计数'])))
    plt.imshow(wc.recolor(), interpolation='bilinear')
    plt.axis("off")
    plt.show()

build_word_cloud("test_data.txt")