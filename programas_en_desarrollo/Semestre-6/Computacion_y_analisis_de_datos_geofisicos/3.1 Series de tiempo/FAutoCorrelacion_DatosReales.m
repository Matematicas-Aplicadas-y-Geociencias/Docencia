%Programar la Función de autocovarianza y de autocorrelaciòn y usar con
%datos reales
y=WE;
fm=48;%cpd
N=length(y);
ymean=mean(y);
k=0:fm*200;%frecuencia de muestreo*desfase
%Calculo la funcion de autocovarianza             
for i=1:length(k) 
    for j=1:N-k(i)
        A(j)=(y(j)-ymean);
        B(j)=(y(j+k(i))-ymean);
    end
      Cyy(i)=(1/(N-k(i))).*sum(A.*B);
      clear A B
end
rho=Cyy/var(y); %Covarianza normalizada..
%a veces referida como función de autocorrelación...
per=k/fm; %periodicidades en dias
plot(per,rho,'.-r')

t=tOcean-tOcean(1);
for i=1:length(k) 
plot(t,y)
axis([0 50 -1 1])
hold on
plot(t+k(i),y,'r')
hold off
pause(1)
end


%Correlaciòn cruzada
% y=VN;%corrientes N-S
% fm=48;%cpd
% x=WN;%Viento N-S
% xmean=mean(x);
% k=0:fm*100;%fr
% 
% for i=1:length(k) 
%     for j=1:N-k(i)
%         A(j)=(y(j)-ymean);
%         B(j)=(x(j+k(i))-xmean);
%     end
%       Cxy(i)=(1/(N-k(i))).*sum(A.*B);
%       clear A B
% end
% rhoxy=Cxy/(std(y)*std(x)); %Covarianza normalizada..
% %a veces referida como función de autocorrelación...
% per=k/fm; %periodicidades
% plot(per,rhoxy,'.-r')
% 
% plot(x)






