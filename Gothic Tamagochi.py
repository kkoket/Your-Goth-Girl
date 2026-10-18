import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw

root = tk.Tk()
root.title("Your Goth Girl")
root.state("zoomed")
root.configure(bg="#E3E0D3")

banner = tk.Frame(root, bg="#B897C4", height=500)
banner.pack(fill="x")
banner.pack_propagate(False)
banner2 = tk.Frame(root, bg="#7D6489", height=1000, width=250)
banner2.place(anchor="w")
banner2.pack_propagate(False)

tk.Label(root, bg="#7D6489",  text="Your GothGirl name is: ", font=("Arial", 16, "italic")).place(x=0, y=510, width=250)
entry_name = tk.Entry(width=25, font=("Arial", 16, "bold"))
entry_name.place(x=260, y=510)

stato = {"hunger": 80, "happiness": 80, "energy": 80}
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
    tk.Label(root, text=nome.capitalize(), bg="#E3E0D3", highlightthickness = 3, highlightbackground = "#BCC6A4").place(x=1090, y=y, anchor="e")
    barre[nome] = ttk.Progressbar(root, length=200, maximum=100, value=stato[nome], style = "Goth.Horizontal.TProgressbar")
    barre[nome].place(x=1100, y=y, anchor="w")

def modifica(nome, quantita):
    valore = stato[nome]
    stato[nome] = valore + quantita
    stato[nome] = max(0, min(100, stato[nome]))
    barre[nome].config(value=stato[nome])

def umore():
    peggiore = min(stato.values())
    if peggiore > 80:
        return "Oh my goth!"
    elif peggiore < 80:
        return "So far so goth.."
    else:
        return "Under the bench the Goath dies.."

etichetta_umore = tk.Label(root, text="", bg="#E3E0D3", font=("Arial", 16, "bold"), highlightthickness = 3, highlightbackground = "#BCC6A4")
etichetta_umore.place(x=800, y=40, anchor="w")

calo = {"hunger": -1, "happiness": -2, "energy": -0.5}
def tick():
    for nome in stato:
        modifica(nome, calo[nome])
    root.after(5000, tick)
    etichetta_umore.config(text=umore())

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

sprite = tk.Label(root, image=foto_outfit[0], bg="#B897C4")
sprite.place(x=600, y=-10)

indice = 0
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

tk.Label(root, text="meow ^^", bg="#B897C4", font=("Arial", 16, "italic")).place(x=380,y=400)

su = True
def respira():
    global su
    sprite.place(y=-10 if su else -8)
    su = not su
    root.after(600, respira)
respira()

tick()
root.mainloop()