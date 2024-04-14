# -*- coding: utf-8 -*-
"""Dashboard.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wFd0Tk3bb0XzQt8CLDddjJBdC1G6LbJ1
"""

import pandas as pd

url = 'https://drive.google.com/file/d/1QPBjNIxIwrMsOpTBQbvquOPyCWbbtkqF/view?usp=sharing'
csv_url = 'https://drive.google.com/uc?id=' + url.split('/')[-2]
df = pd.read_csv(csv_url, on_bad_lines='skip')


import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

col = st.columns((30, 9, 3), gap='medium')

# กำหนดค่าที่ต้องการเปลี่ยนใน column 'คุณเป็นนักศึกษาชั้นปีที่'
replace_values = {'ชั้นปีที่ 1': 'ชั้นปีที่ 1',
                  'ชั้นปีที่ 2': 'ชั้นปีที่ 2',
                  'ชั้นปีที่ 3': 'ชั้นปีที่ 3',
                  'ชั้นปีที่ 4': 'ชั้นปีที่ 4',
                  'ชั้นปีที่ 5': 'ชั้นปีที่ 5-8',
                  'ชั้นปีที่ 6': 'ชั้นปีที่ 5-8',
                  'ชั้นปีที่ 7': 'ชั้นปีที่ 5-8',
                  'ชั้นปีที่ 8': 'ชั้นปีที่ 5-8'
                  }

# เปลี่ยนค่าใน column 'คุณเป็นนักศึกษาชั้นปีที่' ใน DataFrame ใหม่
df_new = df.replace({'คุณเป็นนักศึกษาชั้นปีที่': replace_values})

# กำหนดลำดับของรายได้ต่อเดือน
price_order = ['มากกว่า 9,999 บาท',
               '9,000 - 9,999 บาท',
               '8,000 - 8,999 บาท',
               '7,000 - 7,999 บาท',
               'น้อยกว่า 7,000 บาท']

# กำหนดลำดับของชั้นปีที่ศึกษา
year_order = ['ชั้นปีที่ 1',
              'ชั้นปีที่ 2',
              'ชั้นปีที่ 3',
              'ชั้นปีที่ 4',
              'ชั้นปีที่ 5-8'
              ]

# สร้างกราฟแท่ง
chart2 = alt.Chart(df_new).mark_bar().encode(
    x=alt.X('count():Q', title='จำนวนนักศึกษา'),
    y=alt.Y('คุณมีรายได้ต่อเดือนเท่าไหร่ ?:N', sort=price_order, title='รายได้ต่อเดือน (บาท)'),
    color=alt.Color('คุณเป็นนักศึกษาชั้นปีที่:N', sort=year_order, legend=alt.Legend(title='ชั้นปีที่')),
    tooltip=['คุณมีรายได้ต่อเดือนเท่าไหร่ ?', 'คุณเป็นนักศึกษาชั้นปีที่', 'count()']
).properties(
    width=700,
    height=400,
    title='แนวโน้มรายได้ต่อเดือนของนักศึกษา โดยแบ่งตามชั้นปีที่ศึกษา'
)

# นับจำนวนข้อมูลในแต่ละกลุ่มโดยใช้ groupby และ size
grouped_3_1 = df.groupby(["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1", "เพศ"]).size().reset_index(name="จำนวนนักศึกษา")

# เพิ่มคอลัมน์ลำดับใหม่โดยใช้ค่าจากคอลัมน์ 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1'
grouped_3_1["ลำดับ"] = grouped_3_1["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1"]

# เรียงลำดับข้อมูลตามคอลัมน์ "ลำดับ" และลบคอลัมน์ "ลำดับ" ออก
grouped_3_1 = grouped_3_1.sort_values(by="ลำดับ").drop(columns=["ลำดับ"])

# กรองข้อมูลที่ไม่มีค่าใช้จ่ายในอันดับนี้
filtered_data_3_1 = grouped_3_1[grouped_3_1["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1"] != "ไม่มีค่าใช้จ่ายในอันดับนี้"]

