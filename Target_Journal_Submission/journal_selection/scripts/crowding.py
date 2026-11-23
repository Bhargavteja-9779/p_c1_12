"""Rough crowdedness of candidate problem areas: OpenAlex count of works (2023-2026) matching a search."""
import subprocess,json,urllib.parse,csv,time
Q={
 "wind_scada_fault":'wind turbine SCADA anomaly detection',
 "hdd_failure":'hard disk drive failure prediction SMART',
 "water_leak":'water distribution network leak detection machine learning',
 "hvac_fdd":'HVAC fault detection and diagnosis machine learning',
 "pv_forecast":'solar photovoltaic power forecasting deep learning',
 "fraud_delay":'fraud detection verification latency delayed labels',
 "flood_lstm":'streamflow prediction LSTM ungauged basins',
 "sepsis_alarm":'sepsis early warning alarm fatigue machine learning',
 "battery_life":'battery cycle life early prediction machine learning',
 "aq_sensor_calib":'low-cost air quality sensor calibration machine learning',
 "secom":'semiconductor manufacturing yield prediction SECOM',
 "railway":'railway track defect prediction machine learning',
 "district_heating":'district heating substation fault detection',
 "ev_charging":'electric vehicle charging demand forecasting',
 "drought_crop":'crop yield forecasting machine learning county',
 "power_outage_storm":'power outage prediction storms machine learning',
 "dam_seepage":'dam deformation monitoring prediction machine learning',
 "bridge_shm_temp":'structural health monitoring environmental variability damage detection',
}
w=csv.writer(open('../journal_selection/topic_crowding.csv','w'));w.writerow(["key","query","works_2023_2026"])
for k,q in Q.items():
    u="https://api.openalex.org/works?search="+urllib.parse.quote(q)+"&filter=publication_year:2023-2026&per-page=1&select=id"
    out=json.loads(subprocess.run(["curl","-s","-m","60",u],capture_output=True,text=True).stdout)
    w.writerow([k,q,out['meta']['count']]); print(k,out['meta']['count']); time.sleep(0.3)
