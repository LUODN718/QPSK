from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pathlib import Path

ROOT=Path('/Users/lljk/Desktop/专业课/计算机视觉/QPSK'); FIG=ROOT/'figures'; OUT=ROOT/'ppt'/'QPSK_Communication_Story.pptx'
prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5); blank=prs.slide_layouts[6]
BG=RGBColor(247,249,252); NAVY=RGBColor(16,31,54); BLUE=RGBColor(26,103,196); CYAN=RGBColor(54,178,205); ORANGE=RGBColor(236,133,53); GREEN=RGBColor(55,157,104); RED=RGBColor(196,72,72); GREY=RGBColor(83,100,120); LIGHT=RGBColor(228,235,244); WHITE=RGBColor(255,255,255)

def bg(s,idx,title,sub=''):
 s.background.fill.solid();s.background.fill.fore_color.rgb=BG
 band=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,0,0,Inches(13.333),Inches(.14));band.fill.solid();band.fill.fore_color.rgb=BLUE;band.line.fill.background()
 t=s.shapes.add_textbox(Inches(.65),Inches(.42),Inches(12),Inches(.45));p=t.text_frame.paragraphs[0];p.text=title;p.font.name='Aptos Display';p.font.size=Pt(26);p.font.bold=True;p.font.color.rgb=NAVY
 if sub:
  q=s.shapes.add_textbox(Inches(.67),Inches(.90),Inches(12),Inches(.25));p=q.text_frame.paragraphs[0];p.text=sub.upper();p.font.size=Pt(8);p.font.bold=True;p.font.color.rgb=BLUE
 f=s.shapes.add_textbox(Inches(12.3),Inches(7.08),Inches(.55),Inches(.2));p=f.text_frame.paragraphs[0];p.text=f'{idx:02d}';p.font.size=Pt(9);p.font.color.rgb=GREY;p.alignment=PP_ALIGN.RIGHT

def tx(s,x,y,w,h,text,size=17,color=NAVY,bold=False,align=None,font='Aptos'):
 t=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h));tf=t.text_frame;tf.word_wrap=True;tf.margin_left=0;tf.margin_right=0;p=tf.paragraphs[0];p.text=text;p.font.name=font;p.font.size=Pt(size);p.font.color.rgb=color;p.font.bold=bold;p.alignment=align or PP_ALIGN.LEFT;return t

def card(s,x,y,w,h,title,body,color=BLUE,size=15):
 sh=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h));sh.fill.solid();sh.fill.fore_color.rgb=WHITE;sh.line.color.rgb=LIGHT
 strip=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(.07),Inches(h));strip.fill.solid();strip.fill.fore_color.rgb=color;strip.line.fill.background()
 t=s.shapes.add_textbox(Inches(x+.22),Inches(y+.15),Inches(w-.4),Inches(.3));p=t.text_frame.paragraphs[0];p.text=title;p.font.size=Pt(13);p.font.bold=True;p.font.color.rgb=color
 b=s.shapes.add_textbox(Inches(x+.22),Inches(y+.55),Inches(w-.42),Inches(h-.7));tf=b.text_frame;tf.word_wrap=True;p=tf.paragraphs[0];p.text=body;p.font.size=Pt(size);p.font.color.rgb=NAVY;p.line_spacing=1.05

def arrow(s,x1,y1,x2,y2,color=BLUE):
 ln=s.shapes.add_connector(1,Inches(x1),Inches(y1),Inches(x2),Inches(y2));ln.line.color.rgb=color;ln.line.width=Pt(2.5);ln.line.end_arrowhead=True

def code(s,x,y,w,h,text):
 sh=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h));sh.fill.solid();sh.fill.fore_color.rgb=NAVY;sh.line.color.rgb=RGBColor(46,71,101)
 t=s.shapes.add_textbox(Inches(x+.18),Inches(y+.12),Inches(w-.35),Inches(h-.2));tf=t.text_frame;tf.word_wrap=True;p=tf.paragraphs[0];p.text=text;p.font.name='Menlo';p.font.size=Pt(11);p.font.color.rgb=RGBColor(217,237,243);p.line_spacing=1.0

# 1
s=prs.slides.add_slide(blank);s.background.fill.solid();s.background.fill.fore_color.rgb=BG
bar=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,0,0,Inches(13.333),Inches(.16));bar.fill.solid();bar.fill.fore_color.rgb=BLUE;bar.line.fill.background()
tx(s,.8,1.05,11.8,.55,'Can a QPSK link reliably carry image traffic over fading channels?',29,NAVY,True)
tx(s,.82,1.85,11.2,.5,'Communication Monte Carlo experiment · theory validation · Rician fading · coding gain',20,BLUE)
# visual chain
for x,label,body,c in [(1.0,'BITS','source bits',CYAN),(4.1,'QPSK','2 bits / symbol',BLUE),(7.2,'CHANNEL','h·s + n',ORANGE),(10.3,'RX','BER / image',GREEN)]:
 card(s,x,3.25,2.0,1.45,label,body,c,16)
