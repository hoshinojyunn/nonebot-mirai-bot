import requests
import json

province_code = [{"code": "ABJ", "name": "北京市", "url": "/publish/forecast/ABJ.html"},
                 {"code": "ATJ", "name": "天津市", "url": "/publish/forecast/ATJ.html"},
                 {"code": "AHE", "name": "河北省", "url": "/publish/forecast/AHE.html"},
                 {"code": "ASX", "name": "山西省", "url": "/publish/forecast/ASX.html"},
                 {"code": "ANM", "name": "内蒙古自治区", "url": "/publish/forecast/ANM.html"},
                 {"code": "ALN", "name": "辽宁省", "url": "/publish/forecast/ALN.html"},
                 {"code": "AJL", "name": "吉林省", "url": "/publish/forecast/AJL.html"},
                 {"code": "AHL", "name": "黑龙江省", "url": "/publish/forecast/AHL.html"},
                 {"code": "ASH", "name": "上海市", "url": "/publish/forecast/ASH.html"},
                 {"code": "AJS", "name": "江苏省", "url": "/publish/forecast/AJS.html"},
                 {"code": "AZJ", "name": "浙江省", "url": "/publish/forecast/AZJ.html"},
                 {"code": "AAH", "name": "安徽省", "url": "/publish/forecast/AAH.html"},
                 {"code": "AFJ", "name": "福建省", "url": "/publish/forecast/AFJ.html"},
                 {"code": "AJX", "name": "江西省", "url": "/publish/forecast/AJX.html"},
                 {"code": "ASD", "name": "山东省", "url": "/publish/forecast/ASD.html"},
                 {"code": "AHA", "name": "河南省", "url": "/publish/forecast/AHA.html"},
                 {"code": "AHB", "name": "湖北省", "url": "/publish/forecast/AHB.html"},
                 {"code": "AHN", "name": "湖南省", "url": "/publish/forecast/AHN.html"},
                 {"code": "AGD", "name": "广东省", "url": "/publish/forecast/AGD.html"},
                 {"code": "AGX", "name": "广西壮族自治区", "url": "/publish/forecast/AGX.html"},
                 {"code": "AHI", "name": "海南省", "url": "/publish/forecast/AHI.html"},
                 {"code": "ACQ", "name": "重庆市", "url": "/publish/forecast/ACQ.html"},
                 {"code": "ASC", "name": "四川省", "url": "/publish/forecast/ASC.html"},
                 {"code": "AGZ", "name": "贵州省", "url": "/publish/forecast/AGZ.html"},
                 {"code": "AYN", "name": "云南省", "url": "/publish/forecast/AYN.html"},
                 {"code": "AXZ", "name": "西藏自治区", "url": "/publish/forecast/AXZ.html"},
                 {"code": "ASN", "name": "陕西省", "url": "/publish/forecast/ASN.html"},
                 {"code": "AGS", "name": "甘肃省", "url": "/publish/forecast/AGS.html"},
                 {"code": "AQH", "name": "青海省", "url": "/publish/forecast/AQH.html"},
                 {"code": "ANX", "name": "宁夏回族自治区", "url": "/publish/forecast/ANX.html"},
                 {"code": "AXJ", "name": "新疆维吾尔自治区", "url": "/publish/forecast/AXJ.html"},
                 {"code": "AXG", "name": "香港特别行政区", "url": "/publish/forecast/AXG.html"},
                 {"code": "AAM", "name": "澳门特别行政区", "url": "/publish/forecast/AAM.html"},
                 {"code": "ATW", "name": "台湾省", "url": "/publish/forecast/ATW.html"}]

"""r = requests.get(url=f'http://www.nmc.cn/rest/province/{province_code[0]["code"]}').json()
print(json.dumps(r, ensure_ascii=False, sort_keys=True, indent=4))"""

city_code = []
for province in province_code:
    r = requests.get(url=f'http://www.nmc.cn/rest/province/{province["code"]}').json()
    for i in r:
        city_code.append(i)
with open('city_code.json', 'a') as fp:
    json.dump(city_code, fp, ensure_ascii=False, sort_keys=True, indent=4)
