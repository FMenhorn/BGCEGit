function [ b ] = bezierRHS( N,M,DIM,Px,Py,Pz )
%BEZIERRHS Summary of this function goes here
%   Detailed explanation goes here

b=zeros(DIM*(N+1)*(M+1),1);

%number of gridpoints, does this help?
Nu = size(Px,1); %gridpoints in u direction
Nv = size(Px,2); %gridpoints in v direction

%how to iterate over triangles?
%what is Tmin, Tmax?
hu = 1/(Nu-1);
hv = 1/(Nv-1);

% figure(1)
% hold on
for i = 0:N
    for j = 0:M
        zeta = i+j*(N+1);
        BzetaNM=@(u,v)bernstein(i,N,u).*bernstein(j,M,v);
        for iu = 1:Nu-1
            for jv = 1:Nv-1
                
                umin=(iu-1)*hu;
                umax=iu*hu;
                vmin=(jv-1)*hv;
                vmax=jv*hv;
                
                
                A=[Px(iu,jv),Py(iu,jv),Pz(iu,jv)]';
                B=[Px(iu+1,jv),Py(iu+1,jv),Pz(iu+1,jv)]';
                C=[Px(iu,jv+1),Py(iu,jv+1),Pz(iu,jv+1)]';
                D=[Px(iu+1,jv+1),Py(iu+1,jv+1),Pz(iu+1,jv+1)]';
                
                UV1=[umin,umax,umax;vmin,vmin,vmax];
                P1=[A,B,D];
                
                UV2=[umin,umin,umax;vmin,vmax,vmax];
                P2=[A,C,D];
                
                
                b(DIM*zeta+(1:DIM))=b(DIM*zeta+(1:DIM))+quadrature_L2projection_tri(BzetaNM,ceil((N*M+2)/2),P1,UV1);
                b(DIM*zeta+(1:DIM))=b(DIM*zeta+(1:DIM))+quadrature_L2projection_tri(BzetaNM,ceil((N*M+2)/2),P2,UV2);
            end
        end
        plot3(Px(),Py(),Pz(),'*');
    end
end

% hold off

%corner points lie on corner points of patch
for i = [0,N]
    for j = [0,M]
        zeta = i+j*(N+1);
        cornerPti=i*(Nu-1)/N+1;
        cornerPtj=j*(Nv-1)/M+1;
        for d = 1:DIM
            if(d==1)
                b(DIM*zeta+d)=Px(cornerPti,cornerPtj);
            elseif(d==2)
                b(DIM*zeta+d)=Py(cornerPti,cornerPtj);
            elseif(d==3)
                b(DIM*zeta+d)=Pz(cornerPti,cornerPtj);
            end
        end
    end
end

end

