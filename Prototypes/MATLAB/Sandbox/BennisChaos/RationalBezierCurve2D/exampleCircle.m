P=[1 1 0;0 1 1];
POpt=[1 (sqrt(2)-1/2) 0;0 (sqrt(2)-1/2) 1];
w=ones(3,1);
w(2)=sqrt(2)/2;

[xB,yB]=bezier(POpt,.01);
[xrB,yrB]=bezierRational(P,w,.01);
xC=cos((0:.01:1)*pi/2);
yC=sin((0:.01:1)*pi/2);

figure(1)
% subplot(2,1,1)
hold on
axis square
axis([-.2 1.2 -.2 1.2])
plot(xB,yB,'b',xrB,yrB,'r',xC,yC,'k');
legend('bezier','rational bezier','circle');
plot(P(1,:),P(2,:),'r*');
plot(POpt(1,:),POpt(2,:),'b*');
plot(sqrt(2)/2,sqrt(2)/2,'+');
for i = 1:numel(w)
    text(P(1,i),P(2,i),num2str(w(i)));
end
hold off
% subplot(2,1,2)
% hold on
% plot(0:.01:1,sqrt((yC-yB).^2+(xC-xB).^2),'b',0:.01:1,sqrt((yC-yrB).^2+(xC-xrB).^2),'r');
% legend('bezier','rational bezier');
% hold off