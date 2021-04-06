from bs4 import BeautifulSoup

html = """
<html>
<head><title>黑马程序员</title></head>
<body>
<p id="test01">软件测试</p>
<p id="test02">2020年</p>
<a href="/api.html">接口测试</a>
<a href="/web.html">Web自动化测试</a>
<a href="/app.html">APP自动化测试</a>
</body>
</html>
"""

soup = BeautifulSoup(html,"html.parser")

# 获取title标签元素
print(soup.title)
# 获取title标签的内容值
print(soup.title.string)

# 获取第一个p标签
print(soup.p)
# 获取第一个P标签的内容值
print(soup.p.string)
# 获取第一个p标签的属性ID的值
print(soup.p["id"])
# 获取所有的P标签
print(soup.find_all("p"))

# 获取所有A标签的href属性的值以及标签内容值
for i in soup.find_all("a"):
    print("href = {} , 内容值为：{}".format(i["href"],i.string))