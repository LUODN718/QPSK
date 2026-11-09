%% Communication-first Monte Carlo project
% Main story: QPSK link reliability, channel model validation, coding gain.
% CV is retained only as an application-layer source-adaptation module.
clear; close all; clc; rng(20261109,'twister');
base=fileparts(mfilename('fullpath')); root=fullfile(base,'..'); figDir=fullfile(root,'figures'); dataDir=fullfile(root,'data');
if ~exist(figDir,'dir'),mkdir(figDir);end; if ~exist(dataDir,'dir'),mkdir(dataDir);end

%% 1. Link budget used to motivate the Eb/N0 range
fGHz=2.2; dkm=600; Pt_dBm=30; Gt_dBi=8; Gr_dBi=8; L_dB=2; BW_Hz=1e6; Tn_K=500;
fspl=92.45+20*log10(fGHz)+20*log10(dkm); Pr_dBm=Pt_dBm+Gt_dBi+Gr_dBi-fspl-L_dB; N_dBm=-174+10*log10(BW_Hz)+10*log10(Tn_K/290); linkSNR_dB=Pr_dBm-N_dBm;
linkBudget=table(Pt_dBm,Gt_dBi,Gr_dBi,fspl,L_dB,Pr_dBm,N_dBm,linkSNR_dB,'VariableNames',{'Pt_dBm','Gt_dBi','Gr_dBi','FSPL_dB','OtherLoss_dB','Pr_dBm','Noise_dBm','SNR_dB'}); writetable(linkBudget,fullfile(dataDir,'link_budget.csv'));

%% 2. BER validation: same QPSK, Eb/N0 normalized
EbN0dB=0:2:16; nTrials=28; nInfo=12000; KdB=10;
channels={'AWGN','Rayleigh','Rician'}; coded=[false true];
rows={};
for ci=1:numel(channels)
    for co=1:numel(coded)
        for si=1:numel(EbN0dB)
            err=0; total=0; txTotal=0;
            for tr=1:nTrials
                bits=randi([0 1],nInfo,1); R=1; tx=bits;
                if coded(co), tx=convEncode(bits); R=1/2; end
                [hard,~,nTx]=qpskChannel(tx,EbN0dB(si),channels{ci},KdB,R); txTotal=txTotal+nTx;
                if coded(co), dec=viterbiDecode(hard,nInfo); err=err+sum(dec~=bits); total=total+nInfo; else, err=err+sum(hard~=bits); total=total+numel(bits); end
            end
            pHat=err/total; ci95=1.96*sqrt(max(pHat*(1-pHat)/total,1e-15)); rows=[rows;{channels{ci},coded(co),EbN0dB(si),pHat,ci95,total,txTotal}]; %#ok<AGROW>
        end
    end
end
BER=cell2table(rows,'VariableNames',{'Channel','Coded','EbN0_dB','BER','CI95','InfoBits','TxBits'}); writetable(BER,fullfile(dataDir,'ber_validation.csv'));

% Figure A: theory vs Monte Carlo for uncoded QPSK
f=figure('Color','w','Position',[80 80 1150 500]); hold on; grid on;
awgnTheory=0.5*erfc(sqrt(10.^(EbN0dB/10))); rayTheory=0.5*(1-sqrt(10.^(EbN0dB/10)./(1+10.^(EbN0dB/10))));
semilogy(EbN0dB,awgnTheory,'k--','LineWidth',1.7); semilogy(EbN0dB,rayTheory,'k:','LineWidth',1.7);
styles={'o-','s-','d-'}; colors=[0.10 0.45 0.85;0.85 0.30 0.15;0.15 0.60 0.35];
for ci=1:3, mask=strcmp(BER.Channel,channels{ci}) & ~BER.Coded; errorbar(BER.EbN0_dB(mask),BER.BER(mask),BER.CI95(mask),styles{ci},'Color',colors(ci,:),'LineWidth',1.4,'MarkerSize',5); end
xlabel('E_b/N_0 (dB)'); ylabel('BER'); ylim([1e-4 0.5]); legend('AWGN theory','Rayleigh theory','AWGN sim','Rayleigh sim','Rician K=10 dB sim','Location','southwest'); title('Uncoded QPSK: theory and Monte Carlo validation'); exportgraphics(f,fullfile(figDir,'01_theory_validation.png'),'Resolution',180);

% Figure B: coding gain under Rician
f=figure('Color','w','Position',[80 80 950 500]); hold on; grid on; mask=strcmp(BER.Channel,'Rician');
for co=1:2, mm=mask & (BER.Coded==coded(co)); errorbar(BER.EbN0_dB(mm),BER.BER(mm),BER.CI95(mm),styles{co},'LineWidth',1.6,'MarkerSize',6); end
xlabel('E_b/N_0 (dB)'); ylabel('BER'); ylim([1e-4 .5]); legend('Uncoded QPSK','Rate-1/2 convolutional + Viterbi','Location','southwest'); title('Rician K=10 dB: coding gain'); exportgraphics(f,fullfile(figDir,'02_coding_gain.png'),'Resolution',180);