arrow(s,3.05,3.97,4.0,3.97);arrow(s,6.15,3.97,7.1,3.97);arrow(s,9.25,3.97,10.2,3.97)
card(s,1.0,5.45,3.4,1.0,'MAIN QUESTION','First prove the link simulator is trustworthy',CYAN,15);card(s,4.95,5.45,3.4,1.0,'COMMUNICATION','Channel effects + coding gain',ORANGE,15);card(s,8.9,5.45,3.4,1.0,'APPLICATION','CV only allocates source bits',GREEN,15)
tx(s,.85,6.82,11,.2,'Open the presentation with this sentence',10,GREY)
# 2
s=prs.slides.add_slide(blank);bg(s,2,'Explain the experiment in 30 seconds','Make the verification target explicit')
card(s,.8,1.45,3.7,3.7,'INPUT','Random information BITS\n\nor an image. CV only decides which 8×8 blocks use 4 or 8 bits.',CYAN,18)
card(s,4.8,1.45,3.7,3.7,'LINK','QPSK modulation\n\nAWGN, Rayleigh and Rician channels. The RX estimates h, equalizes, hard-demaps and runs Viterbi when coded.',ORANGE,18)
card(s,8.8,1.45,3.7,3.7,'EVIDENCE','BER curves with theory\n\n95% confidence intervals, coding gain, constellation, spectrum and image-layer PSNR.',GREEN,18)
tx(s,.85,5.75,11.5,.5,'One sentence: validate the link with theory first, then show coding and CV payload trade-offs.',18,NAVY,True,PP_ALIGN.CENTER)
# 3
s=prs.slides.add_slide(blank);bg(s,3,'What is inside the link?','Every box maps to a code block')
for x,title,body,c in [(0.7,'TX','bits → parity\n→ QPSK mapper',CYAN),(3.25,'CHANNEL','h·s + n\nAWGN / Rayleigh / Rician',ORANGE),(5.8,'RX','pilot estimate\n→ equalizer → hard decision',BLUE),(8.35,'FEC','Viterbi\n→ information bits',GREEN),(10.9,'METRICS','BER · CI95\nPSNR · rate',RED)]: card(s,x,2.15,1.8,2.1,title,body,c,15)
for x in [2.55,5.1,7.65,10.2]: arrow(s,x,3.2,x+.55,3.2)
card(s,2.2,5.1,8.9,.9,'APPLICATION ENTRY','Fixed 6-bit image source  ↔  CV adaptive 4/8-bit source',BLUE,16)
# 4
s=prs.slides.add_slide(blank);bg(s,4,'Why use Eb/N0 on the x-axis?','Put modulation and coding on the same scale')
code(s,.8,1.45,5.7,3.8,'QPSK: 2 bits / symbol\n\nE_s = 1\nN0 = R / (2 · 10^(Eb/N0 / 10))\n\nR = 1      uncoded\nR = 1/2    convolutional code')
card(s,7.0,1.45,5.2,1.25,'PROBLEM','Using Es/N0 mixes the 2 bits/symbol factor into the comparison.',ORANGE,16)
card(s,7.0,3.0,5.2,1.25,'FIX','Use information-bit Eb/N0. AWGN BPSK and Gray-QPSK then share the same per-bit theory curve.',CYAN,16)
card(s,7.0,4.55,5.2,1.25,'DEFENSE LINE','Normalize information-bit energy first, then compare channel and coding effects.',GREEN,15)
# 5
s=prs.slides.add_slide(blank);bg(s,5,'What changes in a Rician channel?','K is the LOS-to-scatter power ratio')
code(s,.8,1.45,5.8,2.8,'K = 10^(K_dB / 10)\nh = √(K/(K+1))\n    + √(1/(K+1)) · g\ng ~ CN(0,1)')
card(s,7.05,1.45,5.1,1.1,'K = 0','No LOS term. This becomes Rayleigh.',CYAN,17)
card(s,7.05,2.8,5.1,1.1,'K = 10 dB','LOS power is ten times diffuse power.',ORANGE,17)
card(s,7.05,4.15,5.1,1.1,'K → ∞','Fading vanishes as the channel approaches AWGN.',GREEN,17)
tx(s,.85,5.9,11.6,.5,'The previous zero-mean complex Gaussian model was Rayleigh. The new code fixes this.',16,RED,True,PP_ALIGN.CENTER)
# 6
s=prs.slides.add_slide(blank);bg(s,6,'How is Monte Carlo made credible?','Sample count, fixed seed and confidence intervals')
card(s,.8,1.45,3.55,3.9,'SWEEP','Eb/N0 = 0:2:16 dB\n\nAWGN / Rayleigh / Rician\n\nuncoded / coded',BLUE,18)
card(s,4.85,1.45,3.55,3.9,'SAMPLES','28 independent trials\n\n12,000 information bits / trial\n\n336,000 information bits / point',ORANGE,18)
card(s,8.9,1.45,3.55,3.9,'UNCERTAINTY','p̂ = errors / bits\n\nCI95 = 1.96 × √[p̂(1−p̂)/N]\n\nfixed rng seed',GREEN,18)
tx(s,.85,5.9,11.5,.45,'At high SNR, report the confidence interval when zero errors are observed.',16,NAVY,True,PP_ALIGN.CENTER)
# 7
s=prs.slides.add_slide(blank);bg(s,7,'Core result 1: theory and simulation agree','This validates the simulator before discussing coding gain')
s.shapes.add_picture(str(FIG/'01_theory_validation.png'),Inches(.6),Inches(1.38),width=Inches(8.25),height=Inches(3.7))
card(s,9.15,1.45,3.45,1.25,'AWGN','Markers follow Q(sqrt(2γ)).',CYAN,16)
card(s,9.15,3.0,3.45,1.25,'Rayleigh','Markers follow the Rayleigh theory expression.',ORANGE,16)
card(s,9.15,4.55,3.45,1.25,'Rician','K=10 dB adds LOS power, so BER is lower than Rayleigh.',GREEN,16)
# 8
s=prs.slides.add_slide(blank);bg(s,8,'Core result 2: how much gain does coding buy?','rate-1/2 convolutional code + Viterbi')
s.shapes.add_picture(str(FIG/'02_coding_gain.png'),Inches(.65),Inches(1.45),width=Inches(7.65),height=Inches(3.85))
code(s,8.7,1.45,3.7,2.25,'g1 = 111₂\ng2 = 101₂\n\n4 states · hard Viterbi')
card(s,8.7,4.1,3.7,1.4,'RESULT','At Rician 8 dB, uncoded BER≈3.1×10⁻³. The coded run has zero observed errors in 336,000 information bits.',GREEN,15)
# 9
s=prs.slides.add_slide(blank);bg(s,9,'Waveform evidence: the link really carries QPSK','Constellation and spectrum make the signaling waveform visible')
s.shapes.add_picture(str(FIG/'03_waveform.png'),Inches(.65),Inches(1.45),width=Inches(8.1),height=Inches(3.25))
card(s,9.05,1.45,3.45,1.3,'CONSTELLATION','Rician fading spreads the four ideal points before equalization.',CYAN,16)
card(s,9.05,3.05,3.45,1.3,'SPECTRUM','The FFT shows signal energy over normalized frequency.',ORANGE,16)
card(s,9.05,4.65,3.45,1.3,'RECEIVER','A small h-estimation error models imperfect pilots.',GREEN,16)
# 10
s=prs.slides.add_slide(blank);bg(s,10,'Where does CV fit?','It is a payload policy inside the trusted link')
s.shapes.add_picture(str(FIG/'04_application_reconstruction.png'),Inches(.65),Inches(1.45),width=Inches(8.25),height=Inches(3.05))
card(s,9.15,1.45,3.35,1.2,'FIXED PAYLOAD','6 bits per pixel.',CYAN,17)
card(s,9.15,2.9,3.35,1.2,'ADAPTIVE PAYLOAD','Gradient complexity selects 4 or 8 bits per 8×8 block.',ORANGE,16)
card(s,9.15,4.35,3.35,1.2,'SAME LINK','Both payloads use the same QPSK, Rician channel and Eb/N0.',GREEN,16)
tx(s,.85,5.95,11.5,.4,'Fixed PSNR≈30.7 dB. Adaptive PSNR≈30.0 dB, with target-region PSNR≈32.3 dB.',16,NAVY,True,PP_ALIGN.CENTER)
# 11
s=prs.slides.add_slide(blank);bg(s,11,'How do you read the code?','Trace from the entry point to BER')
code(s,.75,1.35,5.8,4.6,"run_project_v3.m\n\n1  link budget\n2  BER Monte Carlo loop\n3  qpskChannel()\n4  convEncode()\n5  viterbiDecode()\n6  waveform figures\n7  transmitImage()\n8  write CSV + MAT")
card(s,7.0,1.35,5.4,1.35,'START HERE','qpskChannel() maps QPSK, adds noise and h, estimates h_hat, equalizes and hard-demaps.',CYAN,16)
card(s,7.0,3.0,5.4,1.35,'NEXT','viterbiDecode() is a four-state dynamic program with path metrics and traceback.',ORANGE,16)
card(s,7.0,4.65,5.4,1.35,'OUTPUT FILES','ber_validation.csv feeds the theory plot. link_budget.csv stores the link budget. application_layer.csv stores the CV payload results.',GREEN,15)
# 12
s=prs.slides.add_slide(blank);bg(s,12,'Remember three sentences','Close the project with one story')
card(s,.9,1.55,3.55,2.7,'1','I validate the QPSK simulator with AWGN and Rayleigh theory before discussing Rician.',CYAN,19)
card(s,4.85,1.55,3.55,2.7,'2','I measure coding gain with a rate-1/2 convolutional code and Viterbi.',ORANGE,19)
card(s,8.8,1.55,3.55,2.7,'3','I connect a CV-adaptive image source to the same trusted link.',GREEN,19)
tx(s,.9,5.15,11.4,.8,'QPSK is the main character. Rician fading and coding provide depth. CV is the application layer.',25,NAVY,True,PP_ALIGN.CENTER)
tx(s,.9,6.65,11.4,.25,'Q&A',13,BLUE,True,PP_ALIGN.CENTER)
prs.save(OUT); print(OUT)
