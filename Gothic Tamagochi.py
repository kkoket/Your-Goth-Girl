import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import json
import os

FILE_SALVATAGGIO = "salvataggio.json"

def carica():
    if os.path.exists(FILE_SALVATAGGIO):
        with open(FILE_SALVATAGGIO) as f:
            return json.load(f)
    return {}

dati = carica()
root = tk.Tk()
root.title("Your Goth Girl")
root.state("zoomed")
root.configure(bg="#E3E0D3")
root.config(cursor="spider")  # <- tolto highlightcolor, sulla finestra non serve

banner = tk.Frame(root, bg="#B897C4", height=500)
banner.pack(fill="x")
banner.pack_propagate(False)
banner2 = tk.Frame(root, bg="#7D6489", height=500, width=250)  # <- altezza 500
banner2.place(x=0, y=0)                                         # <- posizione chiara
banner2.pack_propagate(False)

tk.Label(root, bg="#7D6489", text="Your GothGirl name is: ", font=("Arial", 16, "italic")).place(x=0, y=510, width=250)
entry_name = tk.Entry(root, width=25, font=("Arial", 16, "bold"))  # <- aggiunto root
entry_name.place(x=260, y=510)
entry_name.insert(0, dati.get("nome", ""))

stato = dati.get("stato", {"hunger": 80, "happiness": 80, "energy": 80})
barre = {}

stile = ttk.Style()
stile.theme_use("clam")
stile.configure(
    "Goth.Horizontal.TProgressbar",
    background="#BCC6A4",     #full
    troughcolor="#D2CDBC",    #empty
    bordercolor="#7E8C5A",    #border
    thickness=20,
)

for i, nome in enumerate(stato):
    y = 330 + i * 70
    tk.Label(root, text=nome.capitalize(), bg="#E3E0D3", highlightthickness=3, highlightbackground="#BCC6A4").place(x=1090, y=y, anchor="e")
    barre[nome] = ttk.Progressbar(root, length=200, maximum=100, value=stato[nome], style="Goth.Horizontal.TProgressbar")
    barre[nome].place(x=1100, y=y, anchor="w")

def modifica(nome, quantita):
    valore = stato[nome]
    stato[nome] = valore + quantita
    stato[nome] = max(0, min(100, stato[nome]))
    barre[nome].config(value=stato[nome])

def umore():  # <- soglie sistemate, ora compaiono tutti e tre i messaggi
    peggiore = min(stato.values())
    if peggiore > 60:
        return "Oh my goth!"
    elif peggiore > 25:
        return "So far so goth.."
    else:
        return "Under the bench the Goath dies.."

etichetta_umore = tk.Label(root, text="", bg="#E3E0D3", font=("Arial", 16, "bold"), highlightthickness=3, highlightbackground="#BCC6A4")
etichetta_umore.place(x=800, y=40, anchor="w")

calo = {"hunger": -1, "happiness": -2, "energy": -0.5}
def tick():
    for nome in stato:
        quantita = calo[nome]
        if notte and nome == "energy":  # <- di notte l'energia cala 3 volte più in fretta
            quantita = quantita * 3
        modifica(nome, quantita)
    root.after(5000, tick)
    etichetta_umore.config(text=umore())
    salva()  # <- salvataggio automatico

def goth():
    modifica("energy", 10)
tk.Button(root, text="Gothify", bg="#E3E0D3", command=goth).place(x=1310, y=470, anchor="w")
def rassicura():
    modifica("happiness", 15)
tk.Button(root, text="Reassure", bg="#E3E0D3", command=rassicura).place(x=1310, y=400, anchor="w")
def nutri():
    modifica("hunger", 20)
tk.Button(root, text="Feed", bg="#E3E0D3", command=nutri).place(x=1310, y=330, anchor="w")

def togli_sfondo(img):
    img = img.convert("RGBA")
    larghezza, altezza = img.size
    for punto in [(0, 0), (larghezza - 1, 0), (0, altezza - 1), (larghezza - 1, altezza - 1)]:
        ImageDraw.floodfill(img, punto, (0, 0, 0, 0), thresh=40)
    return img

nomi_outfit = ["images/goth1.png", "images/goth2.png", "images/goth3.png"]
foto_outfit = []

for percorso in nomi_outfit:
    img = Image.open(percorso).resize((200, 500), Image.NEAREST)
    img = togli_sfondo(img)
    foto_outfit.append(ImageTk.PhotoImage(img))

indice = dati.get("indice", 0) % len(foto_outfit)
sprite = tk.Label(root, image=foto_outfit[indice], bg="#B897C4")  # <- parte già con l'outfit salvato
sprite.place(x=600, y=-10)

def cambia_outfit():
    global indice
    indice = (indice + 1) % len(foto_outfit)
    sprite.config(image=foto_outfit[indice])

tk.Button(root, text="Change outfit", bg="#E3E0D3", command=cambia_outfit).place(x=850, y=330, anchor="w")

img_cat = Image.open("images/cat.png").resize((150, 150), Image.NEAREST)
img_cat = togli_sfondo(img_cat)
foto_cat = ImageTk.PhotoImage(img_cat)
sprite_cat = tk.Label(root, image=foto_cat, bg="#B897C4")
sprite_cat.place(x=600, y=500, anchor="se")

meow = tk.Label(root, text="meow ^^", bg="#B897C4", font=("Arial", 16, "italic"))  # <- place su riga separata
meow.place(x=380, y=400)

su = True
def respira():
    global su
    sprite.place(y=-10 if su else -8)
    su = not su
    root.after(600, respira)
respira()

# (nome, colore sfondo, colore testo)
fasi = [
    ("Morning", "#D9B8C9", "black"),
    ("Day",     "#B897C4", "black"),
    ("Evening", "#8E6FA0", "white"),
    ("Night",   "#4B2A5C", "white"),
]
fase = dati.get("fase", 0) % len(fasi)  # <- tolto "fase = fase =", e % per sicurezza
notte = False

etichetta_fase = tk.Label(root, text="", bg="#7D6489", fg="white", font=("Arial", 20, "bold"))
etichetta_fase.place(x=125, y=40, anchor="n")

def cambia_fase():
    global fase, notte
    nome_fase, sfondo, testo = fasi[fase]

    for widget in (banner, sprite, sprite_cat, meow):
        widget.config(bg=sfondo)
    meow.config(fg=testo)
    etichetta_fase.config(text=nome_fase)
    notte = (nome_fase == "Night")

    fase = (fase + 1) % len(fasi)
    root.after(30000, cambia_fase)

cambia_fase()

def salva():
    dati = {
        "stato": stato,
        "nome": entry_name.get(),
        "indice": indice,
        "fase": (fase - 1) % len(fasi),
    }
    with open(FILE_SALVATAGGIO, "w") as f:
        json.dump(dati, f)

def chiudi():
    salva()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", chiudi)

tick()
root.mainloop()