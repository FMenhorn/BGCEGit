function [x,y,z] = bezier(P,h)
% BEZIER Returns x,y,z values of a 3D bezier-curve with the given control points P and
% stepwidth h

[u,v]=meshgrid(0:h:1);

x=zeros(size(u));
y=zeros(size(u));
z=zeros(size(u));

n=size(P,2)-1;
m=size(P,3)-1;

for i = 0:n
    for j = 0:m
        x=x+bernstein(i,n,u).*bernstein(j,m,v)*P(1,i+1,j+1);
        y=y+bernstein(i,n,u).*bernstein(j,m,v)*P(2,i+1,j+1);
        z=z+bernstein(i,n,u).*bernstein(j,m,v)*P(3,i+1,j+1);
    end
end

end