            add test
源代码：
# add  a record to self.data
import yaml
#d = {'www.baidu.com':'39.156.66.18'} 
# save current data to data file
#f = open('add_find.yaml', 'w', encoding='utf-8')
#yaml.safe_dump(d, f)
#f.close()

url = input()
ip = input()

#test whetherthe record is successfully added
f = open('add_find.yaml', encoding='utf-8')
data = yaml.safe_load(f)
f.close()

#write
data[url] = ip
f = open('add_find.yaml', 'w', encoding='utf-8')
yaml.safe_dump(data, f)
f.close()

#test the result
f = open('add_find.yaml', encoding='utf-8')
data = yaml.safe_load(f)
print(data)

截图：
add_test.png



            find test
源代码：
'''
- if `url` is found, return its ip address
- if `url` is '0.0.0.0', return '0.0.0.0'
- if `url` is not found, return empty str
'''
import yaml
f = open('add_find.yaml', encoding='utf-8')
data = yaml.safe_load(f)
f.close()
url = input()
if url == '0.0.0.0' :
	print('0.0.0.0')
elif url in data :
	print(data[url])
else:
	print('')

截图：
find_test1.png
find_test2.png
find_test3.png






