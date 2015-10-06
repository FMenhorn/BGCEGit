function [ Qx,Qy ] = bezier_casteljau( Px,Py,t )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

n=numel(Px);

if(n==2)
    Qx = Px(1)*(1-t)+Px(2)*t;
    Qy = Py(1)*(1-t)+Py(2)*t;
else
    Rx = Px(1:n-1)*(1-t)+Px(2:n)*t;
    Ry = Py(1:n-1)*(1-t)+Py(2:n)*t;
    [Qx,Qy] = bezier_casteljau(Rx,Ry,t);
end

end

