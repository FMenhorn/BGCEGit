function [ TX,TY,TZ ] = Triangle(Px,Py,Pz)
%TRIANGLE Summary of this function goes here
%   Detailed explanation goes here

D=3;

%number of gridpoints, does this help?
Nu = size(Px,1); %gridpoints in u direction
Nv = size(Px,2); %gridpoints in v direction

%how to iterate over triangles?
%what is Tmin, Tmax?
hu = 1/(Nu-1);
hv = 1/(Nv-1);

for iu = 1:Nu-1
    for jv = 1:Nv-1
        
        A=[Px(iu,jv),Py(iu,jv),Pz(iu,jv)]';
        B=[Px(iu+1,jv),Py(iu+1,jv),Pz(iu+1,jv)]';
        C=[Px(iu,jv+1),Py(iu,jv+1),Pz(iu,jv+1)]';
        D=[Px(iu+1,jv+1),Py(iu+1,jv+1),Pz(iu+1,jv+1)]';
        AB=B-A;
        AC=C-A;
        DB=B-D;
        DC=C-D;
        
        uT=@(u)(u/hu-(iu-1));
        vT=@(v)(v/hv-(jv-1));
        
        %bilinear
        %         T=@(u,v,d)(1-uT(u)).*(1-vT(v)).*A(d)+uT(u).*(1-vT(v))*B(d)+(1-uT(u)).*vT(v)*C(d)+uT(u).*vT(v)*D(d);
        
        %linear
        T=@(u,v,d)  heaviside(1-u-v).*(...
            A(d)+AB(d).*u+AC(d).*v...
            )+...
            heaviside(-1+u+v).*(...
            D(d)+DB(d).*(1-v)+DC(d).*(1-u)...
            );
        
        [U,V]=meshgrid((iu-1)*hu:hu/10:iu*hu,(jv-1)*hv:hv/10:jv*hv);
        TX((iu-1)*10+1:iu*10+1,(jv-1)*10+1:jv*10+1)=T(uT(U),vT(V),1)';
        TY((iu-1)*10+1:iu*10+1,(jv-1)*10+1:jv*10+1)=T(uT(U),vT(V),2)';
        TZ((iu-1)*10+1:iu*10+1,(jv-1)*10+1:jv*10+1)=T(uT(U),vT(V),3)';
    end
end




end

