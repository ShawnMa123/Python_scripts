# 在dict中筛选对应包含字符串格式的值

import re

# dict的value均是list
d_dict = {'a': ['a.BB.123', 'aa.BB.cc.asdas.adsga', 'a.BB.123'],
          'b': ['A123123123.BB.fasdfasdfa.agsdfgsdfgsdfgsdf.qwetrqwe', '1231234.BB.afdsag.ewrqwefawe234123'],
          'c': ['B1234123U']}

# 删除掉所有含有xx. BB.的多级子目录的值
filter_key_list = ['xx', 'BB']

remove_value_list = []
for key in d_dict.keys():
    for element in d_dict.get(key):
        for ignore_key in filter_key_list:
            print(f'now {element} and filter {ignore_key}')
            if ignore_key in element:
                print(f'process {element} by {ignore_key}')
                tmp_str = re.search(rf'{ignore_key}.\w+', element)
                tmp = tmp_str.group()
                if tmp:
                    if element.endswith(tmp) is False:
                        print(f'need remove {element}')
                        remove_value_list.append(element)

for remove_value in remove_value_list:
    for a in d_dict.values():
        try:
            a.remove(remove_value)
        except:
            pass

print(d_dict)
