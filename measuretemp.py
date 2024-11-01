import spidev
import time
import datetime
import matplotlib.pyplot as plt 

dummyData = [0x00,0x00]

dt_now = datetime.datetime.now()
path = './bismuth/programs/measuretemp_result/' + dt_now.strftime('%Y%m%d%H%M%S') + '.csv' 
f = open(path, 'w')

X, Y = [], []                     # XとYの空のリスト
start_time = time.perf_counter()  # プログラム開始時の現在の時刻

spi = spidev.SpiDev()
spi.open(0, 0)          # bus 0,cs 0

# Settings
spi.max_speed_hz = 1000000      # 1MHz
spi.mode = 3                    # SPI mode : 3


while 1:
        if len(X) > 150:           
                del X[0]           # Xの0番目(リストの左端)を削除
                X_max = X[0] + 150 # X軸の最大値設定
                del Y[0]           # Yの0番目(リストの左端)を削除

        else:
                X_max = len(X)         
        
        dt_now = datetime.datetime.now()
        readByteArray = spi.xfer2(dummyData)
        temperatureData = ((readByteArray[0] & 0b01111111) << 5) | ((readByteArray[1] & 0b11111000) >> 3)
        temperature = temperatureData * 0.25
        print(dt_now.strftime('%Y/%m/%d %H:%M:%S') + ',' + str(temperature), file=f)

        Y.append(float(temperature))                 # リストの末尾にアイテムを追加
        X.append(time.perf_counter() - start_time)   # プログラム開始からの経過時間をリストの末尾に追加
        plt.plot(X, Y, color='C1')           # X,Yをプロット
        plt.axhline(271.4, color='C0', linestyle='dashed')
        plt.ylim(0, 500)                             # Y軸の表示範囲
        plt.xlim(X[0], X_max)                        # X軸の表示範囲
        plt.xlabel('Time [s]')                       # X軸ラベル
        plt.ylabel('Temperature [deg]')              # Y軸ラベル

        plt.figure(figsize=(12,8))        # グラフのサイズを指定
        plt.rcParams["font.size"] = 20    # フォントサイズ

        plt.close()
        plt.text(X[0], 520, str(temperature) + '℃', fontsize=25)
        
        plt.pause(1)

        plt.cla()

                
f.close()
spi.close
