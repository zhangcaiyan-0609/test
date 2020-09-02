"""
re模块:使用正则表达式的官方库
方法:
re.search():匹配第一个符合规范的数据,返回一个匹配对象,找不到的返回None
re.match()
re.findall():查找匹配的所有元素,以列表的形式返回
re.sub()
--------------单字符(元字符)--------------
1 .:表示匹配任意一个字符(除了\n外)
2 [abc]:列举可以匹配的字符
3 \d:匹配任意一个数字
4 \D:匹配任意一个非数字
5 \s:匹配任意一个空白字符(空格 tab键 换行符)
6 \S:匹配任意一个非空白字符
7 \w:匹配任意一个单词字符(数字,字母,下划线)
8 \W:匹配任意一个非单词字符

-------------字符数量的表示-------------
1.{n}:表示前一个字符连续出现n次
2.{n,m}:表示前一个字符连续出现n到m次
3.{n,}:表示前一个字符连续出现至少n次以上
4.+:表示前一个字符至少出现1次以上
5.*:表示前一个字符至少出现0次以上

贪婪模式:python中正则匹配数量的时候,默认是贪婪模式
非贪婪模式:在表示数量范围的后面加个?,就可以关闭贪婪模式,?跟在数量范围后面
常见的数量范围有:{n,m},{3,},+,*
-------------字符边界的表示-----------------
1.^:表示字符串开头
2.$:表示字符串结尾
3.\b:表示单词边界(空格,标点,-)
4.\B:表示非单词边界
5.|:表示匹配多个规则
写匹配表达式的时候,尽量前面加个r防止字符串发生转义
\n:换行
\b:backspace
------------分组的表示------------------

1.|:表示匹配多个规则
# 匹配3个数字或者3个字母
res19 = re.findall("[a-z]{3}|\d{3}","aaa11144444bbbbccc")
print(res19)
2.():表示分组
必须掌握的一个分组
data ='{"member_id":"#member_id#","pwd":"#pwd#","uesr":"#user#","loan_id":"#loan_id#"}'
res20 = re.findall("#(.*?)#",data)
print(res20)
['member_id', 'pwd', 'user', 'loan_id']
# 多个分组
# 扩展:一个匹配规则中提取多组数据
res = re.findall(".+?#(.+?)#.+?#(.+?)#.+?#(.+?)#.+?#(.+?)#",data)
print(res)
[('member_id', 'pwd', 'user', 'loan_id')]

--------正则替换参数的应用----------------
1. re.search():匹配第一个符合规则的数据,返回一个匹配对象(字符串)
res21 = re.search("#(.+?)#",data)
print(res21)
#从匹配的对象中提取匹配的内容
group()获取匹配到的数据
print(res21.group())
group(1):获取匹配到的数据中的第X个分组中的内容
res22 = re.search("#(.+?)#",data)
print(res22)
# 提取分组里面的内容,第几个分组,就传多少
print(res22.group(1))
2. re.match():匹配第一个符合规则的数据(必须是在字符串的开头位置),返回一个匹配对象,匹配不到,返回None
3. re.sub():替换





#需求一:匹配如下数据中的手机号:adddffffedf17610772806ddfdfdf
s = "adddffffedf17610772806ddfdfdf"
res1 = re.findall("\d{11}",s)
print(res1)

res2 = re.findall(".",s)
print(res2)

res3 = re.findall("[0-9a-zA-Z]",s)
print(res3)

res4 = re.findall("\d",s)
print(res4)

res5 = re.findall("\D",s)
print(res5)

ss = "adddfff   fedf17610772806d    dfdfdf"
res6 = re.findall("\s",ss)
print(res6)

res7 = re.findall("\S",ss)
print(res7)

res8 = re.findall("\w",ss)
print(res8)

res9 = re.findall("\w",ss)
print(res9)

res10 = re.findall("\d{3,5}","123aaa1111bb2323fs555555")
print(res10)

res11 = re.findall("\d{3,}?","123aaa1111bb2323fs555555")
print(res11)

res12 = re.findall("\d+","123aaa1111bb2323fs555555")
print(res12)

data ='{"member_id":"#member_id#","pwd":"#pwd#"}'
res13 = re.findall("#.+?#",data)
res14 = re.findall("#.*?#",data)
print(res13)
print(res14)

res15 = re.findall("^python","python?-00-java--php-python")
print(res15)

res16 = re.findall("python$","python-00-java--php-python")
print(res16)

res17 = re.findall(r"\bpython\b","python-00-java--php-python")
print(res17)

res18 = re.findall(r"python\B","python-00-java--php-python")
print(res18)

res19 = re.findall("[a-z]{3}|\d{3}","aaa11144444bbbbccc")
print(res19)
"""
import re
data ='{"member_id":"#member_id#","pwd":"#pwd#","user":"#user#","loan_id":"#loan_id#"}'
'''
res20 = re.findall("#(.*?)#",data)
# 扩展
res = re.findall(".+?#(.+?)#.+?#(.+?)#.+?#(.+?)#.+?#(.+?)#",data)
print(res)
#2 re.search匹配
res21 = re.search("#.+?#",data)
print(res21)
#从匹配的对象中提取匹配的内容
print(res21.group())
res22 = re.search("#(.+?)#",data)
print(res22)
# 提取分组里面的内容,第几个分组,就传多少
print(res22.group(1))

#3.替换,count=0,默认替换所有符合规则的字符
class EnvData:
    member_id = 123
    user = "cathy"
    pwd = "lemonban"
    loan_id =31
import re
data22 = re.sub("#.+?#",str(EnvData.member_id),data,count=1)
'''
import re
data ='{"member_id":"#member_id#","pwd":"#pwd#","user":"#user#","loan_id":"#loan_id#"}'
class EnvData:
    member_id = 123
    user = "cathy"
    pwd = "lemonban"
    loan_id =31
item = re.search("#(.+?)#",data)
# 需要替换的数据
rep_data = item.group()
print(rep_data)
# 要替换的类属性
key = item.group(1)
value = getattr(EnvData,key)
print(attr,value)
data = data.replace(rep_data,str(value))
print(data)

