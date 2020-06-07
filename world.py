import datetime

import requests
import json
import pandas as pd

from pyecharts import options as opts
from pyecharts.charts import *
from pyecharts.components import Table
from pyecharts.globals import ThemeType

from world_country_name import item_contry

def getchinadata():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    r = requests.get(url=url).json()['data']
    data = json.loads(r)
    data = data['chinaTotal']
    item = {
        '国家中文':'中国',
        '国家英文':'China',
        '新增确诊':'',
        '总确诊':data['confirm'],
        '疑似':data['suspect'],
        '治愈':data['heal'],
        '死亡':data['dead'],
        '现有确诊':data['nowConfirm'],

    }
    return item

def world_map(url):
    r = requests.get(url).json()['data']

    # data = json.loads(r)
    countryList = []
    for i in r:

        item = {
            '国家中':i['name'],  # 国家
            '国家英':item_contry[i['name']] if i['name'] in item_contry else i['name'], # 如果没有国家英就显示原来的名字
            # '大洲':i['continent'], # 大洲
            # '日期':i['date'], # 日期
            # '是否更新':i['isUpdated'], # 是否更新
            '新增确诊':i['confirmAdd'], # 新增确诊
            # '确认':i['confirmAddCut'], #确认
            '总确诊':i['confirm'], # 总确诊
            '疑似':i['suspect'], # 疑似
            '死亡':i['dead'], # 死亡
            '治愈':i['heal'], # 治愈
            '现有确诊':i['confirm'], # 现有确诊
            # '证实':i['confirmCompare'], # 证实
            # '新增证实':i['nowConfirmCompare'], # 新增证实
            # '治愈证实':i['healCompare'], #治愈证实
            # '死亡证实':i['deadCompare'], # 死亡证实
        }
        countryList.append(item)
    countryList.append(getchinadata())
    df = pd.DataFrame(countryList)
    df.to_csv('./countrycsv/各国数据(%s).csv'%(datetime.date.today()))

    map =(
        Map(init_opts=opts.InitOpts(width="1500px", height="1500px", theme=ThemeType.DARK))
            .add("国家", [list(z) for z in zip(list(df['国家英']),list(df['总确诊']))], "world")
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title='世界疫情确诊地图'), # 标题
            visualmap_opts=opts.VisualMapOpts(
                max_=500000,
                is_piecewise=True,  # 颜色是否分段显示（False为渐变，True为分段）
                pieces=[

                    {"min": 1, "max": 10, "label": "1-10人以下", "color": "#FFE6BE"},
                    {"min": 10, "max": 49, "label": "10-49人", "color": "#FFB769"},
                    {"min": 50, "max": 99, "label": "50-99人", "color": "#FF8F66"},
                    {"min": 100, "max": 499, "label": "100-499人", "color": "#ED514E"},
                    {"min": 500, "max": 999, "label": "500-999人", "color": "#CA0D11"},
                    {"min": 1000, "max": 9999, "label": "1000-9999人", "color": "#C23531"},
                    {"min": 10000, "max": '', "label": "10000>人", "color": "#C80000"},
                ]
            ),#根据颜色进行区分
            tooltip_opts=opts.TooltipOpts( is_show=True,  # 显示
                    trigger_on='mousemove|click',)  # 鼠标点击或者移动到出现具体的数值)

        )
        # .render('./html文件/各国数据(%s).html'%(datetime.date.today()))
    )

    headers = df.columns.to_list()
    rows = list(df.values)
    # print(rows)
    table = (
        Table()
        .add(headers,rows)
        .set_global_opts(title_opts=opts.ComponentTitleOpts(title="Table"))
    )
    page = Page(layout=Page.DraggablePageLayout)
    page.add(
        map,
        table,
    )
    page.render('./templates/各国数据(%s).html'%(datetime.date.today()))


if __name__ == '__main__':
    url = 'https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist'
    world_map(url)