Px=[];
Py=[];
h=[];
t=0:.01:1;
x=zeros(size(t));
y=zeros(size(t));
near_h=[];
figure(1)
axis([-1 1 -1 1])
hold on
while(true)
    if(size(Px) == 0)
        N=ginput(1)';
        Px=[Px,N(1)];
        Py=[Py,N(2)];
    end
    N=ginput(1)';
    near_i=dsearchn([Px;Py]',N');
    if(norm([Px(near_i);Py(near_i)]-N)<.05);
        while(norm([Px(near_i);Py(near_i)]-N)<.05)
            near_i=dsearchn([Px;Py]',N');
            delete(near_h);
            near_h=plot(Px(near_i),Py(near_i),'ko','MarkerSize',10,'MarkerFaceColor','g');
            N=ginput(1)';
        end
        Px(near_i)=N(1);
        Py(near_i)=N(2);
    else
        Px=[Px,N(1)];
        Py=[Py,N(2)];
    end
    
    delete(h);
    for i = 1:numel(t)
        [x(i),y(i)]=bezier_casteljau(Px,Py,t(i));
    end
    h=plot(x,y,'k-',Px,Py,'kx');
    delete(near_h)
end
hold off