%% 3. Waveform evidence
bits=randi([0 1],4000,1); [hard,rxSym,~]=qpskChannel(bits,8,'Rician',KdB,1); %#ok<ASGLU>
f=figure('Color','w','Position',[80 80 1100 450]); subplot(1,2,1); plot(real(rxSym(1:1200)),imag(rxSym(1:1200)),'.','MarkerSize',4); axis equal; grid on; xlabel('I');ylabel('Q');title('Received QPSK constellation, 8 dB'); subplot(1,2,2); s=rxSym(1:min(2048,numel(rxSym))); P=abs(fftshift(fft(s))).^2; freq=linspace(-.5,.5,numel(P)); plot(freq,10*log10(P/max(P)+eps),'LineWidth',1.1); grid on; xlabel('Normalized frequency');ylabel('PSD (dB)');title('Received signal spectrum'); exportgraphics(f,fullfile(figDir,'03_waveform.png'),'Resolution',180);

%% 4. Application layer: adaptive image source, same QPSK link
N=96; B=8; [img,maskObj]=makeScene(N,20261109); [feat,~]=blockFeatures(img,B); score=feat(:,5); th=median(score); adaptiveBits=4*ones(size(score)); adaptiveBits(score>th)=8; fixedBits=6*ones(size(score));
EbApp=8; [recFixed,appFixed]=transmitImage(img,fixedBits,EbApp,'Rician',KdB,false,B); [recAdapt,appAdapt]=transmitImage(img,adaptiveBits,EbApp,'Rician',KdB,true,B);
app=table({'Fixed 6-bit';'CV adaptive 4/8-bit'},[appFixed.bitsPerPixel;appAdapt.bitsPerPixel],[appFixed.ber;appAdapt.ber],[appFixed.psnr;appAdapt.psnr],[appFixed.targetPsnr;appAdapt.targetPsnr],[appFixed.retries;appAdapt.retries],'VariableNames',{'Method','Tx_bits_per_pixel','BER','PSNR_dB','Target_PSNR_dB','Mean_retries'}); writetable(app,fullfile(dataDir,'application_layer.csv'));
f=figure('Color','w','Position',[80 80 1100 350]); subplot(1,3,1);imagesc(img);axis image off;title('Source image');subplot(1,3,2);imagesc(recFixed);axis image off;title(sprintf('Fixed 6 bit, PSNR %.1f dB',appFixed.psnr));subplot(1,3,3);imagesc(recAdapt);axis image off;title(sprintf('Adaptive 4/8 bit, PSNR %.1f dB',appAdapt.psnr));colormap turbo; exportgraphics(f,fullfile(figDir,'04_application_reconstruction.png'),'Resolution',180);

save(fullfile(dataDir,'project_v3.mat'),'BER','app','linkBudget','img','maskObj','adaptiveBits','fixedBits'); disp(linkBudget); disp(BER(strcmp(BER.Channel,'Rician') & BER.EbN0_dB==8,:)); disp(app);

function h=ricianH(KdB,n)
    K=10^(KdB/10); h=sqrt(K/(K+1))+sqrt(1/(K+1))*(randn(n,1)+1i*randn(n,1))/sqrt(2);
