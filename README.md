# QPSK Monte Carlo Communication Project

这是一个通信原理课设，主线是 **QPSK 链路的蒙特卡洛仿真与理论验证**。图像和 CV 只作为业务层载荷，用来展示通信链路在一个实际应用中的用法。

## 一句话说明

发送随机比特，经过 QPSK 调制和 AWGN、Rayleigh 或 Rician 信道，接收端做信道均衡、硬判决和 Viterbi 解码，最后用 BER 曲线、理论公式和置信区间验证仿真器是否可信。

## 运行方式

在 MATLAB R2025b 中运行：

```matlab
cd('你的本地路径/QPSK/matlab')
run_project_v3
```

也可以在 macOS 终端中运行：

```bash
/Applications/MATLAB_R2025b.app/bin/matlab -batch \
  "cd('你的本地路径/QPSK/matlab'); run_project_v3"
```

脚本会重新生成 `data/` 和 `figures/` 中的结果。

## 代码从哪里看

主入口是 [matlab/run_project_v3.m](matlab/run_project_v3.m)。建议按下面顺序阅读：

| 代码区域 | 作用 |
|---|---|
| 链路预算 | 用 2.2 GHz、600 km 的简化 LEO 参数确定 SNR 范围 |
| `qpskChannel` | QPSK 映射、噪声、AWGN/Rayleigh/Rician 衰落、信道估计和均衡 |
| `convEncode` | rate-1/2 卷积编码，生成多项式 111 和 101 |
| `viterbiDecode` | 四状态硬判决 Viterbi 解码 |
| BER 主循环 | 扫描 `Eb/N0 = 0:2:16 dB`，每个点统计 336,000 个信息比特 |
| `transmitImage` | 把固定 6 bit 和自适应 4/8 bit 图像载荷放进同一条 QPSK 链路 |

## 关键实验

### 1. 理论 BER 验证

- AWGN QPSK 理论线使用 `Q(sqrt(2Eb/N0))`
- Rayleigh 理论线使用 `0.5(1 - sqrt(γ/(1+γ)))`
- 仿真点附带 95% 置信区间
- Rician 采用真正的直射分量

```matlab
h = sqrt(K/(K+1)) + ...
    sqrt(1/(K+1)) * (randn + 1i*randn) / sqrt(2)
```

### 2. 信道编码

未编码和编码链路使用相同的 `Eb/N0` 横轴。编码链路的噪声标定包含码率 `R=1/2`，接收端统计的是信息比特 BER。

### 3. 波形证据

`figures/03_waveform.png` 给出接收 QPSK 星座图和归一化频谱，说明 signaling waveform 确实进入了实验。

### 4. 图像业务层

CV 模块按 8×8 图像块计算梯度复杂度，让部分块使用 4 bit、部分块使用 8 bit。它和固定 6 bit 方案共享同一个 QPSK、Rician 和 `Eb/N0` 设置，因此业务层比较不会改变通信主线。

## 结果文件

- [data/ber_validation.csv](data/ber_validation.csv) 包含三种信道、编码/未编码、BER、置信区间和总比特数
- [data/link_budget.csv](data/link_budget.csv) 包含简化链路预算
- [data/application_layer.csv](data/application_layer.csv) 包含图像业务层的 BER、PSNR 和有效传输量
- [figures/01_theory_validation.png](figures/01_theory_validation.png)
- [figures/02_coding_gain.png](figures/02_coding_gain.png)
- [figures/03_waveform.png](figures/03_waveform.png)
- [figures/04_application_reconstruction.png](figures/04_application_reconstruction.png)

## 汇报材料

- [ppt/QPSK_看懂链路版.pptx](ppt/QPSK_看懂链路版.pptx)
- [ppt/speaker_notes_v5.md](ppt/speaker_notes_v5.md)

PPT 按 16 页组织，建议用 12–15 分钟讲完。主讲顺序是链路结构、Eb/N0、信道模型、理论验证、编码增益、波形证据，最后再讲 CV 图像业务层。

## 可视化版说明

`ppt/QPSK_看懂链路版.pptx` 使用 PingFang SC 中文字体，适合在 macOS PowerPoint 中打开。它增加了链路总图、QPSK 星座解释、信道幅度分布、卷积码流程、Viterbi 状态图和 15 分钟时间轴。
