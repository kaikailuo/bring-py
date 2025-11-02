## 答案示例

```python
n = int(input("请输入桥梁的数量："))
t = 0
max_val = 0
for i in range(1, n+1):
    a = int(input("第" + str(i) + "个桥梁承重量："))
    if a >= 250:
        t += 1
    if a > max_val:
        max_val = a
b = round(t / n * 100, 1)
print("合格作品百分比：", b, "%")
print("最大承重量：", max_val)
```