import pandas as pd
import matplotlib.pyplot as plt
from pyecharts import Geo,Style,Line,Bar,Overlap

f = open(r'月饼数据.txt',encoding='utf-8')

df = pd.read_csv(f,sep=',',names=['title','price','sales','location'])

print(df.describe())