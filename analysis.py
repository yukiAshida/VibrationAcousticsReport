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
    thicknesses = {"d1":0.0007, "d2":0.0045}

    # 計算結果
    results = {"fs":[], "d1":[], "d2":[]}
    
    # 各周波数に対する透過損失を計算・記録
    for f in thirdOctaveBand(FS_START,FS_END):

        # 周波数を記録
        results["fs"].append(f)
        
        # 各板厚に対するランダム入力の透過損失を計算・記録
        for dkey, dval in thicknesses.items():
            r = allInput(f, dval)
            results[dkey].append(r)

    # 描画用
    fig = plt.figure()
    axes = [ fig.add_subplot(1,2,i) for i in (1,2) ]
    titles = ["透過損失　100～6300Hz","片対数表示"]
    colors = {"d1":"#66aa66","d2":"#6666aa"}
    
    # 通常プロット，片対数表示
    for i in range(2):
        
        # 板厚ごとにプロット
        for dkey, dval in thicknesses.items():
            plotLoss(axes[i], results["fs"], results[dkey], color=colors[dkey], label="d = {0} [mm]".format(dval*1000))
        
        # 軸周り設定
        axes[i].set_title(titles[i], FontProperties=fp)
        axes[i].set_xlabel("周波数 [Hz]", FontProperties=fp)
        axes[i].set_ylabel("音響透過損失 [dB]", FontProperties=fp)
        axes[i].legend()

        # 片対数
        if i==1:
            axes[i].grid(which='minor',color='w',linestyle='-')
            axes[i].set_xscale('log')

    plt.show()