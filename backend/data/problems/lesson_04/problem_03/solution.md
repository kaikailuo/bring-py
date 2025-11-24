### 答案示例

```python
x = int(input())
fee = 15 + max(0, x - 1) * 10
if fee >= 100:
    fee *= 0.9
fee = round(fee, 1)
print(fee)
```
