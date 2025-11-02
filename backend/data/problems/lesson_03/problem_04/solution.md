## 答案示例

```python
s = 0
n = int(input("今日到访学校："))
for i in range(1, n+1):
    a = int(input("第" + str(i) + "所学校来人："))
    s += a

if s % 40 == 0:
    b = s // 40
else:
    b = s // 40 + 1
print("今日共来人：", s)
print("今日需要安排教室：", b, "个")
```