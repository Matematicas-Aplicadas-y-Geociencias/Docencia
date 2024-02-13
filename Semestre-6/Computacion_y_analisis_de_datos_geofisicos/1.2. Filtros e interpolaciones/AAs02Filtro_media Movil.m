%% Media móvil %%
y=cond2(s);
N=length(y);
o=0;
w=100; % tamaño de la ventana...

for i=1:N
    y2(i)=mean(y(i:o+w));
    if (o+w)<N
        o=i;
    else
        o=o;
      
    end
end
%%
plot(time2(s),y)
hold on
plot(time2(s),y2,'.r')

