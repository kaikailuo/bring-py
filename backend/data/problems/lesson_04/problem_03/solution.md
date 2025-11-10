## 答案示例

```python
x=int(input("请输入包裹重量（正整数，
千克）："))
y=15+(x-1)*10
if y<=100:
s=y
else:
s=y*0.9
print("需要支付的快递费为：",s,"元")
```