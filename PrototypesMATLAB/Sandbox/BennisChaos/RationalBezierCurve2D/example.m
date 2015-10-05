x=0:10;

P=[x;sin(x/numel(x)*pi*2)];
w=ones(numel(x),1);

[x,y]=bezier(P,.01);
[xx,yy]=bezierRational(P,w,.01);

figure(1)
subplot(2,1,1)
hold on
title('non-rational')
plot(x,y,'r-')
plot(P(1,:),P(2,:),'r*')
hold off

subplot(2,1,2)
hold on
title('rational')
plot(xx,yy)
plot(P(1,:),P(2,:),'b*')
hold off

while(1)
    
pause()

w(2)=2*w(2);
w(end-2)=w(end-2)/2;
[xx,yy]=bezierRational(P,w,.01);

subplot(2,1,2)
hold on
plot(xx,yy)
hold off

end
