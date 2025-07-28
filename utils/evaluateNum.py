import numpy as np
import csv
import config

def evaluateNum(time, title_list, rains_list, gs_rain, nest_num):

    x_range = gs_rain.shape[0]
    y_range = gs_rain.shape[1]

    margin = 5

    for i in range(len(rains_list)):

        count = 0
        rain_abs_all = 0
        rain_gs_all = 0

        for x in range(x_range):

            if (x <= margin):
                continue

            for y in range(y_range):
                
                if (y <= margin):
                    continue

                rain_hour_gs = gs_rain[x][y]
                rain_wrf = rains_list[i].values[x][y]

                # print('rain hour gs', rain_hour_gs)
                # print('rain wrf', rain_wrf)

                if (rain_hour_gs and rain_wrf):

                    if (rain_hour_gs > 3 or rain_wrf > 3):
                        count += 1
                        rain_gs_all += rain_hour_gs
                        rain_abs_all += np.abs(rain_hour_gs - rain_wrf)

                    


        

        if (count != 0):
            print('count', count)
            print('abs', rain_abs_all)
            print('mean', rain_abs_all/count, ' mm/h') 
            
            with open(f'data/evaluate_log/{config.COMPARE_WRF_IMAGE_FOLDERNAME}.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([time, title_list[i], nest_num,(rain_abs_all/rain_gs_all)])
                        
        


    
        


