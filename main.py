from PIL import Image, ImageDraw, ImageFont
import numpy as np
from collections import defaultdict

def read_img(fp):
    img = Image.open(fp).convert("RGB")
    w, h = img.size
    r, g, b = np.zeros((w, h)), np.zeros((w, h)), np.zeros((w, h))
    px = img.load()
    for i in range(w):
        for j in range(h):
            r[i, j], g[i, j], b[i, j] = px[i, j]
    return r, g, b, w, h

def ff(r, g, b, v, x, y, w, h, t, oid):
    stk = [(x, y)]
    sc = (r[x, y], g[x, y], b[x, y])
    tc = np.array([0, 0, 0], dtype=np.float64)
    pxl = []
    while stk:
        cx, cy = stk.pop()
        if v[cx][cy]:
            continue
        v[cx][cy] = True
        cc = (r[cx, cy], g[cx, cy], b[cx, cy])
        tc += cc
        pxl.append((cx, cy))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h and not v[nx][ny]:
                nc = (r[nx, ny], g[nx, ny], b[nx, ny])
                if sum(abs(sc[i] - nc[i]) for i in range(3)) <= t:
                    stk.append((nx, ny))
    pc = len(pxl)
    if pc > 0:
        ac = tuple((tc / pc).astype(int))
        return pxl, ac
    return [], (0, 0, 0)

def seg_obj(fp, t=30, ms=100):
    r, g, b, w, h = read_img(fp)
    v = np.zeros((w, h), dtype=bool)
    objs = {}
    oclr = {}
    oid = 0
    for i in range(w):
        for j in range(h):
            if not v[i][j]:
                px, avg = ff(r, g, b, v, i, j, w, h, t, oid + 1)
                if len(px) >= ms:
                    oid += 1
                    objs[oid] = px
                    oclr[oid] = avg
    osz = {k: len(v) for k, v in objs.items()}
    loid = max(osz, key=osz.get, default=None)
    if loid is not None:
        objs[0] = objs.pop(loid)
        oclr[0] = oclr.pop(loid)
    return objs, oclr, w, h

def save_overlay(ol, w, h, op, pad=10, fz=15):
    from collections import Counter
    osz = Counter(ol.flatten())
    bgid = 0
    img = Image.new("RGB", (w, h), (255, 255, 255))
    drw = ImageDraw.Draw(img)
    clr = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    try:
        fnt = ImageFont.truetype("arial.ttf", fz)
    except IOError:
        fnt = ImageFont.load_default()
    for i in range(0, w, pad):
        for j in range(0, h, pad):
            oid = ol[i][j]
            if oid != bgid:
                drw.text((i, j), str(oid - 1), fill=clr[(oid) % len(clr)], font=fnt)
    img.save(op)

def mk_overlay(objs, w, h):
    ol = np.zeros((w, h), dtype=int)
    for oid, px in objs.items():
        for i, j in px:
            ol[i, j] = oid
    return ol

fp = "input/image1.png" #replace with input image
op = "output/overlay_with_numbers.png" #replace with the directory location and file name where u want to add it
th = 170
objs, oclr, w, h = seg_obj(fp, t=th)
ol = mk_overlay(objs, w, h)
save_overlay(ol, w, h, op, pad=20, fz=10)
print(f"Segmentation complete. Overlay saved to {op}.")
