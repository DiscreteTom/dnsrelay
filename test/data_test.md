            add测试
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
print(data)# add  a record to self.data
import yaml
#d = {'www.baidu.com':['39.156.66.18']} 
# save current data to data file
#f = open('add_find.yaml', 'w', encoding='utf-8')
#yaml.safe_dump(d, f)
#f.close()


print("请输入url.")
url = input()
print("请输入ip地址")
ip = input()

#load data
f = open('add_find.yaml', encoding='utf-8')
data = yaml.safe_load(f)
f.close()

# change data
if url in data:
    print("url已存在")
else    :
    data[url] = [ip]

#write
f = open('add_find.yaml', 'w', encoding='utf-8')
yaml.safe_dump(data, f)
f.close()

#test the result
f = open('add_find.yaml', encoding='utf-8')
data = yaml.safe_load(f)
print(data)



测试结果及截图：
(1)插入一个已存在的url：
add_test1.png
(2)插入一个新的url和对应ip:
add_test2.png





		add_init测试
源代码：
#add_init
import yaml
d = {'www.baidu.com':['39.156.66.18','39.156.66.19']} 
# save current data to data file
f = open('add_find.yaml', 'w', encoding='utf-8')
yaml.safe_dump(d, f)
f.close()

#test the result
f = open('add_find.yaml', encoding='utf-8')
data = yaml.safe_load(f)
print(data)

截图：
初始化数据文件内容：
add_init.png



            find测试
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

print('请输入要查找的url')
url = input()

if url in data :
	print(data[url])
else:
	print('找不到ip地址')




截图：
(1)查找成功：
find_test1.png
(2)查找失败：
find_test2.png







