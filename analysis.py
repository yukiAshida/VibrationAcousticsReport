import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from setting import readSetting

# MATPLOTの描画を綺麗にする（個人用）
readSetting()
fp = FontProperties(fname=r'C:\Windows\Fonts\ipaexg.ttf', size=20)

# 定数
ACCOUSTIC_VELOCITY = 340.29 #音速[m/s]
AIR_DENSITY = 1.293 #空気密度[kg/m3]
DENSITY = (7750 + 8050)/2 #鋼の密度[kg/m3]
FS_START = 100
FS_END = 6300

# ランダム入射波に対する数値解析
def allInput(f, thickness):    
    
    omega = f*2*np.pi  #角周波数
    area_density = DENSITY*thickness #面密度[kg/m2]
    
    logarg = (omega*area_density)/(2*AIR_DENSITY*ACCOUSTIC_VELOCITY)
    r = 20*np.log10(logarg) - 10*np.log10(np.log(1+(logarg)**2))
    return r

# プロット成形用
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

# Fs ~ Fe [Hz]の範囲で1/3オクターブバンド中心周波数をリストで返す
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

    for f in thirdOctaveBand(FS_START,FS_END):

        # 周波数を記録
        results["fs"].append(f)
        
        # 各板厚に対するランダム入力の透過損失を計算
        for thickness in thicknesses:
            r = allInput(f, thickness)
            results[str(thickness)].append(r)

    # Figureを用意
    fig = plt.figure()
    
    # 通常プロット，片対数表示
    for i in range(1,3):

        ax = fig.add_subplot(1,2,i)
        
        # 板厚ごとにプロット
        for thickness in thicknesses:
            color = results["colors"][str(thickness)]
            plotLoss(ax, results["fs"], results[str(thickness)], color=color, label="d = {0} [mm]".format(thickness*1000))
        
        # 描画設定
        ax.set_xlabel("周波数 [Hz]", FontProperties=fp)
        ax.set_ylabel("音響透過損失 [dB]", FontProperties=fp)
        ax.legend()

        # 通常 or 片対数
        if i==1:
            ax.set_title('透過損失　100～6300Hz', FontProperties=fp) 
        else:
            ax.set_title('片対数表示', FontProperties=fp)
            ax.grid(which='minor',color='w',linestyle='-')
            ax.set_xscale('log')

    plt.show()