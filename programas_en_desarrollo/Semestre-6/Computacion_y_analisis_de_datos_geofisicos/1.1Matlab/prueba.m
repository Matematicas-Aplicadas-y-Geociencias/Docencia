%Programar rutina de MATLAB para interpolar
s1=find(cond2<=42);
time3=time2(s);
indx=zeros(1,length(s1));
for i=1:length(s1)
    a=s1(i+1);
    b=s1(i)+1;
  if a==b
    indx(i)=1;
    indx(i+1)=3;
  end
end

p5=p2;
p5(s1)=0;
p5(s)=p3;
for i=1:length(s1)
    if indx(i)==0
        x2=time2(s1(i)+1);x1=time2(s1(i)-1);x=time2(s1(i));
        y2=p5(s1(i)+1);y1=p5(s1(i)-1);    
        p5(s1(i))=y1+((x-x1)/(x2-x1))*(y2-y1);     
    elseif indx(i)==1
        o=i;
        while indx(o)==1
            o=o+1;
        end
        x2=time2(s1(o)+1);x1=time2(s1(i)-1);x=time2(s1(i));
        y2=p5(s1(o)+1);y1=p5(s1(i)-1);    
        p5(s1(i))=y1+((x-x1)/(x2-x1))*(y2-y1);
    else 
        x2=time2(s1(i)+1);x1=time2(s1(i)-1);x=time2(s1(i));
        y2=p5(s1(i)+1);y1=p5(s1(i)-1);    
        p5(s1(i))=y1+((x-x1)/(x2-x1))*(y2-y1);    
    end
  end

      

             


        


