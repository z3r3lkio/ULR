import argparse
import base64
import json
import re
import threading
import tkinter as tk
import urllib.request
import webbrowser
from pathlib import Path
from tkinter import messagebox, ttk
from urllib.parse import urlsplit
from providers import decode_input, provider_name

def resolve(raw, notify):
    url = decode_input(raw)
    notify("Abriendo navegador para " + provider_name(url))
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(accept_downloads=True)
        found = {"url": None}
        def check():
            try:
                link = page.locator("#download-link")
                if link.count():
                    href = link.get_attribute("href")
                    if href and href.startswith(("https://", "http://")):
                        found["url"] = href
            except Exception:
                pass
        def download(d):
            found["url"] = d.url
        page.on("download", download)
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        notify("Completa la verificación y espera a Download. Cierra la ventana del navegador para cancelar.")
        for _ in range(600):
            if page.is_closed():
                break
            check()
            if found["url"]:
                break
            page.wait_for_timeout(1000)
        browser.close()
        if not found["url"]:
            raise RuntimeError("No se detectó enlace directo (tiempo agotado o navegador cerrado)")
        return found["url"]

def aria2_add(endpoint, uri, token=""):
    params = []
    if token:
        params.append("token:" + token)
    params.append([uri])
    data = json.dumps({"jsonrpc":"2.0","id":"ulr","method":"aria2.addUri","params":params}).encode()
    request = urllib.request.Request(endpoint, data=data, headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(request, timeout=15) as response:
        result = json.load(response)
    if "error" in result:
        raise RuntimeError(str(result["error"]))
    return result["result"]

def gui():
    root = tk.Tk()
    root.title("ULR · Universal Link Resolver")
    root.geometry("780x390")
    tk.Label(root,text="Universal Link Resolver",font=("Arial",20,"bold")).pack(pady=12)
    tk.Label(root,text="URL o Base64").pack(anchor="w",padx=20)
    source = tk.Entry(root)
    source.pack(fill="x",padx=20,pady=5)
    status = tk.StringVar(value="Introduce un enlace y pulsa Resolver")
    tk.Label(root,textvariable=status,wraplength=730).pack(pady=8)
    tk.Label(root,text="URL directa").pack(anchor="w",padx=20)
    output = tk.Entry(root)
    output.pack(fill="x",padx=20,pady=5)
    row = tk.Frame(root)
    row.pack(pady=10)
    def set_status(value):
        root.after(0,lambda:status.set(value))
    def work():
        try:
            value=resolve(source.get(),set_status)
            root.after(0,lambda:(output.delete(0,"end"),output.insert(0,value),status.set("Enlace detectado")))
        except Exception as exc:
            set_status("Error: "+str(exc))
    ttk.Button(row,text="Resolver",command=lambda:threading.Thread(target=work,daemon=True).start()).pack(side="left",padx=5)
    ttk.Button(row,text="Copiar",command=lambda:(root.clipboard_clear(),root.clipboard_append(output.get()),status.set("Copiado"))).pack(side="left",padx=5)
    ttk.Button(row,text="Abrir",command=lambda:webbrowser.open(output.get())).pack(side="left",padx=5)
    rpc = tk.Frame(root)
    rpc.pack(fill="x",padx=20)
    tk.Label(rpc,text="aria2 JSON-RPC").pack(side="left")
    endpoint=tk.Entry(rpc)
    endpoint.insert(0,"http://localhost:6800/jsonrpc")
    endpoint.pack(side="left",fill="x",expand=True,padx=8)
    def send():
        try:
            gid=aria2_add(endpoint.get(),output.get())
            messagebox.showinfo("aria2","Descarga añadida: "+str(gid))
        except Exception as exc:
            messagebox.showerror("aria2",str(exc))
    ttk.Button(rpc,text="Enviar a aria2",command=lambda:threading.Thread(target=send,daemon=True).start()).pack(side="left")
    root.mainloop()

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("url",nargs="?")
    args=parser.parse_args()
    if args.url:
        print(resolve(args.url,print))
    else:
        gui()
