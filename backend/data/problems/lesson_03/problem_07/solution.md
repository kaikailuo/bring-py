## 答案示例

```python
s=0
for i in range(1,13):
    a=int(input(str(i)+"月获得的愿望星个数是："))
    s=s+a
print("去年小明一共获得愿望星" , s,"颗")
print("平均每个月获得的愿望星是：" , round(s/12, 1) ,"颗")
```