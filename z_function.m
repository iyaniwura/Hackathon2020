
figure()
subplot(1,3,1)
%% plotting
time = 0:0.01:100;
C = 2;
eps = 1;
t_star = 50;
z = C./(1 + exp((time - t_star)/eps));

p1 =plot(time,z)
grid on
set(gca,'FontSize',15)
set([p1],'LineWidth',4)
xlabel('time','interpreter','latex')
ylabel('z(t)','interpreter','latex')
title('\epsilon=1')
xticks(0:20:100)



subplot(1,3,2)
%% plotting
time = 0:0.01:100;
C = 2;
eps = 0.8;
t_star = 50;
z = C./(1 + exp((time - t_star)/eps));
p1 = plot(time,z)
grid on
set(gca,'FontSize',15)
set([p1],'LineWidth',4)
xlabel('time','interpreter','latex')
ylabel('z(t)','interpreter','latex')
title('\epsilon=0.8')
xticks(0:20:100)


subplot(1,3,3)
%% plotting
time = 0:0.01:100;
C = 2;
eps = 0.01;
t_star = 50;
z = C./(1 + exp((time - t_star)/eps));
p1 = plot(time,z)
grid on
set(gca,'FontSize',15)
set([p1],'LineWidth',4)
xlabel('time','interpreter','latex')
ylabel('z(t)','interpreter','latex')
title('\epsilon=0.01')
xticks(0:20:100)


x0=10;
y0=10;
width=1550;
height=400
set(gcf,'position',[x0,y0,width,height])