end
function [hard,rxSym,nTx]=qpskChannel(bits,EbN0dB,channel,KdB,R)
    if mod(numel(bits),2),bits(end+1)=0;end; pair=reshape(bits,2,[])'; txSym=((2*pair(:,1)-1)+1i*(2*pair(:,2)-1))/sqrt(2); k=2; N0=R/(k*10^(EbN0dB/10)); n=sqrt(N0/2)*(randn(size(txSym))+1i*randn(size(txSym)));
    if strcmp(channel,'AWGN'), h=ones(size(txSym)); elseif strcmp(channel,'Rayleigh'), h=(randn(size(txSym))+1i*randn(size(txSym)))/sqrt(2); else, h=ricianH(KdB,numel(txSym)); end
    y=h.*txSym+n; hhat=h+0.08*(randn(size(h))+1i*randn(size(h)))/sqrt(2); z=conj(hhat).*y./(abs(hhat).^2+eps); pairOut=[real(z)>0 imag(z)>0]; hard=double(pairOut.'); hard=hard(:); hard=hard(1:numel(bits)); rxSym=z; nTx=numel(bits);
end
function out=convEncode(bits)
    s1=0;s2=0;out=zeros(2*numel(bits),1); k=1; for b=bits(:)'; out(k)=mod(b+s1+s2,2);out(k+1)=mod(b+s2,2);s2=s1;s1=b;k=k+2;end
end
function dec=viterbiDecode(rx,nInfo)
    g=[0 0;1 1;1 0;0 1]; infv=1e9; metric=infv*ones(4,1);metric(1)=0; prev=zeros(4,nInfo); inbit=zeros(4,nInfo);
    for t=1:nInfo
        r=rx(2*t-1:2*t); new=infv*ones(4,1);
        for st=0:3
            s1=floor(st/2); s2=mod(st,2);
            for b=0:1
                ns=2*b+s1; out=[mod(b+s1+s2,2),mod(b+s2,2)]; cost=metric(st+1)+sum(out~=r(:)');
                if cost<new(ns+1),new(ns+1)=cost;prev(ns+1,t)=st;inbit(ns+1,t)=b;end
            end
        end
        metric=new;
    end
    [~,st]=min(metric);dec=zeros(nInfo,1);for t=nInfo:-1:1,dec(t)=inbit(st,t);st=prev(st,t)+1;end
end
function [rec,stats]=transmitImage(img,bitsPerBlock,EbN0dB,channel,KdB,adaptive,B)
    N=size(img,1); nb=N/B; rec=zeros(N); totalErr=0;totalBits=0;totalTx=0;totalRetries=0; idx=1; [feat,~]=blockFeatures(img,B); %#ok<ASGLU>
    for bi=1:numel(bitsPerBlock), r=floor((bi-1)/nb);c=mod(bi-1,nb); nbp=bitsPerBlock(bi); blk=img(r*B+1:(r+1)*B,c*B+1:(c+1)*B); qv=round(blk*(2^nbp-1)); data=int2bits(uint16(qv(:)),nbp); packet=[reshape(data.',[],1);mod(sum(data(:)),2)]; [rx,e,tx,re]=sendRetry(packet,EbN0dB,nbp,channel,KdB); vals=bits2int(reshape(rx(1:numel(data)),nbp,[])');rec(r*B+1:(r+1)*B,c*B+1:(c+1)*B)=reshape(double(vals)/(2^nbp-1),B,B);totalErr=totalErr+e;totalBits=totalBits+numel(data);totalTx=totalTx+tx;totalRetries=totalRetries+re;idx=idx+1; %#ok<NASGU>
    end
    [~,obj]=makeScene(N,20261109); stats.bitsPerPixel=totalTx/(N*N);stats.ber=totalErr/totalBits;stats.psnr=10*log10(1/mean((img(:)-rec(:)).^2));stats.targetPsnr=10*log10(1/mean((img(obj>0.5)-rec(obj>0.5)).^2));stats.retries=totalRetries/(nb*nb);
end
function [rx,e,tx,re]=sendRetry(packet,EbN0dB,nb,channel,KdB)
    re=0;tx=0;rx=zeros(size(packet));for a=1:3,[r,e0,nt]=qpskChannel(packet,EbN0dB,channel,KdB,1);rx=r(1:numel(packet));e=sum(rx(1:end-1)~=packet(1:end-1));tx=tx+nt;if mod(sum(rx),2)==0||a==3,break;end;re=re+1;end
end
function [im,mask]=makeScene(N,seed)
    rng(seed,'twister');[x,y]=meshgrid(linspace(-1,1,N));im=.25+.15*sin(5*x).*cos(4*y)+.05*randn(N);mask=zeros(N);for k=1:5,cx=-.75+1.5*rand;cy=-.75+1.5*rand;s=.06+.12*rand;g=exp(-((x-cx).^2+(y-cy).^2)/(2*s^2));im=im+(.15+.3*rand)*g;mask=mask|(g>.35);end;r=20;c=25;im(r:r+12,c:c+18)=im(r:r+12,c:c+18)+.2;mask(r:r+12,c:c+18)=1;im=(im-min(im(:)))/(max(im(:))-min(im(:))+eps);mask=double(mask>0);
end
function [F,occ]=blockFeatures(im,B)
    N=size(im,1);nb=N/B;F=zeros(nb*nb,6);occ=zeros(nb*nb,1);k=1;for r=1:nb,for c=1:nb,z=im((r-1)*B+1:r*B,(c-1)*B+1:c*B);gx=diff(z,1,2);gy=diff(z,1,1);lap=diff(z,2,2);F(k,:)=[mean(z(:)),std(z(:)),mean(abs(gx(:))),mean(abs(gy(:))),mean(abs(gx(:)))+mean(abs(gy(:))),mean(abs(lap(:)))];occ(k)=mean(z(:));k=k+1;end,end
end
function out=int2bits(v,n),v=double(v(:));out=zeros(numel(v),n);for k=1:n,out(:,k)=bitget(v,n-k+1);end,end
function v=bits2int(B),v=double(B)*(2.^(size(B,2)-1:-1:0))';end
