import tensorflow as tf
import numpy as np
import game,cv2,random
import matplotlib.pyplot as plt
from collections import deque #for append ,pops replay memory
Actions=5 #上,下,左,右,原地
Gamma=0.99 #learing rate

Epsilon_s=1
Epsilon_f=0.05

Explore=500000 
Observe=50000 

Memory=500000 #把之前的memory存起來
Batch_size=128


def tfGraph():
    w1=tf.Variable(tf.zeros([8,8,4,32]))
    b1=tf.Variable(tf.zeros([32]))

    w2=tf.Variable(tf.zeros([4,4,32,64]))
    b2=tf.Variable(tf.zeros([64]))

    w3=tf.Variable(tf.zeros([3,3,64,64]))
    b3=tf.Variable(tf.zeros([64]))

    w4=tf.Variable(tf.zeros([3136,784]))
    b4=tf.Variable(tf.zeros([784]))

    w5=tf.Variable(tf.zeros([784,Actions]))
    b5=tf.Variable(tf.zeros([Actions]))

    #將讀入的遊戲畫面輸入
    Input=tf.placeholder("float",[None,84,84,4])
    cnn1=tf.nn.relu(tf.nn.conv2d(Input,w1,strides=[1,4,4,1],padding="VALID")+b1)
    cnn2=tf.nn.relu(tf.nn.conv2d(cnn1,w2,strides=[1,2,2,1],padding="VALID")+b2)
    cnn3=tf.nn.relu(tf.nn.conv2d(cnn2,w3,strides=[1,1,1,1],padding="VALID")+b3)
    Flatten_cnn3=tf.reshape(cnn3,[-1,3136]) #將cnn攤平
    d4=tf.nn.relu(tf.matmul(Flatten_cnn3,w4)+b4)
    Output=tf.matmul(d4,w5)+b5  #最後一層線性組合
    return Input,Output

def Training(sess,Input,Output):
    gt=tf.placeholder("float",[None])
    best=tf.placeholder("float",[None,Actions]) #將最好的動作挑出
    ###定義action
    action=tf.reduce_sum(tf.multiply(Output,best),reduction_indices=1)
    ###定義cost function, 訓練的過程中要盡量minimize
    cost=tf.reduce_mean(tf.square(action-gt)) #by mean square error
    optimizer=tf.train.AdamOptimizer(1e-3).minimize(cost)
    ###init 我們寫好的遊戲
    pong=game.Game()
    #用queue來儲存policy
    Queue=deque()
    checkPoint=tf.train.Saver() #把目前訓練的成果記下來
    #得到pygame的環境
    screen_shot=pong.NowFrame()
    #將圖片resolution降低，轉成灰階以加快cnn速度
    screen_shot=cv2.cvtColor(cv2.resize(screen_shot,(84,84)),cv2.COLOR_BGR2GRAY)
    #只有黑白
    ret,screen_shot=cv2.threshold(screen_shot,1,255,cv2.THRESH_BINARY)
    Tensor_in=np.stack((screen_shot,screen_shot,screen_shot,screen_shot),axis=2)
    #將圖片當tensor餵進去
    sess.run(tf.initialize_all_variables())
    checkpoint=tf.train.get_checkpoint_state("model")
    if checkpoint and checkpoint.model_checkpoint_path:
         checkPoint.restore(sess, checkpoint.model_checkpoint_path)
         print ("Successfully loaded:", checkpoint.model_checkpoint_path)
    else:
         print ("Could not find old network weights")
    Epsilon=Epsilon_s
    iteration=0 ##紀錄train到第幾個iteration了
    episode=[]
    Epi=[]
    count_episoed=0
    while(1):
        Score=0
        for c in range(5000):
            out=Output.eval(feed_dict={Input:[Tensor_in]})[0]
            #決定動作
            ac=np.zeros([Actions])
            #ac=np.zeros([5])
            if np.random.random()<=Epsilon: #explore
                bestMove=np.random.randint(0,5,1)
                #bestMove=np.random.randint(0,3,1)
            else: #Base on Policy
                bestMove=np.argmax(out)
            ac[bestMove]=1
            if Epsilon>Epsilon_f:  #更新epsilon, epsilon越大就越observe環境，反之則是以學到的Policy 反應
                Epsilon-=(Epsilon_s-Epsilon_f)/Explore
            reward,screen_shot=pong.NextFrame(ac) #將選擇的動作帶入下一步動作
            Score+=reward
            #回傳遊戲畫面
            screen_shot=cv2.cvtColor(cv2.resize(screen_shot,(84,84)),cv2.COLOR_BGR2GRAY)
            ret,screen_shot=cv2.threshold(screen_shot,1,255,cv2.THRESH_BINARY)
            screen_shot=np.reshape(screen_shot,(84,84,1))
            #新的一層
            In_t1=np.append(screen_shot,Tensor_in[:,:,0:3],axis=2)
            Queue.append((Tensor_in,ac,reward,In_t1))
            if len(Queue)>Memory:Queue.popleft()
            if iteration>Observe: #一開始先observe, 之後再開始訓練
                miniBatch=random.sample(Queue,Batch_size)
                In_b=[d[0]for d in miniBatch]
                best_Ac=[d[1]for d in miniBatch]
                reward_b=[d[2]for d in miniBatch]
                In_t1_b=[d[3]for d in miniBatch]
                out_batch=Output.eval(feed_dict={Input:In_t1_b})
                Q_learn=[]
                for i in range(Batch_size):
                    Q_learn.append(reward_b[i]+Gamma*np.max(out_batch[i]))
                #Opitmization
                optimizer.run(feed_dict={gt:Q_learn,best:best_Ac,Input:In_b})
                Tensor_in=In_t1
            iteration+=1
            if iteration%10000==0:
                checkPoint.save(sess,'model/'+str(iteration))
            print("TIMESTEP", iteration, "/ EPSILON", Epsilon, "/ ACTION", bestMove, "/ REWARD", reward, "/ Q_MAX %e" % np.max(out))
        #print(Score)
        episode.append(Score)
        Epi.append(count_episoed)
        if count_episoed%10==0:
            plt.figure()
            plt.plot(Epi,episode)
            plt.xlabel("game episode")
            plt.ylabel("rewards")
            plt.savefig("figure/"+str(count_episoed)+".png")
        count_episoed+=1

if __name__=="__main__":
    sess=tf.InteractiveSession()
    Input,Output=tfGraph()
    Training(sess,Input,Output)
