%Calculo del espectro Welch 
%Usar datos de coeficientes Fourier
eta=detrend(NivelMar);
y1=detrend(WN);
y2=detrend(WE);
x1=detrend(VN);
x2=detrend(VE);
T1=detrend(TempOcean);
t=tOcean;

s=2^14; %debe ser un multiplo de 2^n
eta(end+1:s)=0;
x1(end+1:s)=0;
x2(end+1:s)=0;
y1(end+1:s)=0;
y2(end+1:s)=0;
T1(end+1:s)=0;

N=length(y1);

m=4096;%32768;%1024%;
n=m/2;
fm=48;%frecuencia de muestreo
restemp=m/fm;  %resolucion temporal 
p=N/m;
df=3.82*p-3.24;%Calculo de los grados de libertad
%ventana 
window=hanning(m);

     [Seta,F]=pwelch(eta,window,n,m,fm);
     [Sxx1,F]=pwelch(x1,window,n,m,fm);
     [Sxx2,F]=pwelch(x2,window,n,m,fm);
     [Syy1,F]=pwelch(y1,window,n,m,fm);
     [Syy2,F]=pwelch(y2,window,n,m,fm);
     [ST1,F]=pwelch(T1,window,n,m,fm);


figure
subplot(2,2,1)
loglog(F,Seta)
title('Nivel del mar')
subplot(2,2,2)
loglog(F,Sxx1)
hold on
loglog(F,Sxx2)
title('Corrientes')
legend('VN','VE')
xlabel('frecuencia cpd')
ylabel('Energia espectral')
subplot(2,2,3)
loglog(F,Syy1,'k')
hold on
loglog(F,Syy2)
title('viento')
legend('WN','WE')
subplot(2,2,4)
loglog(F,ST1)
xlabel('frecuencia cpd')
title('Temperatura')


%df=4.4...li=0.38, ls=6.6
%df=12.04...li=0.5, ls=2.6
%df=27.32...li=0.63, ls=1.8
%df=57.88...li=0.7, ls=1.5
a=6;%hhh
lii=li*ST1(a);
lss=ls*ST1(a);
lc=[lii ST1(a) lss];
xc=[F(a) F(a) F(a)];
hold on
plot(xc, lc,'b+-')


%x = chi2inv(0.95,df)
%chi2inv
% sum(Sxx)./((m/2)+1)
% var(y)

clear lii lss a lc li ls p restemp xc F S NOI Nq Ny Sxx Txx ans df dof fs hflim i m n s s1 sf window  