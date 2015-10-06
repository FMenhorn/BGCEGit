function [ b ] = bezierRHS( N,D,S )
%BEZIERRHS Summary of this function goes here
%   Detailed explanation goes here

b=zeros(2*(N+1),1);

m = size(S,2);
h = 1/(m-1);
Tmin=(0:m-2)*h;
Tmax=Tmin+h;

figure(1)
hold on

for i = 0:N
    BiN=@(t)bernstein(i,N,t);
    for j = 1:m-1
        for d = 1:D
            s = @(t) (1-(t-Tmin(j))/h)*S(d,j)+((t-Tmin(j))/h)*S(d,j+1);
            f = @(t) BiN(t).*s(t);
            b(D*i+d)=b(D*i+d)+integral(f,Tmin(j),Tmax(j));            
            if(d==1)
                sx=s(Tmin(j):.01:Tmax(j));
            else
                sy=s(Tmin(j):.01:Tmax(j));
            end
        end
        plot(S(1,j),S(2,j),'*');
        plot(sx,sy,'-');
    end    
end

plot(S(1,m),S(2,m),'*');

hold off

end

