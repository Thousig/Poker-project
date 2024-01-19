#DDQN Data
DDQN = c(0.83, 0.81, 0.54, 0.85, 0.4, 0.9, 0.98, 0.90, 0.28, 0.78, 0.41, 0.74, 0.75, 0.90, 0.13,
         0.87, 0.63, 0.97, 0.75, 0.82, 0.47, 0.54, 0.04, 0.8, 0.74, 0.72, 0.03, 0.53, 0, 0)

mean(DDQN)
sd(DDQN)
var(DDQN)


#Calculation of confidence interval for DDQN
DDQN_conf_interval = mean(DDQN) + c(-1,1) * qt(0.975, df = 29) * sd(DDQN)/sqrt(30)
DDQN_conf_interval



#DQN Data
DQN = c(0.97 , 0.97, 0.97, 0.97 , 0.99, 0.98, 0.98, 0.95, 0.97, 0.96, 0.96, 0.96, 0.98, 0.98, 0.92,
        0.97, 0.97, 0.97, 0.93, 0.93, 0.89, 0.89, 0.94, 0.91, 0.93, 0.92, 0.92, 0.94, 0.91, 0.91)
mean(DQN)
var(DQN)
sd(DQN)
#Calculate of confidence interval for DQN
DQN_conf_interval = mean(DQN) + c(-1,1) * qt(0.975, df = 29) * sd(DQN)/sqrt(30)
DQN_conf_interval
