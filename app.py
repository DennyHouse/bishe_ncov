import string

from flask import Flask as _Flask, jsonify, redirect
from flask import render_template
from flask.json import JSONEncoder as _JSONEncoder
import decimal

from jieba.analyse import extract_tags

import utils
import datetime
from world import world_map
from manycountry import main
from globalStais import World_ncov

class JSONEncoder(_JSONEncoder):
        def default(self, o):
            if isinstance(o, decimal.Decimal):
                return float(o)
            super(_JSONEncoder, self).default(o)

class Flask(_Flask):
    json_encoder = JSONEncoder


app = Flask(__name__)


@app.route('/hello')
def hello_world():
    return 'Hello World!'

@app.route('/')
def hello_word3():
    return render_template("mian.html")

@app.route('/time')
def get_time():
    return utils.get_time()

@app.route('/c1')
def get_c1_data():
    data = utils.get_c1_data()
    return jsonify({"confirm":data[0],"suspect":data[1],"heal":data[2],"dead":data[3]})

@app.route('/c2')
def get_c2_data():
    res = []
    for tup in utils.get_c2_data():
        res.append({"name":tup[0],"value":int(tup[1])})
    return jsonify({"data":res})

@app.route('/l1')
def get_l1_data():
    data = utils.get_l1_data()
    day,confirm,suspect,heal,dead = [],[],[],[],[]
    for a,b,c,d,e in data[7:]:
        day.append(a.strftime("%m-%d"))
        confirm.append(b)
        suspect.append(c)
        heal.append(d)
        dead.append(e)
    return jsonify({"day":day,"confirm":confirm,"suspect":suspect,"heal":heal,"dead":dead})

@app.route('/l2')
def get_l2_data():
    data = utils.get_l2_data()
    day,confirm_add,suspect_add = [],[],[]
    for a,b,c in data[7:]:
        day.append(a.strftime("%m-%d"))
        confirm_add.append(b)
        suspect_add.append(c)
    return jsonify({"day":day,"confirm_add":confirm_add,"suspect_add":suspect_add})

@app.route('/r1')
def get_r1_data():
    data = utils.get_r1_data()
    city = []
    confirm = []
    for k,v in data:
        city.append(k)
        confirm.append(int(v))
    return jsonify({"city": city,"confirm": confirm})

@app.route('/r2')

def get_r2_data():
    data = utils.get_r2_data()
    d = []
    for i in data:
        k = i[0].rstrip(string.digits)
        v = i[0][len(k):]
        ks = extract_tags(k)
        for j in ks:
            if not j.isdigit():
                d.append({"name": j,"value": v})
    return jsonify({"kws": d})

@app.route('/shuju')
def map_world():
    url = 'https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist'
    world_map(url)
    return render_template('各国数据(%s).html'%(datetime.date.today()))

@app.route('/index')
def index():
    return redirect(map_world)

#多国累计确诊趋势折线图
@app.route('/manycounrtry')
def manyCountry():
    main()
    return render_template('多国累计确诊趋势折线图.html')

wn = World_ncov()


#今日新增 countryAddConfirmRankList 国家
@app.route('/counrtryadd')
def worldCountryAdd():
    wn.countryAddConfirmRankList()
    return render_template('今日国家新增数量.html')


"""
全球除了中国的
如果要实现总的确诊人数把  name = 'confirm'
全球每日死亡折线图name = 'dead'
全球每日治愈折线图name = 'heal'
全球每日治愈折线图name = 'newAddConfirm'

"""
#http://127.0.0.1:5000/world/info/heal/
#这种格式
@app.route('/world/info/<name>/')
def worldInfo(name):
    print(name)
    wn.globalDailyHistory(name=name)
    return render_template('全球历史%s信息.html'%name)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)