%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
eta=detrend(Z);
%x1=detrend(VN);
x2=detrend(VE);
% y1=detrend(WN);
y2=detrend(WE);
T1=detrend(TempOcean);
t=tOcean;
fm=48;
% s=2^14; %preferencia un multiplo de 2^n
% y(end+1:s)=0;
% x(end+1:s)=0;
N=length(tOcean);


[wtnm,f,coi] = cwt(eta,'amor',fm);%señal y la frecuencia de muestreo
magNM=sqrt(real(wtnm).^2+imag(wtnm).^2);
[wtve,f,coi] = cwt(x2,'amor',fm);%señal y la frecuencia de muestreo
magVE=sqrt(real(wtve).^2+imag(wtve).^2);
[wtwe,f,coi] = cwt(y2,'amor',fm);%señal y la frecuencia de muestreo
magWE=sqrt(real(wtwe).^2+imag(wtwe).^2);
[wttem,f,coi] = cwt(T1,'amor',fm);%señal y la frecuencia de muestreo
magTMP=sqrt(real(wttem).^2+imag(wttem).^2);

figure
subplot(4,1,1)
pcolor(t,f,magNM(:,1:N)); shading flat; colorbar %eje y en log
ax=gca;
ax.YScale = 'log';
hold on
ylabel('cpd')
plot(t,coi(1:N),'w')
title('NivMar')
datetick

subplot(4,1,2)
pcolor(t,f,magWE(:,1:N)); shading flat; colorbar %eje y en log
ax=gca;
ax.YScale = 'log';
hold on
plot(t,coi(1:N),'w')
title('WE')
datetick

subplot(4,1,3)
pcolor(t,f,magVE(:,1:N)); shading flat; colorbar %eje y en log
ax=gca;
ax.YScale = 'log';
hold on
plot(t,coi(1:N),'w')
title('VE')
datetick

subplot(4,1,4)
pcolor(t,f,magTMP(:,1:N)); shading flat; colorbar %eje y en log
ax=gca;
ax.YScale = 'log';
hold on
plot(t,coi(1:N),'w')
title('TEMP')
datetick


WavSpec=sum(magNM');
figure
loglog(f,WavSpec)