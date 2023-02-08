import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib
matplotlib.use('Agg')
import plotly.graph_objects as go
import geopandas as gp
import json
from datetime import datetime, timedelta


def run_predict():
    t1, t2 = st.tabs(['전세예측','전월세평균'])

    with t1:
        st.title('지도 그래프')
        #st.tabs(["A","B"])
        ef = "data/ef.geojson"
        dgg = gp.read_file(ef,encoding='euc-kr')
        #map_df = gp.read_file(fp)
        #map_df.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)

        ab = "data/dong_j_d_mean.csv"
        dff =  pd.read_csv(ab,encoding='euc-kr')
        now = datetime.now()
        default_date = now - timedelta(days=1)
        date1 = st.date_input("날짜선택", default_date)
        date2 = st.selectbox("구선택", dgg['adm_nm'].unique())
        map_dong = dgg[dgg['adm_nm'] == f'{date2}']
        map_si = dff[dff['CNTRCT_DE'] == f'{date1}']
        merged = map_dong.set_index('adm_nm').join(map_si.set_index('BJDONG_NM'))
        fig = px.choropleth_mapbox(merged, geojson=merged.geometry, locations=merged.index, color="RENT_GTN", mapbox_style="carto-positron", zoom=9.8, 
        center = {"lat": 37.575651, "lon": 126.97689}, opacity=0.6)
        fig.update_geos(fitbounds="locations", visible=True)

        if  merged["RENT_GTN"].values > 0:
            st.plotly_chart(fig)
        else:
            st.markdown('# 금일 거래는 없습니다.')
            st.plotly_chart(fig)

        st.title('전세 예측')
        
    with t2:    
        j_m_mean = pd.read_csv('data/gu_j_m_mean.csv', encoding='cp949')
        w_m_mean = pd.read_csv('data/gu_w_m_mean.csv', encoding='cp949')

        gu = np.array(j_m_mean['SGG_NM'].unique())
        t3, t4 = st.tabs(['전세 월평균 예측','월세 월평균 그래프']) 
        with t3:
            c1 = st.checkbox('전세 월평균 그래프', True)
            
            fig = go.Figure()
            dic = {}
            if c1:
                fig = px.scatter(width=700)
                for i in gu:
                    dic.update({i : j_m_mean[j_m_mean['SGG_NM']==i]['RENT_GTN']})
                
                for j in gu:
                    df = j_m_mean[j_m_mean['SGG_NM']==j]
                    fig.add_scatter(x=df['YM'], y=df['RENT_GTN'], name=j)
                fig.update_layout(xaxis_title='날짜', yaxis_title='보증금(k=천만원)')
                st.plotly_chart(fig)

            else:
                st.write(j_m_mean)

        with t4:
            c1, c2 = st.columns([1,1])
            s1 = c1.checkbox('보증금 월평균 그래프', True)
            s2 = c2.checkbox('월세 월평균 그래프', True)

            p1 = c1.empty()
            p2 = c2.empty()
            
            fig = go.Figure()
            dic = {}
            if s1:
                with p1.container():
                    fig = px.scatter(width=350)
                    for i in gu:
                        dic.update({i : w_m_mean[w_m_mean['SGG_NM']==i]['RENT_GTN']})
                    
                    for j in gu:
                        df = w_m_mean[w_m_mean['SGG_NM']==j]
                        fig.add_scatter(x=df['YM'], y=df['RENT_GTN'], name=j)
                    fig.update_layout(xaxis_title='날짜', yaxis_title='보증금(k=천만원)')
                    st.plotly_chart(fig)

            else:
                c1.write(j_m_mean)
                p1 = st.empty()

            if s2:
                with p2.container():
                    fig = px.scatter(width=350)
                    for i in gu:
                        dic.update({i : w_m_mean[w_m_mean['SGG_NM']==i]['RENT_GTN']})
                    
                    for j in gu:
                        df = w_m_mean[w_m_mean['SGG_NM']==j]
                        
                        fig.add_scatter(x=df['YM'], y=df['RENT_FEE'], name=j)
                    fig.update_layout(xaxis_title='날짜', yaxis_title='보증금(만원)')
                    st.plotly_chart(fig)
            else:
                c2.write(w_m_mean)
                p2 = st.empty()

        data = pd.read_csv('data/bds_data.csv', encoding='cp949')
        data2 = data.copy()       
        # 실거래 수 지역 순위
        col1, col2 = st.columns(2)
        # 월세 실거래 수 지역 순위
        with col1:
            st.subheader('월세 실거래 수 지역 순위')
            # 월세인 데이터 추출
            data_m = data2[data2['RENT_GBN']=='월세']
            # 구, 동 합치기
            cols = ['SGG_NM', 'BJDONG_NM']
            data_m['주소'] = data_m[cols].apply(lambda row:' '.join(row.values.astype(str)),axis=1)
            # 같은 구, 동 카운트
            data_addr = data_m['주소'].value_counts().rename_axis('주소').reset_index(name='거래 수')
            #인덱스 재지정
            data_addr = data_addr.reset_index(drop=True)
            data_addr.index = data_addr.index+1

            # 그래프
            c1 = st.checkbox('월세 실거래 수 지역 순위 그래프', True)
            fig = go.Figure()
            if c1:
                fig = px.bar(x=data_addr.head(10)['주소'], y=data_addr.head(10)['거래 수'], width=350,
                            color=data_addr.head(10)['주소'])
                fig.update_layout(xaxis_title='지역 동', yaxis_title='보증금(만원)')
                st.plotly_chart(fig)
            else:
                # 데이터
                st.write(data_addr.head(10))

        # 전세 실거래 수 지역 순위(월세와 같은 방식)
        with col2:
            st.subheader('전세 실거래 수 지역 순위')
            data_m = data2[data2['RENT_GBN']=='전세']
            cols = ['SGG_NM', 'BJDONG_NM']
            data_m['주소'] = data_m[cols].apply(lambda row:' '.join(row.values.astype(str)),axis=1)
            data_addr = data_m['주소'].value_counts().rename_axis('주소').reset_index(name='거래 수')
            data_addr = data_addr.reset_index(drop=True)
            data_addr.index = data_addr.index+1
            # 그래프
            c1 = st.checkbox('전세 실거래 수 지역 순위 그래프', True)
            fig = go.Figure()
            if c1:
                fig = px.bar(x=data_addr.head(10)['주소'], y=data_addr.head(10)['거래 수'], width=350,
                            color=data_addr.head(10)['주소'])
                fig.update_layout(xaxis_title='지역 동', yaxis_title='보증금(만원)')
                st.plotly_chart(fig)
            else:
                # 데이터
                st.write(data_addr.head(10))        
            