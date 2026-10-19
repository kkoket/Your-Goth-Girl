import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

FILE_SALVATAGGIO = "salvataggio.json"

TRASPARENTE = "#010101"
W, H = 340, 730
ALTEZZA_PANNELLO = 275

nomi_outfit = ["images/goth1.png", "images/goth2.png", "images/goth3.png"]

calo = {"hunger": -1, "happiness": -2, "energy": -0.5}

temi = {
    "cutie": {
        "etichetta": "#E3E0D3", "bordo": "#BCC6A4", "testo": "black",
        "barra_piena": "#BCC6A4", "barra_vuota": "#D2CDBC", "barra_bordo": "#7E8C5A",
        "bottone": "#E3E0D3", "bottone_attivo": "#D2CDBC", "entry": "white",
    },
    "vampire": {
        "etichetta": "#2A1A2E", "bordo": "#9E2A4B", "testo": "#E8D9E6",
        "barra_piena": "#B23A5A", "barra_vuota": "#2A1A2E", "barra_bordo": "#6B2D5C",
        "bottone": "#6B2D5C", "bottone_attivo": "#9E2A4B", "entry": "#2A1A2E",
    },
    "zombie": {
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
        "posizione": [root.winfo_x(), root.winfo_y()],
        "in_primo_piano": in_primo_piano.get(),
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
        if notte and nome == "energy":
            quantita = quantita * 3
        modifica(nome, quantita)
    etichetta_umore.config(text=umore())
    salva()
    root.after(5000, tick)

def respira():
    global su
    sprite.place(y=45 if su else 47)
    su = not su
    root.after(600, respira)

def mostra_fase():
    global notte
    nome_fase, sfondo, testo = fasi[fase]
    pannello.config(bg=sfondo)
    etichetta_fase.config(text=f"{nome_fase} · {tema_attuale}")
    for lbl in testi_pannello:
        lbl.config(bg=sfondo, fg=testo)
    notte = (nome_fase == "Night")

def prossima_fase():
    global fase
    fase = (fase + 1) % len(fasi)
    mostra_fase()
    root.after(30000, prossima_fase)

def applica_tema():
    global fasi
    t = temi[tema_attuale]
    fasi = fasi_temi[tema_attuale]

    entry_name.config(bg=t["entry"], fg=t["testo"], insertbackground=t["testo"])

    for lbl in etichette_stat + [etichetta_umore]:
        lbl.config(bg=t["etichetta"], fg=t["testo"], highlightbackground=t["bordo"])

    for b in bottoni:
        b.config(bg=t["bottone"], fg=t["testo"], activebackground=t["bottone_attivo"])

    stile.configure("Goth.Horizontal.TProgressbar",
                    background=t["barra_piena"], troughcolor=t["barra_vuota"],
                    bordercolor=t["barra_bordo"],
                    lightcolor=t["barra_piena"], darkcolor=t["barra_piena"],
                    thickness=14)

    mostra_fase()

def cambia_tema():
    global tema_attuale
    posizione = nomi_temi.index(tema_attuale)
    tema_attuale = nomi_temi[(posizione + 1) % len(nomi_temi)]
    applica_tema()

def inizia_trascina(e):
    root.dx = e.x_root - root.winfo_x()
    root.dy = e.y_root - root.winfo_y()

def trascina(e):
    root.geometry(f"+{e.x_root - root.dx}+{e.y_root - root.dy}")

def apri_menu(e):
    menu.tk_popup(e.x_root, e.y_root)

def cambia_primo_piano():
    root.attributes("-topmost", in_primo_piano.get())

def chiudi():
    salva()
    root.destroy()

def togli_sfondo(img):
    img = img.convert("RGBA")
    larghezza, altezza = img.size
    for punto in [(0, 0), (larghezza - 1, 0), (0, altezza - 1), (larghezza - 1, altezza - 1)]:
        ImageDraw.floodfill(img, punto, (0, 0, 0, 0), thresh=40)
    return img

def carica_immagine(percorso, dimensioni):
    img = Image.open(percorso).resize(dimensioni, Image.NEAREST)
    return ImageTk.PhotoImage(togli_sfondo(img))

root = tk.Tk()
root.title("Your Goth Girl")
root.overrideredirect(True)
root.config(bg=TRASPARENTE, cursor="spider")
root.attributes("-transparentcolor", TRASPARENTE)

larghezza_schermo = root.winfo_screenwidth()
altezza_schermo = root.winfo_screenheight()
x, y = dati.get("posizione", [larghezza_schermo - W - 20, altezza_schermo - H - 60])
x = max(0, min(x, larghezza_schermo - W))
y = max(0, min(y, altezza_schermo - H))
root.geometry(f"{W}x{H}+{x}+{y}")

in_primo_piano = tk.BooleanVar(value=dati.get("in_primo_piano", True))
root.attributes("-topmost", in_primo_piano.get())

stile = ttk.Style()
stile.theme_use("clam")

etichetta_umore = tk.Label(root, font=("Arial", 12, "bold"), highlightthickness=2, padx=6)
etichetta_umore.place(x=W // 2, y=5, anchor="n")

foto_outfit = []
for percorso in nomi_outfit:
    foto_outfit.append(carica_immagine(percorso, (160, 400)))

indice = dati.get("indice", 0) % len(foto_outfit)
sprite = tk.Label(root, image=foto_outfit[indice], bg=TRASPARENTE, borderwidth=0)
sprite.place(x=W // 2, y=45, anchor="n")

foto_cat = carica_immagine("images/cat.png", (90, 90))
sprite_cat = tk.Label(root, image=foto_cat, bg=TRASPARENTE, borderwidth=0)
sprite_cat.place(x=95, y=H - ALTEZZA_PANNELLO - 10, anchor="se")

pannello = tk.Frame(root)
pannello.place(x=0, y=H - ALTEZZA_PANNELLO, width=W, height=ALTEZZA_PANNELLO)

etichetta_fase = tk.Label(pannello, font=("Arial", 13, "bold"))
etichetta_fase.place(x=W // 2, y=8, anchor="n")

azioni = {"hunger": ("Feed", nutri), "happiness": ("Reassure", rassicura), "energy": ("Gothify", goth)}

barre = {}
etichette_stat = []
bottoni = []
for i, nome in enumerate(stato):
    y = 55 + i * 42
    lbl = tk.Label(pannello, text=nome.capitalize(), font=("Arial", 9), highlightthickness=2, width=9)
    lbl.place(x=10, y=y, anchor="w")
    etichette_stat.append(lbl)

    barre[nome] = ttk.Progressbar(pannello, length=130, maximum=100, value=stato[nome],
                                  style="Goth.Horizontal.TProgressbar")
    barre[nome].place(x=100, y=y, anchor="w")

    testo_bottone, funzione = azioni[nome]
    b = tk.Button(pannello, text=testo_bottone, command=funzione, font=("Arial", 9), width=8)
    b.place(x=W - 10, y=y, anchor="e")
    bottoni.append(b)

etichetta_nome = tk.Label(pannello, text="Her name", font=("Arial", 9, "italic"))
etichetta_nome.place(x=W // 2, y=168, anchor="n")

entry_name = tk.Entry(pannello, font=("Arial", 12, "bold"), justify="center")
entry_name.place(x=W // 2, y=190, anchor="n", width=W - 40)
entry_name.insert(0, dati.get("nome", ""))

suggerimento = tk.Label(pannello, text="drag to move · right-click for menu", font=("Arial", 8, "italic"))
suggerimento.place(x=W // 2, y=ALTEZZA_PANNELLO - 8, anchor="s")

testi_pannello = [etichetta_fase, etichetta_nome, suggerimento]

menu = tk.Menu(root, tearoff=0)
menu.add_command(label="Change outfit", command=cambia_outfit)
menu.add_command(label="Change theme", command=cambia_tema)
menu.add_checkbutton(label="Always on top", variable=in_primo_piano, command=cambia_primo_piano)
menu.add_separator()
menu.add_command(label="Close", command=chiudi)

for w in (sprite, sprite_cat, pannello, etichetta_umore, etichetta_fase, etichetta_nome, suggerimento):
    w.bind("<Button-1>", inizia_trascina)
    w.bind("<B1-Motion>", trascina)
    w.bind("<Button-3>", apri_menu)

applica_tema()
respira()
root.after(30000, prossima_fase)
tick()

root.mainloop()
