## 答案示例

```python
n = int(input())
t = 0
max_val = 0
for i in range(1, n+1):
    a = int(input())
    if a >= 250:
        t += 1
    if a > max_val:
        max_val = a
b = round(t / n * 100, 1)
print(b)
print(max_val)
````