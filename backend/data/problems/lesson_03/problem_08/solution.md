## 答案示例

```python
n = int(input("提交答案的同学一共有（名）："))
s = 0
for i in range(1,n+1):
    a = int(input("第"+str(i)+"位同学提交的答案是："))    
    if a == 3:
        s = s + 1
s=round(s/n*100,1)
print("同学们的正确率是：",s,"%")
```