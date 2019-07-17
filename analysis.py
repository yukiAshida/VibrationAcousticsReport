import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from setting import readSetting
import sys
from datetime import datetime

# MATPLOTの描画を綺麗にする（個人用）
readSetting()
fp = FontProperties(fname=r'C:\Windows\Fonts\ipaexg.ttf', size=20)

# 定数
ACCOUSTIC_VELOCITY = 340.29 #音速[m/s]
AIR_DENSITY = 1.293 #空気密度[kg/m3]
DENSITY = (7750 + 8050)/2 #鋼の密度[kg/m3]
FS_START = 100 #計算する最小周波数
FS_END = 6300 #計算する最大周波数

# ランダム入射波に対する数値解析
def allInput(f, thickness):
    """
    Parameters
    ------------
    f: float
        入力周波数[Hz]
    thickness: float
        板厚[m^2]
    
    Returns
    ------------
    r: float
        透過損失
    """
    
    omega = f*2*np.pi  #角周波数
    area_density = DENSITY*thickness #面密度[kg/m2]
    
    logarg = (omega*area_density)/(2*AIR_DENSITY*ACCOUSTIC_VELOCITY)
    r = 20*np.log10(logarg) - 10*np.log10(np.log(1+(logarg)**2))
    return r

# プロット
def plotLoss( ax, x, y, color, label):
    """
    Parameters
    ------------
    x,y: list(float)
        縦軸，横軸の値
    color,label: str
        色（#XXXXXX）, 凡例
    """
    
    plot_settings = {
        "color":color,
        "linewidth":3,
        "marker":"o",
        "markerfacecolor":"w",
        "markeredgecolor":color,
        "markersize":10,
        "markeredgewidth":3,
        "label":label
    }

    ax.plot(x, y, **plot_settings)

# Fs ~ Fe [Hz]の範囲で1/3オクターブバンド中心周波数をリストで返す
def thirdOctaveBand(Fs=100, Fe=6300):
    """
    Parameters
    ------------
    Fs, Fe: float
        周波数[Hz]
    
    Returns
    ------------
    freq_list: list(float)
        指定した周波数範囲の1/3オクターブバンドの中心周波数のリスト
    """

    # 初期化
    f_low = f_high = Fs
    freq_list = []

    while f_high <= Fe:

        # 高域遮断周波数を計算
        f_high = f_low*(pow(2,1/3))
        
        # 中心周波数
        f_center = round(np.sqrt(f_low*f_high),2)
        freq_list.append(f_center)
        
        # 低域遮断周波数を更新
        f_low = f_high

    return freq_list

def writeCsv(results, columns=["fs","d1","d2"]):

    pdata = pd.DataFrame(results)
    pdata.columns = columns

    # 日付
    time_info=datetime.today()
    day_info="{0}_{1}_{2}_{3}_{4}_{5}".format(time_info.year,time_info.month,time_info.day,time_info.hour,time_info.minute,time_info.second)

    # csv書き出し
    pdata.to_csv("{0}.csv".format(day_info), encoding="utf8")
     

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
    
    # CSV書き出し   
    if len(sys.argv)>1 and sys.argv[1] in ("-s","--save"):
        columns = ["fs", "{0} mm".format(thicknesses["d1"]*1000), "{0} mm".format(thicknesses["d2"]*1000)]
        writeCsv(results, columns)

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