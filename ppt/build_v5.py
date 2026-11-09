from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT=Path('/Users/lljk/Desktop/专业课/计算机视觉/QPSK'); FIG=ROOT/'figures'; OUT=ROOT/'ppt'/'QPSK_看懂链路版.pptx'; OUT.parent.mkdir(exist_ok=True)
# Generate an extra visual that explains the three channel distributions
np.random.seed(7); g=(np.random.randn(10000)+1j*np.random.randn(10000))/np.sqrt(2); hR=np.sqrt(10/11)+np.sqrt(1/11)*g
plt.figure(figsize=(9,3.2));
for vals,lab,col in [(np.abs(g),'Rayleigh','#e8893a'),(np.abs(hR),'Rician K=10dB','#319a68')]: plt.hist(vals,bins=80,density=True,histtype='step',linewidth=2,label=lab,color=col)
plt.xlabel('channel amplitude |h|'); plt.ylabel('density'); plt.title('LOS component shifts the amplitude distribution'); plt.grid(alpha=.25); plt.legend(); plt.tight_layout(); plt.savefig(FIG/'05_channel_distributions.png',dpi=180); plt.close()

prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5); blank=prs.slide_layouts[6]
BG=RGBColor(247,249,252); NAVY=RGBColor(16,31,54); BLUE=RGBColor(26,103,196); CYAN=RGBColor(54,178,205); ORANGE=RGBColor(236,133,53); GREEN=RGBColor(55,157,104); RED=RGBColor(196,72,72); GREY=RGBColor(83,100,120); LIGHT=RGBColor(226,234,243); WHITE=RGBColor(255,255,255); FONT='PingFang SC'

def bg(s,idx,title,sub=''):
 s.background.fill.solid(); s.background.fill.fore_color.rgb=BG
 band=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,0,0,Inches(13.333),Inches(.14)); band.fill.solid(); band.fill.fore_color.rgb=BLUE; band.line.fill.background()
 t=s.shapes.add_textbox(Inches(.65),Inches(.42),Inches(12),Inches(.45));p=t.text_frame.paragraphs[0];p.text=title;p.font.name=FONT;p.font.size=Pt(25);p.font.bold=True;p.font.color.rgb=NAVY
 if sub: q=s.shapes.add_textbox(Inches(.67),Inches(.89),Inches(12),Inches(.22));p=q.text_frame.paragraphs[0];p.text=sub;p.font.name=FONT;p.font.size=Pt(8);p.font.bold=True;p.font.color.rgb=BLUE
 f=s.shapes.add_textbox(Inches(12.3),Inches(7.08),Inches(.55),Inches(.2));p=f.text_frame.paragraphs[0];p.text=f'{idx:02d}';p.font.name=FONT;p.font.size=Pt(9);p.font.color.rgb=GREY;p.alignment=PP_ALIGN.RIGHT

def tx(s,x,y,w,h,text,size=17,color=NAVY,bold=False,align=None,font=FONT):
 t=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h));tf=t.text_frame;tf.word_wrap=True;tf.margin_left=0;tf.margin_right=0;p=tf.paragraphs[0];p.text=text;p.font.name=font;p.font.size=Pt(size);p.font.color.rgb=color;p.font.bold=bold;p.alignment=align or PP_ALIGN.LEFT;return t

def card(s,x,y,w,h,title,body,color=BLUE,size=15):
 sh=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h));sh.fill.solid();sh.fill.fore_color.rgb=WHITE;sh.line.color.rgb=LIGHT
 strip=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(.07),Inches(h));strip.fill.solid();strip.fill.fore_color.rgb=color;strip.line.fill.background()
 t=s.shapes.add_textbox(Inches(x+.22),Inches(y+.14),Inches(w-.4),Inches(.3));p=t.text_frame.paragraphs[0];p.text=title;p.font.name=FONT;p.font.size=Pt(13);p.font.bold=True;p.font.color.rgb=color
 b=s.shapes.add_textbox(Inches(x+.22),Inches(y+.53),Inches(w-.42),Inches(h-.65));tf=b.text_frame;tf.word_wrap=True;p=tf.paragraphs[0];p.text=body;p.font.name=FONT;p.font.size=Pt(size);p.font.color.rgb=NAVY;p.line_spacing=1.04

