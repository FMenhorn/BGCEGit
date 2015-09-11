n = 3; %degree of fit
m = 3; %number of intervals in knot vector

t = [zeros(1,n-1),linspace(0,1,m),ones(1,n-1)];

%sample data
phi = linspace(0,pi,50)';
P=[cos(phi),sin(pi*cos(phi)),zeros(size(phi))];

%first guess for chord length
% -> in Eck/Hoppe we get this from the previous steps!
x=(linspace(0,1,numel(phi))');
%x=chordLength(P,t);

C=setupLSQmatrix(x,t,n);
B=C\P;

[X,Y,Z]=NURBS( B,0:.005:1,t,n );

it = 0;
itmax=10;

figure(1)
subplot(2,1,1)
hold on
title('fit')
plot3(P(:,1),P(:,2),P(:,3),'b*');
h1=plot3(X,Y,Z);
%plot3(B(:,1),B(:,2),B(:,3),'r*','MarkerSize',20);
%pause();
hold off
subplot(2,1,2)
hold on
title('parameter space')
h2=plot(x,it*ones(size(x)),'.');
axis([0 1 -1 itmax]);
hold off
pause(.01)
%delete([h1,h2]);

P_c=C*B;% points on the curve -> P-P_c gives deviation
D=P-P_c;
figure(1)
hold on
%quiver3(P_c(:,1),P_c(:,2),P_c(:,3),D(:,1),D(:,2),D(:,3),0)
hold off


while(it<itmax)
    it = it+1;
    [x,dx]=reparametrize(D,B,x,t,n);
    disp 'Error:' %how to estimate error? See RogersFog1989
    mean(dx)
    
    C=setupLSQmatrix(x,t,n);
    B=C\P;
    P_c=C*B;% points on the curve -> P-P_c gives deviation
    D=P-P_c;
    
    [X,Y,Z]=NURBS( B,0:.005:1,t,n );
    
    figure(1)    
    subplot(2,1,1)
    hold on    
    if(it == itmax)
        h1=plot3(X,Y,Z);
        legend('data','first','last')
    end
    hold off
    subplot(2,1,2)
    hold on    
    h2=plot(x,it*ones(size(x)),'.');    
    hold off
    pause(.01)
    %delete([h1,h2]);
end

