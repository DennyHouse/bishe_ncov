import json

import pandas as pd
import requests
from pyecharts import options as opts
from pyecharts.charts import *
from pyecharts.globals import ThemeType


class World_ncov(object):
    def __init__(self):
        self.url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_foreign'

        self.countrysUrl = 'https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist'

    def getdata(self):
        r = requests.get(self.url).json()


        data = json.loads(r['data'])
        return data

    # 全球每日增加信息,总计信息绘制 绘制折线图
    """
    如果要实现总的确诊人数把  name = 'confirm'
    全球每日死亡折线图name = 'dead'
    全球每日治愈折线图name = 'heal'
    """
    def globalDailyHistory(self, name):
        """
        如果要实现总的确诊人数把 newAddConfirm改成 confirm
        """
        data = self.getdata()
        print(name)
        newAddConfirmList = []
        for i in data['globalDailyHistory'][:-1]:
            item = {
                'date': i['date'],
                name: i['all'][name]
            }
            newAddConfirmList.append(item)
        df = pd.DataFrame(newAddConfirmList)
        print(df)
        line = (
            Line()
                .add_xaxis(list(df['date']))
                .add_yaxis(series_name=name, y_axis=list(df[name]))
                .set_global_opts(
                title_opts=opts.TitleOpts(title='全球历史%s信息(不包括中国)'%name),
                datazoom_opts=opts.DataZoomOpts(
                    is_show=True,  #
                    is_realtime=True,  # 拖动时，是否实时更新系列的视图。如果设置为 false，则只在拖拽结束的时候更新。
                    range_end=80,  # 数据窗口范围的结束百分比。
                    range_start=50
                ),
                tooltip_opts=opts.TooltipOpts(
                    is_show=True,
                    trigger='axis',  # 坐标轴触发，主要在柱状图和折线图使用
                    trigger_on='mousemove|click',  # 同时鼠标移动和点击时触发。
                ),
            )
                .render('./templates/全球历史{}信息.html'.format(name))
        )


    #今日新增 countryAddConfirmRankList 国家
    def countryAddConfirmRankList(self):
        data = self.getdata()

        countryList = []
        for i in data['countryAddConfirmRankList']:
            item = {
                'nation':i['nation'],
                'addConfirm':i['addConfirm']
            }
            countryList.append(item)
        df = pd.DataFrame(countryList)

        #Bar翻转xy轴
        bar = (
            Bar()
            .add_xaxis(list(df['nation']))
            .add_yaxis('国家新增数量',list(df['addConfirm']))
            .reversal_axis() #翻转xy轴
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))
            .set_global_opts(title_opts=opts.TitleOpts(title="今日新增国家数量"))
            .render("./templates/今日国家新增数量.html")
        )


if __name__ == '__main__':
    wn = World_ncov()

    """
    如果要实现总的确诊人数把  name = 'confirm'
    全球每日死亡折线图name = 'dead'
    全球每日治愈折线图name = 'heal'
    """
    wn.globalDailyHistory('heal')

    # 今日新增 countryAddConfirmRankList 国家
    wn.countryAddConfirmRankList()