import sys, urllib.request
from PIL import Image
B = "https://lagalerieimmobiliere.com/wp-content/uploads/"
U = {"01":"2025/10/17278165891_VM345_23_original.jpg",
"02":"2026/07/17219260191_VM345_8_original.jpg",
"04":"2026/07/17219260311_VM345_10_original.jpg",
"06":"2026/07/17219260541_VM345_13_original.jpg",
"07":"2026/07/17219260621_VM345_14_original.jpg",
"08":"2026/07/17219260751_VM345_16_original.jpg",
"09":"2026/07/17219260951_VM345_18_original.jpg",
"10":"2026/07/17219261071_VM345_19_original.jpg",
"11":"2026/07/17704722541_VM383_1_original.jpg",
"12":"2026/07/17704722551_VM383_2_original.jpg",
"13":"2026/07/17704722571_VM383_4_original.jpg",
"15":"2026/07/17704722611_VM383_7_original.jpg",
"17":"2026/07/17704722631_VM383_9_original.jpg",
"18":"2026/07/17704722661_VM383_11_original.jpg",
"20":"2026/07/17704722951_VM383_40_original.jpg",
"24":"2026/07/17798895811_VA2709_11_original.jpg",
"27":"2026/07/17811232911_VA2709_19_original.jpg",
"28":"2026/07/17811234651_VA2709_20_original.jpg",
"30":"2026/07/17811242321_VA2709_22_original.jpg"}
for k in sys.argv[1:]:
    r = urllib.request.Request(B + U[k], headers={"User-Agent": "Mozilla/5.0"})
    open("s.jpg", "wb").write(urllib.request.urlopen(r, timeout=30).read())
    p = Image.open("s.jpg").convert("RGB")
    W, H = p.size
    cw = int(H * 9 / 16)
    p.crop(((W - cw) // 2, 0, (W - cw) // 2 + cw, H)).resize((864, 1536), Image.LANCZOS).save(k + ".jpg", quality=92)
    print("ok", k, p.size)
