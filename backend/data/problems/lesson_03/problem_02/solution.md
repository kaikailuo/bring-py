## 答案示例

```python
s = 0
n = int(input())
for i in range(1, n+1):
    a = int(input())
    s += a
if s % 500 == 0:
    m = s // 500
else:
    m = s // 500 + 1
print(m)
```