def arrow(s,x1,y1,x2,y2,color=BLUE):
 ln=s.shapes.add_connector(1,Inches(x1),Inches(y1),Inches(x2),Inches(y2));ln.line.color.rgb=color;ln.line.width=Pt(2.5);ln.line.end_arrowhead=True

def dot(s,x,y,r,color):
 sh=s.shapes.add_shape(MSO_SHAPE.OVAL,Inches(x-r),Inches(y-r),Inches(2*r),Inches(2*r));sh.fill.solid();sh.fill.fore_color.rgb=color;sh.line.color.rgb=color

def code(s,x,y,w,h,text):
 sh=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h));sh.fill.solid();sh.fill.fore_color.rgb=NAVY;sh.line.color.rgb=RGBColor(45,70,101)
 t=s.shapes.add_textbox(Inches(x+.18),Inches(y+.12),Inches(w-.35),Inches(h-.2));tf=t.text_frame;tf.word_wrap=True;p=tf.paragraphs[0];p.text=text;p.font.name='Menlo';p.font.size=Pt(11);p.font.color.rgb=RGBColor(217,237,243);p.line_spacing=1.0

# 1 hero
s=prs.slides.add_slide(blank);s.background.fill.solid();s.background.fill.fore_color.rgb=BG
bar=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,0,0,Inches(13.333),Inches(.16));bar.fill.solid();bar.fill.fore_color.rgb=BLUE;bar.line.fill.background()
tx(s,.75,.95,11.9,.55,'这套课设到底在做什么？',31,NAVY,True)
tx(s,.78,1.75,11.5,.65,'验证一条 QPSK 通信链路，观察信道和编码如何改变可靠性。',24,BLUE,True)
# hero path
for x,lab,sub,c in [(1.0,'信息比特','101100…',CYAN),(3.95,'QPSK','2 bit → 1 symbol',BLUE),(6.9,'Rician 信道','h·s+n',ORANGE),(9.85,'接收端','BER / PSNR',GREEN)]:
 card(s,x,3.2,2.3,1.5,lab,sub,c,16)
arrow(s,3.35,3.95,3.85,3.95);arrow(s,6.3,3.95,6.8,3.95);arrow(s,9.25,3.95,9.75,3.95)
card(s,1.0,5.55,3.45,.9,'主线','理论 BER → 仿真 BER',CYAN,15);card(s,4.95,5.55,3.45,.9,'通信深度','Rician → 卷积码',ORANGE,15);card(s,8.9,5.55,3.45,.9,'业务亮点','CV 自适应图像源',GREEN,15)
tx(s,.8,6.82,11,.2,'开场直接说这句话，观众就知道你要讲什么。',10,GREY)
# 2 visual overview
s=prs.slides.add_slide(blank);bg(s,2,'一眼看懂：数据怎么走','每一个箭头都对应代码中的一个阶段')
# large numbered flow
stages=[('1','源','随机比特或图像块',CYAN),('2','调制','QPSK 映射',BLUE),('3','信道','AWGN / Rayleigh / Rician',ORANGE),('4','接收','ĥ 均衡 + 硬判决',GREEN),('5','评价','BER、置信区间、PSNR',RED)]
xs=[.65,3.1,5.55,8.0,10.45]
for (n,lab,body,c),x in zip(stages,xs):
 dot(s,x+.45,2.0,.27,c);tx(s,x+.32,1.82,.28,.25,n,12,WHITE,True,PP_ALIGN.CENTER);card(s,x,2.35,1.95,2.1,lab,body,c,15)
for x in [2.65,5.1,7.55,10.0]: arrow(s,x,3.4,x+.38,3.4)
card(s,2.0,5.3,9.3,.95,'一句话','先证明第 3～5 步的通信链路可信，再把图像业务接到第 1 步。',BLUE,17)
# 3 modulation visual
s=prs.slides.add_slide(blank);bg(s,3,'QPSK 在做什么？','两个 bit 组合成一个复数符号')
# bit timeline
for i,(lab,c) in enumerate([('00',BLUE),('01',CYAN),('11',GREEN),('10',ORANGE)]):
 x=1.0+i*1.35; card(s,x,1.55,1.0,.8,lab,'',c,18)
 tx(s,x+1.03,1.75,.25,.2,'→',20,GREY,True,PP_ALIGN.CENTER)
