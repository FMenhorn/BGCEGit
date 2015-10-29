data = dlmread('param.csv',';');

id = data(:,1);
u = data(:,2);
v = data(:,3);

ids = unique(id);
figure(1)
plot([0,0,1,1,0],[0,1,1,0,0],'g')
for i = 1:numel(ids)
    disp(i)
    hold on
    h = plot(u(id==ids(i)),v(id==ids(i)),'*');
    pause()
    delete(h)
    hold off
end

