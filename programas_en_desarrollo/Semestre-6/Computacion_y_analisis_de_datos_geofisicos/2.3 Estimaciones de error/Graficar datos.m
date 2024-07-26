Uo=u(:,22);
Vo=v(:,22);

tm=tlocal(1589:18545);
Um=u(1589:18545,310);
Vm=v(1589:18545,310);

plot(to,Vo)
hold on
plot(tm,Vm)


plot(to,Uo)
hold on
plot(tm,Um)