# constellation manually
cx,cy=4.2,4.0; ax=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(2.6),Inches(2.55),Inches(3.2),Inches(3.0));ax.fill.solid();ax.fill.fore_color.rgb=WHITE;ax.line.color.rgb=LIGHT
arrow(s,2.8,4.05,5.45,4.05,GREY);arrow(s,4.2,5.35,4.2,2.75,GREY)
pts=[(3.45,3.3,'00',BLUE),(4.95,3.3,'01',CYAN),(4.95,4.8,'11',GREEN),(3.45,4.8,'10',ORANGE)]
for x,y,lab,c in pts: dot(s,x,y,.12,c);tx(s,x+.14,y-.08,.45,.2,lab,12,c,True)
tx(s,2.85,5.6,2.8,.2,'I + jQ 平面',13,GREY,False,PP_ALIGN.CENTER)
code(s,6.45,1.55,5.55,2.2,'s = [(2b₁−1) + j(2b₂−1)] / √2\n\n每个 symbol 携带 2 个 bit\n所以横轴要使用信息 bit 的 Eb/N0')
card(s,6.45,4.15,5.55,1.3,'你要讲的重点','QPSK 不是四条独立线路，而是把两个 bit 绑成一个复数点，再一起穿过信道。',BLUE,17)
# 4 channel visual
s=prs.slides.add_slide(blank);bg(s,4,'信道到底做了什么？','同一个 QPSK 符号，经过不同信道会变成不同样子')
s.shapes.add_picture(str(FIG/'05_channel_distributions.png'),Inches(.75),Inches(1.4),width=Inches(6.3),height=Inches(2.3))
card(s,7.35,1.4,2.35,1.25,'AWGN','只加噪声，h=1。',CYAN,16)
card(s,9.95,1.4,2.35,1.25,'Rayleigh','没有直射径，幅度会深衰落。',ORANGE,15)
card(s,7.35,2.95,4.95,1.25,'Rician K=10 dB','h = LOS + diffuse scatter。直射径让幅度分布向右移动。',GREEN,16)
# signal mini diagram
for x,lab,c in [(1.0,'原始点',BLUE),(3.65,'衰落后',ORANGE),(6.3,'均衡后',GREEN)]:
 ax=s.shapes.add_shape(MSO_SHAPE.OVAL,Inches(x),Inches(4.55),Inches(1.35),Inches(1.35));ax.fill.solid();ax.fill.fore_color.rgb=WHITE;ax.line.color.rgb=c
 dot(s,x+.68,5.22,.12,c);tx(s,x+.18,5.95,1.0,.25,lab,13,c,True,PP_ALIGN.CENTER)
arrow(s,2.45,5.22,3.45,5.22);arrow(s,5.1,5.22,6.1,5.22)
card(s,7.9,4.55,4.3,1.35,'接收机动作','用估计的 ĥ 除掉旋转和幅度变化，再判断点落在哪个象限。',BLUE,16)
# 5 theory plot
s=prs.slides.add_slide(blank);bg(s,5,'第一张证据图：理论和仿真对上了','这一页证明通信仿真器本身可信')
s.shapes.add_picture(str(FIG/'01_theory_validation.png'),Inches(.55),Inches(1.35),width=Inches(8.55),height=Inches(3.8))
card(s,9.4,1.4,3.05,1.2,'AWGN','蓝色点贴住 AWGN 理论线。',CYAN,16)
card(s,9.4,2.85,3.05,1.2,'Rayleigh','橙色点贴住 Rayleigh 理论线。',ORANGE,16)
card(s,9.4,4.3,3.05,1.2,'Rician','绿色曲线因为有 LOS，性能更好。',GREEN,16)
tx(s,.8,6.0,11.6,.35,'如果理论线和仿真点对不上，后面的编码增益都不能解释。',17,RED,True,PP_ALIGN.CENTER)
# 6 Monte Carlo visual
s=prs.slides.add_slide(blank);bg(s,6,'蒙特卡洛不是“跑几次看看”','每一个曲线点都有明确的统计量')
# big counters
for x,n,lab,c in [(1.0,'7','个 Eb/N0 点',CYAN),(4.0,'3','种信道',ORANGE),(7.0,'28','次独立试验',GREEN),(10.0,'336k','信息比特 / 点',RED)]:
 sh=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,Inches(x),Inches(1.55),Inches(2.2),Inches(1.6));sh.fill.solid();sh.fill.fore_color.rgb=WHITE;sh.line.color.rgb=c
 tx(s,x+.15,1.78,1.9,.55,n,30,c,True,PP_ALIGN.CENTER);tx(s,x+.15,2.45,1.9,.3,lab,12,GREY,False,PP_ALIGN.CENTER)
