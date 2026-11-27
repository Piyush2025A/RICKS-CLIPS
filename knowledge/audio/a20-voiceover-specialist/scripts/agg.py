import json,numpy as np,csv
rows=[]
for n in range(1,31):
    o=json.load(open(f'aud_{n}.json'));g=np.array(o['gaps'])
    ph=o['phrases'];pd=np.array([p[1] for p in ph]);ps=np.array([p[2] for p in ph])
    # gaps >=0.3 sentence/phrase pauses
    r=dict(key=f"RC30-{n:02d}",dur_s=round(o['dur'],2),lufs_i=o['lufs_i'],lra=o['lra'],true_peak_dbtp=o['tp'],
      L_rms_db=round(o['L_rms_db'],2),R_rms_db=round(o['R_rms_db'],2),LR_diff_db=round(o['L_rms_db']-o['R_rms_db'],2),
      side_minus_mid_db=round(o['side_minus_mid_db'],1),lr_corr=round(o['lr_corr'],4),
      first_active_s=o['first_active_s'],active_frac=round(o['active_frac'],3),
      syl_rate_active=round(o['syl_rate_active'],2),syl_rate_overall=round(o['syl_rate_overall'],2),mod_peak_hz=round(o['mod_peak_hz'],2),
      n_gaps150=len(g),gaps_per_s=round(len(g)/o['dur'],2),gap_med_s=round(float(np.median(g)),2),gap_p90_s=round(float(np.percentile(g,90)),2),
      n_gaps_ge300=int((g>=0.3).sum()),n_gaps_ge500=int((g>=0.5).sum()),n_gaps_ge1000=int((g>=1.0).sum()),pause_total_gt025_s=round(o['pause_total_gt025'],2),
      pause_frac=round(o['pause_total_gt025']/o['dur'],3),
      phrase_med_s=round(float(np.median(pd)),2),phrase_syl_med=float(np.median(ps)),
      vo_bed_diff_db=round(o['vo_bed_diff_db'],1),sp_active_db=round(o['sp_active_db_med'],1),sp_pause_db=round(o['sp_pause_db_med'],1),
      lowband_active_minus_pause_db=round(o['low_active_db']-o['low_pause_db'],1),
      f0_med_hz=round(o['f0_med']),f0_p10=round(o['f0_p10']),f0_p90=round(o['f0_p90']),f0_std_st=round(o['f0_std_semitones'],2),f0_voiced_active_frac=round(o['f0_voiced_active_frac'],2),f0_voiced_pause_frac=round(o['f0_voiced_pause_frac'],2),
      centroid_active_hz=round(o['centroid_active_med']),centroid_pause_hz=round(o['centroid_pause_med']))
    rows.append(r)
w=csv.DictWriter(open('/home/piyush/RICKS-CLIPS/knowledge/audio/a20-voiceover-specialist/data/audio_per_video.csv','w'),fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def st(k):
    v=np.array([r[k] for r in rows],float);return k,round(np.median(v),2),round(np.percentile(v,25),2),round(np.percentile(v,75),2),round(v.min(),2),round(v.max(),2)
for k in ['lufs_i','lra','true_peak_dbtp','LR_diff_db','side_minus_mid_db','lr_corr','first_active_s','active_frac','syl_rate_active','syl_rate_overall','mod_peak_hz','gaps_per_s','gap_med_s','n_gaps_ge300','n_gaps_ge500','n_gaps_ge1000','pause_total_gt025_s','pause_frac','phrase_med_s','phrase_syl_med','vo_bed_diff_db','lowband_active_minus_pause_db','f0_med_hz','f0_p10','f0_p90','f0_std_st','f0_voiced_pause_frac','centroid_active_hz','centroid_pause_hz']:print(st(k))
allg=np.concatenate([json.load(open(f'aud_{n}.json'))['gaps'] for n in range(1,31)])
print('allgaps',len(allg),np.percentile(allg,[10,25,50,75,90,99]).round(2))
h,b=np.histogram(allg,bins=[0.15,0.2,0.25,0.3,0.4,0.5,0.75,1.0,1.5,2.5,10]);print(h,b)
print([ (r['key'],r['lufs_i']) for r in rows if r['lufs_i']>-14.5])
