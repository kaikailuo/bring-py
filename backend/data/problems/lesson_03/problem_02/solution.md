## 答案示例

```python
s = 0
n = int(input("请输入教师的数量："))
for i in range(1, n+1):
    a = int(input("第" + str(i) + "位教师打印量："))
    s += a
if s % 500 == 0:
    m = s // 500
else:
    m = s // 500 + 1
print("共需要墨盒", m, "个")
```