# equation and confidence visual
code(s,1.0,3.85,5.35,1.8,'p̂ = 错误 bit 数 / 总 bit 数\n\nCI95 = 1.96 × √[p̂(1−p̂) / N]')
card(s,7.0,3.85,5.15,1.8,'为什么要 CI95？','当某个点没有观察到错误时，不能把它理解成真实 BER 等于 0。置信区间告诉你“还可能有多大误差”。',BLUE,16)
# 7 coding visual
s=prs.slides.add_slide(blank);bg(s,7,'编码怎么把错误压下去？','卷积码增加冗余，Viterbi 从多条路径中选最可信的一条')
# encoder flow
card(s,.75,1.45,1.75,1.0,'输入 bit','bₖ',CYAN,18);arrow(s,2.6,1.95,3.15,1.95)
card(s,3.25,1.45,2.15,1.0,'卷积编码','g₁=111\ng₂=101',ORANGE,16);arrow(s,5.55,1.95,6.1,1.95)
card(s,6.2,1.45,1.75,1.0,'发送','2 bit',BLUE,18);arrow(s,8.05,1.95,8.6,1.95)
card(s,8.7,1.45,2.15,1.0,'Viterbi','4 states',GREEN,16);arrow(s,11.0,1.95,11.55,1.95)
card(s,11.65,1.45,1.0,1.0,'输出','b̂ₖ',RED,16)
# trellis mini
for row,(y,lab) in enumerate([(3.45,'00'),(4.15,'01'),(4.85,'10'),(5.55,'11')]):
 dot(s,2.0,y,.1,BLUE);tx(s,2.2,y-.1,.35,.2,lab,10,GREY)
 dot(s,5.3,y,.1,BLUE);arrow(s,2.15,y,5.15,y,RGBColor(150,170,190))
 tx(s,6.0,3.2,5.5,.35,'每个时刻保留到达每个状态的最短路径',16,NAVY,True)
 card(s,6.0,3.8,5.4,1.5,'Rician 8 dB 结果','未编码 BER ≈ 3.1×10⁻³\n编码后 336,000 个信息 bit 中没有观测到错误。',GREEN,18)
