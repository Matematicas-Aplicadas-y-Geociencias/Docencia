%Calculo del espectro Welch para una señal ficticia

m=1024;
n=m/2;
restemp=m/fm  %resolucion temporal 
p=N/m;
df=3.82*p-3.24;%Calculo de los grados de libertad
%ventana 
window=hanning(m);

     [Sxx,F]=pwelch(X,window,n,m,fm);
     
figure
loglog(F,Sxx)
title('nivel del mar')

%df=4.4...li=0.38, ls=6.6
%df=12.04...li=0.5, ls=2.6
%df=27.32...li=0.63, ls=1.8
%df=57.88...li=0.7, ls=1.5
a=6;%hhh
lii=li*Sxx(a);
lss=ls*Sxx(a);
lc=[lii Sxx(a) lss];
xc=[F(a) F(a) F(a)];
hold on
plot(xc, lc,'r+-')


%x = chi2inv(0.95,df)
%chi2inv
sum(Sxx)./((m/2)+1)
var(X)

clear lii lss a lc li ls p restemp xc F S NOI Nq Ny Sxx Txx ans df dof fs hflim i m n s s1 sf window  