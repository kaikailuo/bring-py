## 答案示例

```python
n = int(input("小组数："))
min_val = 99999
s = 0
for i in range(1, n+1):
    a = int(input("第" + str(i) + "组木棍使用量："))
    s += a
    if a < min_val:
        min_val = a
print("共使用木棍：", s, "最少的组用量：", min_val)
```