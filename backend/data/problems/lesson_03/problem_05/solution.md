## 答案示例

```python
s = 0
m = 0
n = int(input())
for i in range(1, n+1):
    a = int(input())
    if a > m:
        m = a
    if a > 125:
        s += 1
print(m)
print(s)
```
