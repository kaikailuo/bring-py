# 利用Turtle画图
高一年级信息技术学科

## 目录
1. 用Python画图需要解决的问题
2. 认识Python的Turtle工具
3. 利用Turtle绘制简单图形
4. Turtle绘图进阶
5. 项目分析与准备

---

## 一、用Python画图需要解决的问题

### 核心问题
- **在哪里画？** —— 画布
- **如何定位？** —— 坐标系
- **用什么画？** —— Turtle库函数
- **怎么画？** —— 任务分解与编程实现

### 编程画图的任务分解
- 数学直角坐标系，原点在中心
- 使用turtle库中的函数，如：`turtle.circle(30)`

---

## 二、认识Python的Turtle工具

### 1. 导入turtle库
```python
# 方法1：
import turtle
turtle.circle(50)
turtle.forward(100)

# 方法2（推荐）：
import turtle as t
t.circle(50)
t.forward(100)
### 2. 设置画布
python
t.setup(800, 600)        # 设置画布大小（宽×高，单位：像素）
t.bgcolor("lightblue")   # 设置背景色
常用颜色：red、gray、yellow、white、black、pink、purple、orange等

3. 绘图的坐标系
数学直角坐标系

原点(0,0)在窗口正中间

向右为x轴正向，向上为y轴正向

默认海龟向正右方移动（坐标正方向）

4. 画笔状态函数
python
t.pensize(5)            # 设置画笔粗细
t.pencolor("green")     # 设置画笔颜色
t.fillcolor("yellow")   # 设置填充颜色
t.shape("turtle")       # 设置画笔形状
t.hideturtle()          # 隐藏海龟
t.up()                  # 抬笔（移动时不画线）
t.down()                # 落笔（移动时画线）
5. 画笔绘图函数
python
t.forward(100)          # 前进
t.backward(50)          # 后退
t.left(90)              # 左转90度
t.right(45)             # 右转45度
t.circle(30)            # 画圆（半径30）
t.circle(40, 90)        # 画圆弧（半径40，角度90度）
t.goto(100, 50)         # 移动到指定坐标
t.begin_fill()          # 开始填充
t.end_fill()            # 结束填充
三、利用Turtle绘制简单图形
画正三角形示例
python
import turtle as t
t.pensize(5)
t.pencolor("green")
t.shape("turtle")
t.forward(90)
t.left(120)
t.forward(90)
t.left(120)
t.forward(90)
t.left(120)
填充图形示例
python
import turtle as t
t.pensize(5)
t.pencolor("green")
t.fillcolor("yellow")
t.shape("turtle")
t.bgcolor("lightgreen")

t.begin_fill()
t.forward(90)
t.left(120)
t.forward(90)
t.left(120)
t.forward(90)
t.left(120)
t.end_fill()
画图流程总结
导入turtle库

设置turtle状态

用turtle绘图

函数使用格式
text
对象名.函数名()
四、Turtle绘图进阶
1. 解决画图定位问题
问题分析：

窗口的大小

确定位置坐标

定位到指定位置

示例：画回字形

python
import turtle as t
t.pensize(5)
t.pencolor("blue")
t.hideturtle()

# 画大正方形
t.forward(100)
t.left(90)
t.forward(100)
t.left(90)
t.forward(100)
t.left(90)
t.forward(100)

# 定位到小正方形起点
t.up()
t.goto(20, 20)
t.down()

# 画小正方形
t.left(90)
t.forward(60)
t.left(90)
t.forward(60)
t.left(90)
t.forward(60)
t.left(90)
t.forward(60)
2. 使用goto直接画图
python
import turtle as t
t.pensize(5)
t.pencolor("blue")
t.hideturtle()

# 用goto画大正方形
t.goto(100, 0)
t.goto(100, 100)
t.goto(0, 100)
t.goto(0, 0)

# 画小正方形
t.up()
t.goto(20, 20)
t.down()
t.goto(80, 20)
t.goto(80, 80)
t.goto(20, 80)
t.goto(20, 20)
3. 画有规律的曲线
python
t.circle(40, 90)    # 逆时针画90度圆弧
t.circle(-40, 90)   # 顺时针画90度圆弧
t.circle(40, 90)
t.circle(-40, 90)
t.circle(40, 90)
t.circle(-40, 90)
circle函数说明：

radius：半径（正数逆时针，负数顺时针）

extent：圆弧的度数

五、项目分析与准备
1. 顺序结构
程序代码自上向下顺序执行

按照解决问题的顺序编写代码

2. 画气球案例
python
import turtle as t
t.setup(900, 500)
t.bgpic("bg32.gif")
t.pensize(5)
t.fillcolor("red")
t.pencolor("gold")
t.hideturtle()

# 定位
t.up()
t.goto(-50, -50)
t.down()

# 画线
t.left(90)
t.fd(80)

# 画圆
t.begin_fill()
t.right(90)
t.circle(30)

# 画三角形
t.right(120)
t.fd(20)
t.left(120)
t.fd(20)
t.left(120)
t.fd(20)
t.end_fill()

t.exitonclick()