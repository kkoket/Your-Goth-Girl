import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import json
import os

#  settings

FILE_SALVATAGGIO = "salvataggio.json"

nomi_outfit = ["images/goth1.png", "images/goth2.png", "images/goth3.png"]

calo = {"hunger": -1, "happiness": -2, "energy": -0.5}

temi = {
    "cutie": {
        "sfondo": "#E3E0D3", "banner2": "#7D6489", "testo_colonna": "white",
        "etichetta": "#E3E0D3", "bordo": "#BCC6A4", "testo": "black",
        "barra_piena": "#BCC6A4", "barra_vuota": "#D2CDBC", "barra_bordo": "#7E8C5A",
        "bottone": "#E3E0D3", "bottone_attivo": "#D2CDBC", "entry": "white",
    },
    "vampire": {
        "sfondo": "#1A1220", "banner2": "#5A1E33", "testo_colonna": "#E8D9E6",
        "etichetta": "#2A1A2E", "bordo": "#9E2A4B", "testo": "#E8D9E6",
        "barra_piena": "#B23A5A", "barra_vuota": "#2A1A2E", "barra_bordo": "#6B2D5C",
        "bottone": "#6B2D5C", "bottone_attivo": "#9E2A4B", "entry": "#2A1A2E",
    },
    "zombie": {
        "sfondo": "#E3E0D3", "banner2": "#8FA67F", "testo_colonna": "#2F3A28",
        "etichetta": "#EEEBDD", "bordo": "#A9B58C", "testo": "#3F4A35",
        "barra_piena": "#9DBF8E", "barra_vuota": "#D2CDBC", "barra_bordo": "#7E8C5A",
        "bottone": "#D7E3C5", "bottone_attivo": "#B7C9A8", "entry": "#F7F5EC",
    },
}

fasi_temi = {
    "cutie": [
        ("Morning", "#D9B8C9", "black"),
        ("Day",     "#B897C4", "black"),
        ("Evening", "#8E6FA0", "white"),
        ("Night",   "#4B2A5C", "white"),
    ],
    "vampire": [
        ("Morning", "#5A3A5E", "#E8D9E6"),
        ("Day",     "#4A2A4E", "#E8D9E6"),
        ("Evening", "#3B1F3F", "#E8D9E6"),
        ("Night",   "#1F0F22", "#E8D9E6"),
    ],
    "zombie": [
        ("Morning", "#D6E2C8", "#3F4A35"),
        ("Day",     "#B7C9A8", "#3F4A35"),
        ("Evening", "#8FA67F", "#F7F5EC"),
        ("Night",   "#4E5E45", "#F7F5EC"),
    ],
}

nomi_temi = list(temi)

#  saving

def carica():
    if os.path.exists(FILE_SALVATAGGIO):
        with open(FILE_SALVATAGGIO) as f:
            return json.load(f)
    return {}

def salva():
    dati = {
        "stato": stato,
        "nome": entry_name.get(),
        "indice": indice,
        "fase": fase,
        "tema": tema_attuale,
    }
    with open(FILE_SALVATAGGIO, "w") as f:
        json.dump(dati, f)

dati = carica()

stato = dati.get("stato", {"hunger": 80, "happiness": 80, "energy": 80})

tema_attuale = dati.get("tema", "cutie")
if tema_attuale not in nomi_temi:
    tema_attuale = "cutie"

fasi = fasi_temi[tema_attuale]
fase = dati.get("fase", 0) % len(fasi)
notte = False
su = True

#  game functions

def modifica(nome, quantita):
    stato[nome] = max(0, min(100, stato[nome] + quantita))
    barre[nome].config(value=stato[nome])

def umore():
    peggiore = min(stato.values())
    if peggiore > 60:
        return "Oh my goth!"
    elif peggiore > 25:
        return "So far so goth.."
    else:
        return "Under the bench the Goath dies.."

def nutri():
    modifica("hunger", 20)

def rassicura():
    modifica("happiness", 15)

def goth():
    modifica("energy", 10)

def cambia_outfit():
    global indice
    indice = (indice + 1) % len(foto_outfit)
    sprite.config(image=foto_outfit[indice])

def tick():
    for nome in stato:
        quantita = calo[nome]
        if notte and nome == "energy":  # 3x down energy by night O-O
            quantita = quantita * 3
        modifica(nome, quantita)
    etichetta_umore.config(text=umore())
    salva()
    root.after(5000, tick)

#  animationsand day/night cycle

def respira():
    global su
    sprite.place(y=-10 if su else -8)
    su = not su
    root.after(600, respira)

def mostra_fase():
    global notte
    nome_fase, sfondo, testo = fasi[fase]
    for widget in (banner, sprite, sprite_cat, meow):
        widget.config(bg=sfondo)
    meow.config(fg=testo)
    etichetta_fase.config(text=nome_fase)
    notte = (nome_fase == "Night")

def prossima_fase():
    global fase
    fase = (fase + 1) % len(fasi)
    mostra_fase()
    root.after(30000, prossima_fase)

#  themes

