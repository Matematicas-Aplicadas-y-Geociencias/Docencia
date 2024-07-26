%Antes de usar generar señal sinusoidal con o sin ruido
N=length(X);
n=1:N;
Ny=fm/2;%Frecuencia de Nyquist (máxima frecuencia a resolver)

tm=1/fm;%periodo de muestreo (tiempo)
freq1=(1:(N/2-1))/(N*tm);%dividido entre el numero de segundos
f=[freq1, Ny,-Ny, -1.*fliplr(freq1)]';

for p=1:N
    arg=cos(((2*pi*p)./N).*n);
    A(p)=2/N.*sum(X.*arg);
    B(p)=2/N.*sum(X.*sin(((2*pi*p)./N).*n));
    
     subplot(1,2,1)
     plot(f(p),A(p),'o')
     title (p)
     axis([-Ny Ny -0.15 0.15])
     hold on  
     subplot(1,2,2)                       
     plot(t,arg,'b')
     hold on
     plot(t,X)
     title (f(p))
     axis([0 t(end) -2 2])
     hold off
     clear arg
     
     if p<3
        pause
     else
         pause(0.00001)
     end
     
end

C=sqrt(A.^2+B.^2);
%vector de frecuencias
TH=atan(B./A);

figure
plot(f,C,'r')
xlabel('frequency (cpd)')

D=fft(X);
hold on
plot(f,abs(D)/1024,'k')

for p=1:N
    arg=cos(((2*pi*p)./N).*n-TH(p));
    y(p,:)=C(p).*arg;
    
     subplot(2,1,1)
     plot(t,arg,'b')
     title (p)
     subplot(2,1,2)
     plot(t,y(p,:))
     axis([0 t(end) -0.5 0.5])
     clear arg
     
%      if p<150
%         pause
%      else
%          pause(0.00001)
%      end
     
end

y2=sum(y);

plot(t,y2)
clear A B C N Ny f freq1 fs n p ts