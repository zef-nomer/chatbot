import json
#
#data = {"sizes": [{"type": "a","val": 200}, {"type": "b","val": 500}, {"type": "c","val": 600}]}
#
#data = json.loads(data)
#
#max_item = max(data['fig']['types']['sizes'],
#               key = lambda item: int(item['val'])
#               )
#
#print("Тип с максимальным значением: %s" % max_item['type'])
#print("Максимальное значение: %s" % max_item['val'])

with open("info.json", "r") as f:
    d = json.load(f)
#d = {
#  "858585885856985": 8.2,
#  "841224131321321": 100.6
#}
print(max(d, key = lambda x: d[x]))


#import operator
# import json
# a = json.loads(...)  если json  в виде строки прилетает
#a = {
#   "858585885856985": 8.2,
#   "841224131321321": 100.6,
#    "65464651659456": 4646516
#}
#print(max(a.items(), key=operator.itemgetter(1)))
# ('841224131321321', 100.6)




