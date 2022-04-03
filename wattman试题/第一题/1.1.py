import json
def load_json(path):
    """
    加载json文件，返回为字典
    :param path: json文件路径
    :return: json文件对应的字典
    """
    with open(path) as f:
        json_dict = json.load(f)
    return json_dict

json_path = 'boxes.json'
dic = load_json(json_path)

for box in dic['boxes']:
    if box['name'] == 'box_b':
        print('box_b:',box['rectangle'])
