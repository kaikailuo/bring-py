## 答案示例

```python
a=int(input("树苗开始编号是："))
b=int(input("树苗结束编号是："))
s=0
for i in range(a,b+1):
if i% 2==1:
   s=s+1
print("小明要安装的支架是：",s, "个")
```