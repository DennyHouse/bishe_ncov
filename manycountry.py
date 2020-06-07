import datetime

import requests
import json
import pyecharts
import pandas as pd
import urllib.parse

from pyecharts import options as opts
from pyecharts.charts import *

def downdata(country,url):

    data = requests.get(url).json()
    list = []

    for i in data['data']:

        info = {
            'country':country,
            'date':i['date'],
            'confirm_add':i['confirm_add'],
            'confirm':i['confirm'],
            'heal':i['heal'],
            'dead':i['dead']
        }
        list.append(info)
    df = pd.DataFrame(list)
    df.to_csv('./countrycsv/%s.csv'%country)
    # print(df)

def country_line():

    df_yilang = pd.read_csv('./countrycsv/伊朗.csv')
    df_deguo = pd.read_csv('./countrycsv/德国.csv')
    df_yidali = pd.read_csv('./countrycsv/意大利.csv')
    df_ribenbentu = pd.read_csv('./countrycsv/日本本土.csv')
    df_faguo = pd.read_csv('./countrycsv/法国.csv')
    df_meiguo = pd.read_csv('./countrycsv/美国.csv')
    df_yingguo = pd.read_csv('./countrycsv/英国.csv')
    df_xibanya = pd.read_csv('./countrycsv/西班牙.csv')

    # print(list(df_yilang['confirm'])[6:])
    """
    以为各个国家开始统计的日期不一致，所以在此以2.25日以后开始画图
    """
    # print(list(df_yilang['date'][6:]))
    lines =(
        Line()

        .add_xaxis([x.strftime('%Y-%m-%d') for x in list(pd.date_range(start='2020-02-25', end=datetime.date.today()))])
        .add_yaxis('伊朗',y_axis=list(df_yilang['confirm'])[6:])
        .add_yaxis('德国',list(df_deguo['confirm'])[28:])
        .add_yaxis('意大利',list(df_yidali['confirm'])[25:])
        .add_yaxis('日本本土',list(df_ribenbentu['confirm'])[28:])
        .add_yaxis('法国',list(df_faguo['confirm'])[28:])
        .add_yaxis('美国',list(df_meiguo['confirm'])[28:])
        .add_yaxis('英国',list(df_yingguo['confirm'])[25:])
        .add_yaxis('西班牙',list(df_xibanya['confirm'])[24:])
        .set_global_opts(
            title_opts = opts.TitleOpts(title='多国累计确诊趋势'),
            datazoom_opts= opts.DataZoomOpts(
                is_show=True,#显示
                is_realtime=True,#拖动时，是否实时更新系列的视图。如果设置为 false，则只在拖拽结束的时候更新。
                range_end= 60, # 数据窗口范围的结束百分比。
            ),
            tooltip_opts= opts.TooltipOpts(
                is_show=True,
                trigger='axis', #坐标轴触发，主要在柱状图和折线图使用
                trigger_on='mousemove|click', #同时鼠标移动和点击时触发。
            ),
            # toolbox_opts=opts.ToolboxOpts(
            #     is_show=True,  # 是否显示提示框组件，包括提示框浮层和axisPointer。
            # )
        )
        .render('./templates/多国累计确诊趋势折线图.html')
    )
    # print('多国累计确诊趋势完成')



def main():
    url = 'https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country='
    countryList =['意大利','伊朗','西班牙','美国','德国','英国','法国','日本本土']
    for i in countryList:
        # print(i)
        s = urllib.parse.quote(i) # urlencode
        urls = url  + s
        # print(i,urls)
        downdata(i,urls)

    country_line()




if __name__ == '__main__':
    main()