## 答案示例

```python
m=float(input("请输入单价（元）:"))
n=int(input("请输入数量（本）:"))
if n<100:
f=m*n
elif n<500:
f=m*0.9*n
else:
f=m*0.8*n
print("总价为：",f,"元")
```