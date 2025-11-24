## 答案示例

```python
n = int(input())
min_val = 99999
s = 0
for i in range(1, n+1):
    a = int(input())
    s += a
    if a < min_val:
        min_val = a
print(s)
print(min_val)
```