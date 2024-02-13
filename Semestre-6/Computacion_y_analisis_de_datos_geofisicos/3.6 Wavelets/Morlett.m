% como generar una onduleta
%onda sinusoidal compleja
a=10;
f=1/a;
t=-50:0.25:50;
cos=exp(i*2*pi*f*t);
subplot(3,1,1)
plot(t,real(cos))

%campana de Gauss
a=10; %desviación standar
gaus=exp(-0.5*(t./a).^2);
subplot(3,1,2)
plot(t,gaus)

%Morlet wavelet
Morl=cos.*gaus;
subplot(3,1,3)
plot(t,real(Morl))

%con posición y escala
clear
t=0:0.1:50;
a=[2 10 20];
for j=1:length(t)
    tau=t(j);
    for i=1:length(a)
        cos(:,i)=exp(1i*2*pi*((t-tau)/a(i)));
        gaus(:,i)=exp(-0.5*((t-tau)/a(i)).^2);
        mor(:,i)=real(cos(:,i)).*gaus(:,i);
        
        subplot(3,1,1)
        plot(t,real(cos(:,i)))
        title(['j= ',num2str(j),';    a= ',num2str(a(i))])
        subplot(3,1,2)
        plot(t,gaus(:,i))
        subplot(3,1,3)
        plot(t,mor(:,i))
        if j<5
            pause
        else
        pause(0.001)
        end
    end
end




