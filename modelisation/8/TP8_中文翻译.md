# TP 8

微分方程

ZFAI

## 练习 1（预备测试）

我们先确认 `numpy` 和 `matplotlib` 库是否正确导入。运行下面的程序：

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 1000)
y = np.sin(x)
plt.plot(x, y)
plt.show()
```

## 问题 1（Volterra-Lotka 捕食者-猎物系统）

我们想要模拟下面的方程组：

```text
x'(t) = a x(t) - b x(t)y(t)
y'(t) = -c y(t) + d x(t)y(t)
```

初始条件为：

```text
(x(0), y(0)) = (x0, y0)
```

取参数：

```text
a = 3, b = 2, c = 2, d = 3
x0 = 3/2, y0 = 3/4
```

1. 记 `X(t) = (x(t), y(t))` 为解，并把上面的微分方程写成：

```text
X'(t) = F(X(t))
```

命令 `np.array([x,y])` 可以生成数组 `[x,y]`。  
编写函数 `FVL(X)`，输入 `X = array([x,y])`，返回：

```text
(ax - bxy, -cy + dxy)
```

返回格式为 `np.array`。

2. 下面的函数用通用方式实现 Euler 格式，可以用于任意函数 `F`：

```python
def Euler(F,X0,T,N):
    h=T/N
    n=np.size(X0)
    S=np.zeros((n,N+1))
    S[:,0]=X0
    Xn=X0
    for i in range(N):
        Xn+=h*F(Xn)
        S[:,i+1]=Xn
    return S
```

用捕食者-猎物模型函数 `FVL` 测试它，取：

```text
X0 = (3/2, 3/4), T = 3, N = 100
```

3. 用两种形式绘图：

- 随时间 `t` 变化的 `x(t)` 和 `y(t)`；
- 相平面中的轨迹 `(x(t), y(t))`。

4. 实现二阶 Runge-Kutta 格式：

```text
X_(n+1) = X_n + h F(X_n + h/2 F(X_n))
```

写成通用函数：

```python
RK2(F,X0,T,N)
```

并测试。

5. 实现二阶 Adams-Bashforth 格式：

```text
X_(n+1) = X_n + h/2 (3F(X_n) - F(X_(n-1)))
```

写成通用函数：

```python
AB2(F,X0,T,N)
```

可以用 RK2 做第一步。然后测试。

6. 实现四阶 Runge-Kutta 格式：

```text
k0 = F(X_n)
k1 = F(X_n + h/2 k0)
k2 = F(X_n + h/2 k1)
k3 = F(X_n + h k2)

k = k0/6 + k1/3 + k2/3 + k3/6
X_(n+1) = X_n + h k
```

写成通用函数：

```python
RK4(F,X0,T,N)
```

并测试。

7. Newton 算法可以求解非线性方程：

```text
G(X) = 0
```

迭代为：

```text
X^0 = X_n
X^(k+1) = X^k - DG(X^k)^(-1) G(X^k)
```

实现隐式 Euler 格式：

```text
X_(n+1) = X_n + h F(X_(n+1))
```

函数形式为：

```python
IEuler(F,DF,X0,T,N)
```

其中 `DF` 是 `F` 的 Jacobi 矩阵，也就是由偏导数组成的矩阵。  
可以使用：

```python
np.linalg.solve(np.array([[...],...,[...]]), np.array([...]))
np.eye(n)
```

8. 实现 Crank-Nicholson 格式：

```text
X_(n+1) = X_n + h/2 (F(X_n) + F(X_(n+1)))
```

函数形式为：

```python
CN(F,DF,X0,T,N)
```

9. 对这些不同格式（显式和隐式），绘制第一积分：

```text
H(x,y) = d x - c ln(x) + b y - a ln(y)
```

## 进一步内容

## 问题 2（Lorenz 奇异吸引子）

考虑下面的微分方程组：

```text
y1'(t) = sigma (y2(t) - y1(t))
y2'(t) = r y1(t) - y2(t) - y1(t)y3(t)
y3'(t) = y1(t)y2(t) - b y3(t)
```

初始条件为：

```text
(y1(0), y2(0), y3(0)) = (1, 0, 0)
```

取参数：

```text
sigma = 10, b = 8/3, r = 28
```

1. 对 `0 ≤ t ≤ 100`，分别用显式 Euler、Runge-Kutta 2、Runge-Kutta 4 格式实现并绘制数值解：

```text
(y1(t), y2(t), y3(t))
```

绘图包括：

- 随时间变化的图像；
- 相平面 `(y1,y3)` 中的轨迹。

2. 对下面三项分别做约 `10^(-8)` 的小扰动：

- 初始条件 `(y1(0), y2(0), y3(0))`；
- `sigma`；
- 时间步长 `h`。

对不同数值格式绘图并比较结果。
