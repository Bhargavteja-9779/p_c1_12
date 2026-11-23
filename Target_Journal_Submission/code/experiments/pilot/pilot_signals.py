"""PILOT (exploratory, not a final result): do simple control-loop signals deviate in the 7 days before
customer fault reports, relative to the same substation's earlier days? Exploratory only; informs design."""
import pandas as pd,numpy as np,os
R="../../data/raw/predist"
def load(m,s):
    d=pd.read_csv(f"{R}/manufacturer {m}/operational_data/substation_{s}.csv",sep=';',low_memory=False)
    d['timestamp']=pd.to_datetime(d.timestamp,format='mixed'); return d.set_index('timestamp').sort_index()
def daily_feats(d):
    f=pd.DataFrame(index=d.index)
    num=lambda c: pd.to_numeric(d[c],errors='coerce') if c in d else pd.Series(np.nan,index=d.index)
    f['hc1_track']=(num('s_hc1_supply_temperature')-num('s_hc1_supply_temperature_setpoint'))
    f['hc1_short']=(-f['hc1_track']).clip(lower=0)
    f['dhw_short']=(num('s_dhw_supply_temperature_setpoint')-num('s_dhw_upper_storage_temperature')).clip(lower=0)
    f['flow0']=(num('p_net_meter_flow')<=1).astype(float).where(num('p_net_meter_flow').notna())
    f['dT_net']=num('p_net_supply_temperature')-num('p_net_return_temperature')
    return f.resample('D').mean()
rows=[]
for m in (1,2):
    F=pd.read_csv(f"{R}/manufacturer {m}/faults.csv",sep=';'); F=F[F.efd_possible==True]
    for _,e in F.iterrows():
        try: d=load(m,e['substation ID'])
        except FileNotFoundError: continue
        rep=pd.to_datetime(e['Report date']); df=daily_feats(d)
        base=df[(df.index<rep-pd.Timedelta(days=14))&(df.index>=rep-pd.Timedelta(days=120))]
        pre=df[(df.index>=rep-pd.Timedelta(days=7))&(df.index<rep)]
        if len(base)<20 or len(pre)==0: continue
        z={}
        for c in df.columns:
            mu,sd=base[c].mean(),base[c].std()+1e-6
            z[c]=np.nanmax(np.abs((pre[c]-mu)/sd)) if pre[c].notna().any() else np.nan
        rows.append(dict(m=m,sub=e['substation ID'],label=e['Fault label'],**z))
r=pd.DataFrame(rows); r['any_z>4']=(r[['hc1_short','dhw_short','flow0','dT_net','hc1_track']].max(axis=1)>4)
print(r.round(1).to_string()); print("frac with max|z|>4 in 7d pre-report:",r['any_z>4'].mean(), "n=",len(r))
