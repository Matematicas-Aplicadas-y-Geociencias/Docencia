
Um2=interp1(tm,Um,to);
plot(Uo)
hold on
plot(Um2,'r')

%Calculo del histograma con las particiones en x ubicadas en
%"edges"
edges=-0.4:0.05:0.4;
V=R;
[N,x] = histcounts(V,edges);
%Aqui se conviernte número de observaciones en porcentajes y porcentajes
%cumulativos
n=length(V);
Npercent=(N/n)*100;
Ncum=cumsum(Npercent);

%Esta parte grafica el histograma de velocidades promediadas en la vertical
%y sobrepone los porcentajes cumulativos
yyaxis left
bar(x(2:end),Npercent,'g')
ylabel('Porcentajes')
yyaxis right
plot(x(2:end),Ncum)
ylabel('Porcentajes')
xlabel('velocidad (m/s)')
alpha(0.5)%agregar transparencia a figura

%3er y 4o momento de la distribución estadística

Mean1=mean(V);
Stdev=std(V);
Sk1=skewness(V);
Kur1=kurtosis(V);
Mean2=mean(Vo);
Sk2=skewness(Vo);
Kur2=kurtosis(Vo);

%prueba de Skewness...teorica
a1=0.5; T1=10;   
a2=0.6; T2=5;   
fm=2;%Hz frecuencia de muestreo en ciclos por tiempo
endt=1024;%*10;
t=0:1/fm:endt;
ETA1=a1.*cos((2*pi/T1).*t);
ETA2=a2.*cos((2*pi/T2).*t);
ETA=ETA1+ETA2;

subplot(2,1,1)
plot(t,ETA1)
hold on
plot(t,ETA2)
subplot(2,1,2)
plot(t,ETA)
Mean1=mean(ETA);Stdev=std(ETA);Sk1=skewness(ETA);