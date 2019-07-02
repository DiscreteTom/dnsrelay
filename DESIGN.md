# 设计

## 需求

## 功能设计

## 模块划分

### 模块划分图

![modules](img/modules.png)

### dnsrelay模块

负责命令行参数与选项的处理

### net模块

负责：
- 网络通信，包括直接回复客户端和向DNS服务器查询后回复客户端
- 数据包内数据与python内置数据类型dict的转换

### processor模块

负责对dict类型的数据包进行解析，根据协议作出一些行为。需要并发处理

### data模块

负责维护数据与文件，在给定域名时对IP地址进行查找

## 软件流程图

### 包数据格式

此处定义了把DNS报文解析为python的内置类型dict时dict的数据格式，用来作为Processor.parse/NetController.reply/NetController.query三个函数的参数使用

```python
data = {
	'address': {
		'ip': str,
		'port':int
	},
	'data': {
		'header': {
			'id': bytes,
			'qr': bool,
			'opcode': int,
			'aa': bool,
			'tc': bool,
			'rd': bool,
			'ra': bool,
			'rcode': int,
			'qdcount': int,
			'ancount': int,
			'nscount': int,
			'arcount': int
		},
		'question': [{
			'qname': bytes,
			'qtype': int,
			'qclass': int
		}],
		'answer': [{
			'name': bytes,
			'type': int,
			'class': int,
			'ttl': int,
			'rdlength': int,
			'rdata': bytes
		}],
		'authority': [{ # same as the format of data['answer']
			'name': bytes,
			'type': int,
			'class': int,
			'ttl': int,
			'rdlength': int,
			'rdata': bytes
		}],
		'additional': [{ # same as the format of data['answer']
			'name': bytes,
			'type': int,
			'class': int,
			'ttl': int,
			'rdlength': int,
			'rdata': bytes
		}]
	}
}
```

其中`name`或`qname`字段可能以`0b11`开头，表示引用包内其他名称。也可能为正常的字符串。如果是正常的字符串，则串尾包含`\0`

### 并发设计

每次NetController接收到一个新的请求，都会调用Processor.parse。Processor.parse被调用后创建一个解析包的进程或线程后立即返回以防止NetController阻塞。因为parse可能调用Data.add引起Data内部数据的改变，所以需要对Data实例进行加锁保护。因为并行的Processor.parse可能同时多次调用NetController.reply或NetController.query，而NetController.query与NetController.reply会写发送缓冲区，所以Processor调用NetController.reply和NetController.query的时候也需要加锁。并发控制完全由Processor模块负责

### 正常检索地址

![normal](img/normal.png)

### 检索不良地址

![bad](img/bad.png)

### 未检索到地址

![query](img/query.png)

## 测试用例以及运行结果

### 单元测试

- 测试net模块
  - packageToDict函数测试用例：见`test/packageToDict.bin`
  - dictToPackage函数把packageToDict函数生成的dict再转换为bytes和`test/packageToDict.bin`文件对比

### 集成测试

## 遇到的问题与解决
