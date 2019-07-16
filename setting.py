# ==================================
# matplotlibの描画設定用ファイル
# ==================================

import matplotlib.pyplot as plt
import cycler
import numpy as np
import json
import os

def readSetting():

    filepass = os.path.dirname(__file__) + "/settings/default.json"

    f = open(filepass, "r")
    data = json.load(f)
    f.close()

    convert_name = {
        "grid.on": "axes.grid",
        "grid.axis": "axes.grid.axis",
        "grid.which": "axes.grid.which",
        "grid.below": "axes.axisbelow",
        "frame.top":"axes.spines.top",
        "frame.bottom":"axes.spines.bottom",
        "frame.left":"axes.spines.left",
        "frame.right":"axes.spines.right",
        "frame.edgecolor":"axes.edgecolor",
        "frame.facecolor":"axes.facecolor",
        "frame.linewidth":"axes.linewidth",
        "title.pad":"axes.titlepad",
        "title.size":"axes.titlesize",
        "title.weight":"axes.titleweight",
        "margin.x":"axes.ymargin",
        "margin.y":"axes.xmargin",
        "date.day":"date.autoformatter.day",
        "date.hour":"date.autoformatter.hour",
        "date.microsecond":"date.autoformatter.microsecond",
        "date.minute":"date.autoformatter.minute",
        "date.month":"date.autoformatter.month",
        "date.second":"date.autoformatter.second",
        "date.year":"date.autoformatter.year",
        "label.color":"axes.labelcolor",
        "label.pad":"axes.labelpad",
        "label.size":"axes.labelsize",
        "label.weight":"axes.labelweight",
        "xtick.minor":"xtick.minor.visible",
        "ytick.minor":"ytick.minor.visible",
        "color.default":"axes.prop_cycle"
    }

    connection_data = { first_key+"."+second_key :value  for first_key, values in data.items() for second_key, value in values.items() }
    for key,val in connection_data.items():
        original_key = convert_name[key] if key in convert_name else key  
        
        if original_key == "axes.prop_cycle":
            __setDefaultColor(val)
        else:
            plt.rcParams[original_key] = val

def __setDefaultColor(colors):
    plt.rcParams["axes.prop_cycle"] = cycler.cycler( color=list(colors.values()) )