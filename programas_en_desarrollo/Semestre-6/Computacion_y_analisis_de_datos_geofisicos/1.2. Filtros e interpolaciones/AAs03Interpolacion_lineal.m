%Cargar los datos de cond2, time2, s, cond3

%Programar rutina de MATLAB para interpolar
s=find(cond2>42);
s1=find(cond2<=42);
indx=zeros(1,length(s1));
for i=1:length(s1)
    a=s1(i+1);
    b=s1(i)+1;
  if a==b
    indx(i)=1;
    indx(i+1)=2;
  end
end

cond3=smooth(cond2(s),200);
cond5=cond2;
cond5(s1)=0;
cond5(s)=cond3;
for i=1:length(s1)
    if indx(i)==0
        x2=time2(s1(i)+1);x1=time2(s1(i)-1);x=time2(s1(i));
        y2=cond5(s1(i)+1);y1=cond5(s1(i)-1);    
        cond5(s1(i))=y1+((x-x1)/(x2-x1))*(y2-y1);     
    elseif indx(i)==1
        o=i;
        while indx(o)==1
            o=o+1;
        end
        x2=time2(s1(o)+1);x1=time2(s1(i)-1);x=time2(s1(i));
        y2=cond5(s1(o)+1);y1=cond5(s1(i)-1);    
        cond5(s1(i))=y1+((x-x1)/(x2-x1))*(y2-y1);
    else 
        x2=time2(s1(i)+1);x1=time2(s1(i)-1);x=time2(s1(i));
        y2=cond5(s1(i)+1);y1=cond5(s1(i)-1);    
        cond5(s1(i))=y1+((x-x1)/(x2-x1))*(y2-y1);    
    end
  end
plot(time2,cond5,'.')
hold on
plot(time2(s),cond3,'.r')

      

             


        


