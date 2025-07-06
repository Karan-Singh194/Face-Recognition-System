import tkinter as tk

def draw_gradient(canvas, width, height, color1, color2):
    r1, g1, b1 = canvas.winfo_rgb(color1)
    r2, g2, b2 = canvas.winfo_rgb(color2)

    r_ratio = (r2 - r1) / height
    g_ratio = (g2 - g1) / height
    b_ratio = (b2 - b1) / height

    for i in range(height):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = f'#{nr//256:02x}{ng//256:02x}{nb//256:02x}'
        canvas.create_line(0, i, width, i, fill=color)

root = tk.Tk()
width, height = 1300, 700
canvas = tk.Canvas(root, width=width, height=height)
canvas.pack()

draw_gradient(canvas, width, height, "#338BFF", "#0024C7")  # From orange to red

root.mainloop()
