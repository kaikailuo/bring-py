### 答案示例

```python
m = float(input())
n = int(input())
if n < 100:
    total = m * n
elif n < 500:
    total = m * 0.9 * n
else:
    total = m * 0.8 * n
total = round(total, 1)
print(total)
```