# 8 coding result
s=prs.slides.add_slide(blank);bg(s,8,'第二张证据图：编码增益','同一 Rician 信道，编码让 BER 曲线整体下降')
s.shapes.add_picture(str(FIG/'02_coding_gain.png'),Inches(.6),Inches(1.35),width=Inches(8.35),height=Inches(3.85))
card(s,9.35,1.4,3.15,1.25,'未编码','8 dB 仍然有约 3.1×10⁻³ 的 BER。',ORANGE,16)
card(s,9.35,2.95,3.15,1.25,'rate-1/2 编码','多发一倍冗余 bit，换来更低的信息 bit BER。',GREEN,16)
card(s,9.35,4.5,3.15,1.25,'图上怎么看','同一个 BER 水平，编码曲线所需 Eb/N0 更低。',BLUE,16)
# 9 app visual
s=prs.slides.add_slide(blank);bg(s,9,'CV 只负责“送什么”，通信负责“能否送到”','两种业务共享同一条 QPSK + Rician 链路')
s.shapes.add_picture(str(FIG/'04_application_reconstruction.png'),Inches(.6),Inches(1.35),width=Inches(8.5),height=Inches(3.15))
card(s,9.4,1.45,3.05,1.2,'固定源','每个像素统一 6 bit。',CYAN,17)
card(s,9.4,2.9,3.05,1.2,'CV 自适应源','平滑块 4 bit，纹理块 8 bit。',ORANGE,16)
card(s,9.4,4.35,3.05,1.2,'结果','全局 PSNR 约 30 dB，目标区域 PSNR 约 32.3 dB。',GREEN,15)
tx(s,.8,6.0,11.6,.35,'这部分是应用展示，BER 主线仍然来自前面的通信实验。',17,NAVY,True,PP_ALIGN.CENTER)
# 10 code visual
s=prs.slides.add_slide(blank);bg(s,10,'代码应该怎么读？','打开一个文件，按这条路径走')
# file path flow
steps=[('run_project_v3.m','入口'),('qpskChannel()','调制 / 信道 / 均衡'),('convEncode()','加冗余'),('viterbiDecode()','恢复信息 bit'),('transmitImage()','接入图像业务')]
for i,(name,desc) in enumerate(steps):
 y=1.35+i*.92; dot(s,1.05,y+.22,.14,[CYAN,BLUE,ORANGE,GREEN,RED][i]);tx(s,1.35,y,3.0,.3,name,16,NAVY,True,font='Menlo');tx(s,4.65,y,4.4,.3,desc,16,GREY)
 if i<4: arrow(s,1.05,y+.42,1.05,y+.78,GREY)
# right code highlight
code(s,8.0,1.35,4.5,2.0,'h = sqrt(K/(K+1))\n  + sqrt(1/(K+1))*g\n\ny = h.*s + n')
card(s,8.0,3.75,4.5,1.35,'先看这一段','它直接告诉你 Rician 的直射径、散射径和接收信号模型。',ORANGE,16)
card(s,8.0,5.3,4.5,.85,'数据出口','CSV 保存 BER、链路预算和业务层指标。',GREEN,15)
# 11 conclusion visual
s=prs.slides.add_slide(blank);bg(s,11,'最后只记住三张图','把整套实验讲成三个问题')
for x,img,title,body,c in [(0.7,'01_theory_validation.png','图 1：能不能信？','理论线和仿真点对上了吗？',CYAN),(4.45,'02_coding_gain.png','图 2：编码有用吗？','同一信道下 BER 下降了多少？',ORANGE),(8.2,'04_application_reconstruction.png','图 3：能传什么？','CV 业务在链路上如何取舍？',GREEN)]:
 s.shapes.add_picture(str(FIG/img),Inches(x),Inches(1.45),width=Inches(3.35),height=Inches(1.65));card(s,x,3.3,3.35,1.35,title,body,c,16)
card(s,1.6,5.35,10.0,.9,'完整故事','QPSK 是链路，Rician 是环境，卷积码是可靠性，CV 是业务。',BLUE,19)
# 12 timing
s=prs.slides.add_slide(blank);bg(s,12,'15 分钟怎么讲？','按这个节奏不会散')
for x,t,body,c in [(0.8,'0–3 min','链路总图 + QPSK + Eb/N0',CYAN),(3.95,'3–7 min','AWGN / Rayleigh / Rician + 理论线',ORANGE),(7.1,'7–11 min','卷积码 + Viterbi + coding gain',GREEN),(10.25,'11–15 min','CV 业务 + 结论 + Q&A',RED)]: card(s,x,1.6,2.35,2.0,t,body,c,16)
tx(s,.85,4.55,11.5,.7,'如果老师只问一个问题，就回答：\n“我先用理论 BER 验证了 QPSK 仿真器，再比较 Rician 和编码，最后把图像业务接入同一条链路。”',22,NAVY,True,PP_ALIGN.CENTER)
tx(s,.85,6.55,11.5,.25,'新版讲稿已与这 12 页逐页对应。',12,BLUE,True,PP_ALIGN.CENTER)
prs.save(OUT);print(OUT)
