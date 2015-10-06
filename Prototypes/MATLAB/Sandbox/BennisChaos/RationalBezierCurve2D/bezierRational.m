function [x,y] = bezierRational(P,w,h)
% BEZIERRATIONAL Returns x,y values of a bezier-curve with the given control points P , weights w and
% stepwidth h

t=0:h:1;

N_t=numel(t);
x=zeros(1,N_t);
y=zeros(1,N_t);

n=size(P,2)-1;

for i = 0:n
    x=x+w(i+1)*bernstein(i,n,t)*P(1,i+1);
    y=y+w(i+1)*bernstein(i,n,t)*P(2,i+1);
end

SUMwB=0;
for i = 0:n
    SUMwB=SUMwB+w(i+1)*bernstein(i,n,t);
end

x=x./SUMwB;
y=y./SUMwB;

end