def applica_tema():
    global fasi
    t = temi[tema_attuale]
    fasi = fasi_temi[tema_attuale]

    root.config(bg=t["sfondo"])
    banner2.config(bg=t["banner2"])
    etichetta_fase.config(bg=t["banner2"], fg=t["testo_colonna"])
    theme_label.config(text=tema_attuale, bg=t["banner2"], fg=t["testo_colonna"])
    etichetta_nome.config(bg=t["banner2"], fg=t["testo_colonna"])
    entry_name.config(bg=t["entry"], fg=t["testo"], insertbackground=t["testo"])

    for lbl in etichette_stat + [etichetta_umore]:
        lbl.config(bg=t["etichetta"], fg=t["testo"], highlightbackground=t["bordo"])

    for w in root.winfo_children():
        if isinstance(w, tk.Button):
            w.config(bg=t["bottone"], fg=t["testo"], activebackground=t["bottone_attivo"])

    stile.configure("Goth.Horizontal.TProgressbar",
                    background=t["barra_piena"], troughcolor=t["barra_vuota"],
                    bordercolor=t["barra_bordo"],
                    lightcolor=t["barra_piena"], darkcolor=t["barra_piena"],
                    thickness=20)

    mostra_fase()

def cambia_tema():
    global tema_attuale
    posizione = nomi_temi.index(tema_attuale)
    tema_attuale = nomi_temi[(posizione + 1) % len(nomi_temi)]
    applica_tema()

def chiudi():
    salva()
    root.destroy()

#  images

def togli_sfondo(img):
    img = img.convert("RGBA")
    larghezza, altezza = img.size
    for punto in [(0, 0), (larghezza - 1, 0), (0, altezza - 1), (larghezza - 1, altezza - 1)]:
        ImageDraw.floodfill(img, punto, (0, 0, 0, 0), thresh=40)
    return img

def carica_immagine(percorso, dimensioni):
    img = Image.open(percorso).resize(dimensioni, Image.NEAREST)
    return ImageTk.PhotoImage(togli_sfondo(img))

#  root sets

root = tk.Tk()
root.title("Your Goth Girl")
root.state("zoomed")
root.config(cursor="spider")

stile = ttk.Style()
stile.theme_use("clam")

banner = tk.Frame(root, height=500)
banner.pack(fill="x")
banner.pack_propagate(False)

banner2 = tk.Frame(root, height=500, width=250)
banner2.place(x=0, y=0)
banner2.pack_propagate(False)

# sx
etichetta_fase = tk.Label(root, font=("Arial", 20, "bold"))
etichetta_fase.place(x=125, y=40, anchor="n")

tk.Button(root, text="Change theme", command=cambia_tema).place(x=125, y=90, anchor="n")

# girl
foto_outfit = []
for percorso in nomi_outfit:
    foto_outfit.append(carica_immagine(percorso, (200, 500)))

indice = dati.get("indice", 0) % len(foto_outfit)
sprite = tk.Label(root, image=foto_outfit[indice])
sprite.place(x=600, y=-10)

tk.Button(root, text="Change outfit", command=cambia_outfit).place(x=850, y=330, anchor="w")

# cat
foto_cat = carica_immagine("images/cat.png", (150, 150))
sprite_cat = tk.Label(root, image=foto_cat)
sprite_cat.place(x=600, y=500, anchor="se")

meow = tk.Label(root, text="meow ^^", font=("Arial", 16, "italic"))
meow.place(x=380, y=400)

# humor
etichetta_umore = tk.Label(root, font=("Arial", 16, "bold"), highlightthickness=3)
etichetta_umore.place(x=800, y=40, anchor="w")

# bars
barre = {}
etichette_stat = []
for i, nome in enumerate(stato):
    y = 330 + i * 70
    lbl = tk.Label(root, text=nome.capitalize(), highlightthickness=3)
    lbl.place(x=1090, y=y, anchor="e")
    etichette_stat.append(lbl)
    barre[nome] = ttk.Progressbar(root, length=200, maximum=100, value=stato[nome],
                                  style="Goth.Horizontal.TProgressbar")
    barre[nome].place(x=1100, y=y, anchor="w")

tk.Button(root, text="Feed", command=nutri).place(x=1310, y=330, anchor="w")
tk.Button(root, text="Reassure", command=rassicura).place(x=1310, y=400, anchor="w")
tk.Button(root, text="Gothify", command=goth).place(x=1310, y=470, anchor="w")

# name
etichetta_nome = tk.Label(root, text="Your GothGirl name is: ", font=("Arial", 16, "italic"))
etichetta_nome.place(x=0, y=510, width=250)

entry_name = tk.Entry(root, width=25, font=("Arial", 16, "bold"))
entry_name.place(x=260, y=510)
entry_name.insert(0, dati.get("nome", ""))

# theme label
theme_label = tk.Label(root, text=tema_attuale, font=("Arial", 20, "italic"))
theme_label.place(x=125, y=140, anchor="n")

#  start

applica_tema()
respira()
root.after(30000, prossima_fase)
tick()

root.protocol("WM_DELETE_WINDOW", chiudi)
root.mainloop()