# สร้างแผนภูมิแท่งด้วย Altair
chart3 = alt.Chart(filtered_data_3_1).mark_bar().encode(
    x=alt.X('sum(จำนวนนักศึกษา):Q', title='จำนวนนักศึกษา'),
    y=alt.Y('เพศ:N', title='เพศของนักศึกษา'),
    color=alt.Color('ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1:N', legend=alt.Legend(title='หมวดหมู่ค่าใช้จ่าย')),
    tooltip=['เพศ', 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1', 'sum(จำนวนนักศึกษา)']
).properties(
    width=700,
    height=400,
    title='แผนภูมิแท่ง แสดงการเปรียบเทียบเพศกับค่าใช้จ่ายโดยรวมอันดับ 1 ของนักศึกษาในมหาวิทยาลัย'
)

# นับจำนวนข้อมูลในแต่ละกลุ่มโดยใช้ groupby และ size
grouped_3_2 = df.groupby(["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 2", "เพศ"]).size().reset_index(name="จำนวนนักศึกษา")

# เพิ่มคอลัมน์ลำดับใหม่โดยใช้ค่าจากคอลัมน์ 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 2'
grouped_3_2["ลำดับ"] = grouped_3_2["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 2"]

# เรียงลำดับข้อมูลตามคอลัมน์ "ลำดับ" และลบคอลัมน์ "ลำดับ" ออก
grouped_3_2 = grouped_3_2.sort_values(by="ลำดับ").drop(columns=["ลำดับ"])


# กรองข้อมูลเพื่อเอาแต่ละแถวที่ไม่มีค่าใช้จ่ายในอันดับที่สองออก
filtered_data_3_2 = grouped_3_2[grouped_3_2["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 2"] != "ไม่มีค่าใช้จ่ายในอันดับนี้"]

# สร้างแผนภูมิแท่งด้วย Altair
chart4 = alt.Chart(filtered_data_3_2).mark_bar().encode(
    x=alt.X('sum(จำนวนนักศึกษา):Q', title='จำนวนนักศึกษา'),
    y=alt.Y('เพศ:N', title='เพศของนักศึกษา'),
    color=alt.Color('ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 2:N', legend=alt.Legend(title='หมวดหมู่ค่าใช้จ่าย')),
    tooltip=['เพศ', 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 2', 'sum(จำนวนนักศึกษา)']
).properties(
    width=700,
    height=400,
    title='แผนภูมิแท่ง แสดงการเปรียบเทียบเพศกับค่าใช้จ่ายโดยรวมอันดับ 2 ของนักศึกษาในมหาวิทยาลัย'
)

# นับจำนวนข้อมูลในแต่ละกลุ่มโดยใช้ groupby และ size
grouped_3_3 = df.groupby(["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 3", "เพศ"]).size().reset_index(name="จำนวนนักศึกษา")

# เพิ่มคอลัมน์ลำดับใหม่โดยใช้ค่าจากคอลัมน์ 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 3'
grouped_3_3["ลำดับ"] = grouped_3_3["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 3"]

# เรียงลำดับข้อมูลตามคอลัมน์ "ลำดับ" และลบคอลัมน์ "ลำดับ" ออก
grouped_3_3 = grouped_3_3.sort_values(by="ลำดับ").drop(columns=["ลำดับ"])

# กรองข้อมูลเพื่อเอาแต่ละแถวที่ไม่มีค่าใช้จ่ายในอันดับที่สามออก
filtered_data_3_3 = grouped_3_3[grouped_3_3["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 3"] != "ไม่มีค่าใช้จ่ายในอันดับนี้"]

# สร้างแผนภูมิแท่งด้วย Altair
chart5 = alt.Chart(filtered_data_3_3).mark_bar().encode(
    x=alt.X('sum(จำนวนนักศึกษา):Q', title='จำนวนนักศึกษา'),
    y=alt.Y('เพศ:N', title='เพศของนักศึกษา'),
    color=alt.Color('ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 3:N', legend=alt.Legend(title='หมวดหมู่ค่าใช้จ่าย')),
    tooltip=['เพศ', 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 3', 'sum(จำนวนนักศึกษา)']
).properties(
    width=700,
    height=400,
    title='แผนภูมิแท่ง แสดงการเปรียบเทียบเพศกับค่าใช้จ่ายโดยรวมอันดับ 3 ของนักศึกษาในมหาวิทยาลัย'
)

# นับจำนวนข้อมูลในแต่ละกลุ่มของคอลัมน์ 'คุณเป็นนักศึกษาชั้นปีที่' และ 'คุณใช้จ่ายเงินเฉลี่ยเท่าไหร่ต่อวันในมหาวิทยาลัย ?'
grouped_6 = df.groupby(["คุณเป็นนักศึกษาชั้นปีที่", "คุณใช้จ่ายเงินเฉลี่ยเท่าไหร่ต่อวันในมหาวิทยาลัย ?"]).size().reset_index(name="จำนวนนักศึกษา")

# สร้าง dictionary เพื่อกำหนดลำดับใหม่สำหรับชั้นปีของนักศึกษา
reorder_map = {
    "ชั้นปีที่ 1": 0,
    "ชั้นปีที่ 2": 1,
    "ชั้นปีที่ 3": 2,
    "ชั้นปีที่ 4": 3,
    "ชั้นปีที่ 5-8": 4
}

# รวมชั้นปีที่ 5 ถึง 8 เป็นชั้นปีที่ 5-8
grouped_6['คุณเป็นนักศึกษาชั้นปีที่'] = grouped_6['คุณเป็นนักศึกษาชั้นปีที่'].replace(['ชั้นปีที่ 5', 'ชั้นปีที่ 6', 'ชั้นปีที่ 7', 'ชั้นปีที่ 8'], 'ชั้นปีที่ 5-8')

# นับจำนวนนักศึกษาใหม่โดยรวมชั้นปีที่ 5-8
grouped_6 = grouped_6.groupby(["คุณเป็นนักศึกษาชั้นปีที่", "คุณใช้จ่ายเงินเฉลี่ยเท่าไหร่ต่อวันในมหาวิทยาลัย ?"]).agg({'จำนวนนักศึกษา': 'sum'}).reset_index()

# เพิ่มคอลัมน์ลำดับใหม่โดยใช้ dictionary reorder_map
grouped_6["ลำดับ"] = grouped_6["คุณเป็นนักศึกษาชั้นปีที่"].map(reorder_map)

# เรียงลำดับตามคอลัมน์ "ลำดับ" และลบคอลัมน์ "ลำดับ" ออก
grouped_6 = grouped_6.sort_values(by="ลำดับ").drop(columns=["ลำดับ"])

# สร้างแผนภูมิแท่งด้วย Altair
chart6 = alt.Chart(grouped_6).mark_bar().encode(
    x=alt.X('sum(จำนวนนักศึกษา):Q', title='จำนวนนักศึกษา (คน)'),
    y=alt.Y('คุณเป็นนักศึกษาชั้นปีที่:N', title='ชั้นปี'),
    color=alt.Color('คุณใช้จ่ายเงินเฉลี่ยเท่าไหร่ต่อวันในมหาวิทยาลัย ?:N', legend=alt.Legend(title='ค่าใช้จ่ายเฉลี่ยต่อวัน')),
    tooltip=['คุณเป็นนักศึกษาชั้นปีที่', 'คุณใช้จ่ายเงินเฉลี่ยเท่าไหร่ต่อวันในมหาวิทยาลัย ?', 'sum(จำนวนนักศึกษา)']
).properties(
    width=700,
    height=400,
    title='จำนวนนักศึกษาในแต่ละชั้นปีตามค่าใช้จ่ายเฉลี่ยต่อวัน'
)

# นับจำนวนข้อมูลในแต่ละกลุ่มของคอลัมน์ 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1' และ 'จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 1 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'
grouped_8_1 = df.groupby(["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1", "จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 1 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?"]).size().reset_index(name="จำนวนนักศึกษา")
# นับจำนวนข้อมูลในแต่ละกลุ่มของคอลัมน์ 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 2' และ 'จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 2 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'
grouped_8_2 = df.groupby(["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 2", "จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 2 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?"]).size().reset_index(name="จำนวนนักศึกษา")
# นับจำนวนข้อมูลในแต่ละกลุ่มของคอลัมน์ 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 3' และ 'จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 3 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'
grouped_8_3 = df.groupby(["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 3", "จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 3 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?"]).size().reset_index(name="จำนวนนักศึกษา")

# สร้าง dictionary เพื่อกำหนดลำดับใหม่สำหรับจำนวนเงินที่ใช้จ่าย
reorder_expenses_map = {
    "ต่ำกว่า 500 บาท": 0,
    "500 - 1,500 บาท": 1,
    "1,501 - 2,500 บาท": 2,
    "2,501 - 3,500 บาท": 3,
    "3,501 - 4,500 บาท": 4,
    "4,501 - 5,500 บาท" : 5,
    "มากกว่า 5,500 บาท" : 6
}

# รวมทั้งสาม dataframe
frames = [grouped_8_1, grouped_8_2, grouped_8_3]
df_concat = pd.concat(frames)

# รวมคอลัมน์ที่มีค่าเหมือนกันและบวกค่าจำนวนนักศึกษา
grouped_df_8 = df_concat.groupby(["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1", "จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 1 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?"]).sum().reset_index()

# เปลี่ยนชื่อคอลัมน์เพื่อความชัดเจน
grouped_df_8.rename(columns={'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1': 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุด'}, inplace=True)
grouped_df_8.rename(columns={'จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 1 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?': 'คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'}, inplace=True)

# ลบคอลัมน์ที่ไม่จำเป็นออก
grouped_df_8.drop(['ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 2', 'จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 2 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?', 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 3', 'จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 3 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'], axis=1, inplace=True)

# เพิ่มคอลัมน์ลำดับใหม่
grouped_df_8["ลำดับ"] = grouped_df_8["คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?"].map(reorder_expenses_map)

# เรียงลำดับตามคอลัมน์ "ลำดับ"
grouped_df_8 = grouped_df_8.sort_values(by="ลำดับ").drop(columns=["ลำดับ"])

# สร้าง DataFrame จากข้อมูลที่มีอยู่
data = {
    'คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?': grouped_df_8["คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?"].tolist(),
    'จำนวนนักศึกษา': grouped_df_8["จำนวนนักศึกษา"].tolist(),
    'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุด': grouped_df_8["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุด"].tolist()
}
df = pd.DataFrame(data)

# สร้างกราฟ
chart8 = alt.Chart(df).mark_bar().encode(
    y=alt.Y('คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?:N', title='ค่าใช้จ่ายโดยประมาณต่อหนึ่งเดือน'),
    x=alt.X('จำนวนนักศึกษา:Q', title='จำนวนนักศึกษา (คน)'),
    color='ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุด:N',
    order=alt.Order(
      'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุด:N',
      sort='ascending'
    )
).properties(
    width=600,
    height=400,
    title='แผนภูมิแท่ง แสดงการเปรียบเทียบประเภทค่าใช้จ่ายส่วนที่มากที่สุดกับปริมาณค่าใช้จ่ายที่ในส่วนนั้น'
)

with col[0]:
    st.altair_chart(chart2, use_container_width=True)
    st.altair_chart(chart3, use_container_width=True)
    st.altair_chart(chart4, use_container_width=True)
    st.altair_chart(chart5, use_container_width=True)
with col[1]:
    st.altair_chart(chart6, use_container_width=True)
    st.altair_chart(chart8, use_container_width=True)
