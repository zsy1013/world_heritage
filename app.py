import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium import plugins

st.title('World Heritage Plus')

#------sidebarコード---------
tiles = st.sidebar.selectbox(
    '地図の種類を選択してください',
     ['OpenStreetMap',
     'stamenterrain',
     'cartodbpositron',
     ]
)

#st.sidebar.write('追加する情報を選んでください')
st.sidebar.checkbox('気温データ【月平均(℃)】※準備中')
st.sidebar.checkbox('降水量データ【月平均(mm)】※準備中')
st.sidebar.slider('気温の変化(月別)', 1, 12, 1, 1)
st.sidebar.slider('降水量の変化(月別)', 1, 12, 1, 1)

expander = st.sidebar.expander('お問合せ先')
expander.write('準備中')


#------mainコード---------
num_list = ['登録基準(ⅰ)', '登録基準(ⅱ)', '登録基準(ⅲ)', '登録基準(ⅳ)', '登録基準(ⅴ)', 
            '登録基準(ⅵ)', '登録基準(ⅶ)', '登録基準(ⅷ)', '登録基準(ⅸ)', '登録基準(ⅹ)']

numbers = st.multiselect('登録基準を選択してください', num_list, num_list)

select_n = []
for number in numbers:
    number = number.replace('登録基準', '')
    select_n.append(number)

df = pd.read_csv('世界遺産サンプル.csv') 

heritage_df = pd.DataFrame()
for n in select_n:
    n = df[df[n]==1]
    heritage_df = heritage_df.append(n)

def Heritage_Map(df, m):
    for index, r in df.iterrows():
        if r['種類'] == '文化遺産':
            color = 'orange'
            icon = 'tower'
        elif r['種類'] == '自然遺産':
            color = 'green'
            icon = 'tree-conifer'
        else:
            color = 'lightblue'
            icon= 'globe'
        
        popup=folium.Popup(r['popup'], max_width=30)
        folium.Marker(
            location=[r.lat, r.lon],
            popup=popup,
            icon=folium.Icon(color=color, icon=icon)
        ).add_to(m)
        
m = folium.Map(location=[41.897706284596445, 12.498682805103234], tiles=tiles, zoom_start=1.5)

Heritage_Map(heritage_df, m)
minimap = plugins.MiniMap()
m.add_child(minimap)
folium_static(m)