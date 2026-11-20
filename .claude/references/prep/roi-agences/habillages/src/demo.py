# Démo : tous les habillages enchaînés sur un fond gris foncé animé neutre (H.264).
import subprocess, sys, os
FF = sys.argv[1]; D = sys.argv[2]  # ffmpeg, dossier des .mov
seq = [('01_10000',2.0),('02_ligne-depart',1.52),('03_la-defense',2.0),('04_5km',1.0),('05_10km',1.0),
       ('06_arena',2.0),('07_networking',2.52),('08_compteur',2.52),('09_public',2.0),('10_2027',1.52),
       ('11_agence',3.0),('12_pas-tout',2.52),('13_signature',4.0)]
flash_before = {'04_5km','06_arena','11_agence','13_signature'}
t = 0.5; gap = 0.55; ev = []
for name, d in seq:
    if name in flash_before:
        ev += [("00_flash-rouge", t - 0.3)]
    ev += [(name, t)]; t += d + gap
total = round(t - gap + 0.2, 2)
inputs = []; fc = []
fc += [f"gradients=s=1920x1080:r=25:d={total}:c0=0x1c1c1c:c1=0x3a3a3a:c2=0x262626:c3=0x303030:n=4:speed=0.006:seed=7,"
          f"format=rgba[bg0]"]
prev = 'bg0'
for i, (name, st) in enumerate(ev):
    inputs += ['-i', os.path.join(D, name + '.mov')]
    fc += [f"[{i}:v]scale=in_color_matrix=bt709:in_range=tv,format=rgba,setpts=PTS-STARTPTS+{st:.2f}/TB[v{i}]"]
    fc += [f"[{prev}][v{i}]overlay=format=rgb:eof_action=pass:repeatlast=0[bg{i+1}]"]
    prev = f'bg{i+1}'
fc += [f"[{prev}]scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[out]"]
cmd = [FF, '-y', '-loglevel', 'error'] + inputs + ['-filter_complex', ';'.join(fc), '-map', '[out]',
       '-t', str(total), '-r', '25', '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-pix_fmt', 'yuv420p',
       '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-movflags', '+faststart',
       os.path.join(D, 'demo-habillages.mp4')]
for name, st in ev: print(f"{st:6.2f} s  {name}")
print('durée', total)
subprocess.run(cmd, check=True)
