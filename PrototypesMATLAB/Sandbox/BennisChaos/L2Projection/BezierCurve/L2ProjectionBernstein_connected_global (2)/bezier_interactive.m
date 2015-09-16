P=[];
h=[];
near_h=[];
figure(1)
axis([-1 1 -1 1])
hold on
while(true)
    if(size(P,2) == 0)
        P=[P,ginput(1)'];
    end
    N=ginput(1)';
    near_i=dsearchn(P',N');
    if(norm(P(:,near_i)-N)<.05);        
        while(norm(P(:,near_i)-N)<.05)
            near_i=dsearchn(P',N');
            delete(near_h);
            near_h=plot(P(1,near_i),P(2,near_i),'ko','MarkerSize',10,'MarkerFaceColor','g');
            N=ginput(1)';            
        end
        P(:,near_i)=N;
    else
        P=[P,N];
    end
    
    delete(h);
    [x,y]=bezier(P,.001);
    h=plot(x,y,'k-',P(1,:),P(2,:),'kx'); 
    delete(near_h)
end
hold off