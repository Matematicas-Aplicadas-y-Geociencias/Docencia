subplot(4,1,1)
plot(tOcean,NivelMar)
axis([tOcean(1) tOcean(end) -1 1])
ylabel('Nivel del mar (m)')
datetick
grid

subplot(4,1,2)
plot(tOcean,VE)
hold on
plot(tOcean,VN,'r')
axis([tOcean(1) tOcean(end) -0.5 0.5])
legend('Este','Norte')
ylabel('Corrientes (m/s)')
datetick
grid

subplot(4,1,3)
plot(tOcean,WE)
hold on
plot(tOcean,WN,'r')
axis([tOcean(1) tOcean(end) -20 20])
legend('Este','Norte')
ylabel('Viento (m/s)')
datetick
grid

subplot(4,1,4)
plot(tOcean,TempOcean)
axis([tOcean(1) tOcean(end) 19 31])
ylabel('Temperatura (^oC)')
datetick
grid
