function [ c ] = getConnectedNodes( f,v,i )
%GETCONNECTEDNODES Summary of this function goes here
%   Detailed explanation goes here

l=mod(find(f==i),size(f,1)); %lines, meaning triangles, where node i is part of.
l(l==0)=size(f,1);
vc=f(l,:);
c=unique(vc(vc~=i));


end

