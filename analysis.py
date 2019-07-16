import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from setting import readSetting

readSetting()
fp = FontProperties(fname=r'C:\Windows\Fonts\ipaexg.ttf', size=20)

# 特性
ACCOUSTIC_VELOCITY = 340.29 #音速[m/s]
AIR_DENSITY = 1.293 #空気密度[kg/m3]
#DENSITY = 8.96*0.001*1000000 
DENSITY = (7750 + 8050)/2 #鋼の密度[kg/m3]

# 解析条件
FS_START = 100
FS_END = 6300
# FS_STEP = 250

# N = 1000

# def calcLossTheta(theta, f, thickness):

#     omega = f*2*np.pi  #角周波数
#     area_density = DENSITY*thickness #面密度[kg/m2]
    
#     top = omega*area_density*np.cos(theta) # 式中の分子
#     bottom = 2*AIR_DENSITY*ACCOUSTIC_VELOCITY # 式中の分母

#     loss = 10*np.log10( 1 + (top/bottom)**2 )
#     return theta, loss

# def randamInput(f, thickness):
    
#     # ユニバーサル関数に変換
#     fnp = np.frompyfunc(calcLossTheta, 3, 2)
    
#     # θを乱数として入力・計算
#     theta_random = np.random.rand(N)*np.pi/2
#     _, rs = fnp(theta_random, f, thickness)

#     # 計算結果を平均化（ここ怪しい）
#     r = np.mean(rs)

#     return r

def allInput(f, thickness):    
    
    omega = f*2*np.pi  #角周波数
    area_density = DENSITY*thickness #面密度[kg/m2]
    
    logarg = (omega*area_density)/(2*AIR_DENSITY*ACCOUSTIC_VELOCITY)
    r = 20*np.log10(logarg) - 10*np.log10(np.log(1+(logarg)**2))
    return r

def plotLoss( ax, x, y, color, label):

    C = color
    plot_settings = {
        "color":C,
        "linewidth":3,
        "marker":"o",
        "markerfacecolor":"w",
        "markeredgecolor":C,
        "markersize":10,
        "markeredgewidth":3,
        "label":label
    }

    ax.plot(x, y, **plot_settings)

def thirdOctaveBand(Fs=100, Fe=6300):

    f_low = Fs
    freq_list = []

    while True:

        f_high = f_low*(pow(2,1/3))
        f_center = round(np.sqrt(f_low*f_high),2)
        freq_list.append(f_center)
        f_low = f_high

        if f_high > Fe:
            break
    
    return freq_list

if __name__ == "__main__":
    
    # 板厚 [m]
    thicknesses = [0.0007, 0.0045]
    colors = ["#66aa66","#6666aa"]
    
    # 計算結果格納リスト
    results = { str(thickness):[] for thickness in thicknesses }
    results["fs"] = []
    results["colors"] = { str(t):c for t,c in zip(thicknesses, colors) }


    # 各周波数ごとにθをランダム入力
    #for i,f in enumerate(range(FS_START, FS_END+FS_STEP-1, FS_STEP)):
    
    freq_list = thirdOctaveBand(FS_START,FS_END)
    for i,f in enumerate(freq_list):

        # 周波数を記録
        results["fs"].append(f)
        
        # 各板厚に対するランダム入力の透過損失を計算
        for thickness in thicknesses:
            #r = randamInput(f, thickness)
            r = allInput(f, thickness)
            results[str(thickness)].append(r)

        # デバッグ
        percentage = int(100*(i+1)/len(freq_list))
        print("{0}Hz completed. ({1}%)".format(f,percentage))

    # Figureを用意
    fig = plt.figure()
    
    for i in range(1,3):

        ax = fig.add_subplot(1,2,i)
        
        # 描画
        for thickness in thicknesses:

            color = results["colors"][str(thickness)]
            plotLoss(ax, results["fs"], results[str(thickness)], color=color, label="d = {0} [mm]".format(thickness*1000))
        
        # 描画設定
        ax.set_xlabel("周波数 [Hz]", FontProperties=fp)
        ax.set_ylabel("音響透過損失 [dB]", FontProperties=fp)
        ax.legend()

        if i==1:
            ax.set_title('透過損失　100～6300Hz', FontProperties=fp) 
        else:
            ax.set_title('片対数表示', FontProperties=fp)
            ax.grid(which='minor',color='w',linestyle='-')
            ax.set_xscale('log')

    plt.show()