import base64
from urllib.parse import urlsplit

KNOWN = {"vik1ngfile.site":"VikingFile","vikingfile.com":"VikingFile","pixeldrain.com":"Pixeldrain","mediafire.com":"MediaFire","gofile.io":"GoFile","1fichier.com":"1fichier"}

def decode_input(value):
    value=value.strip()
    if not value.startswith(("https://","http://")):
        try:
            decoded=base64.urlsafe_b64decode(value+"="*((-len(value))%4)).decode("utf-8").strip()
            value=decoded
        except Exception as exc:
            raise ValueError("No es una URL HTTP(S) ni Base64 válido") from exc
    parsed=urlsplit(value)
    if parsed.scheme not in ("https","http") or not parsed.hostname:
        raise ValueError("Solo se admiten URLs HTTP(S)")
    return value

def provider_name(url):
    host=urlsplit(url).hostname or ""
    for domain,name in KNOWN.items():
        if host==domain or host.endswith("."+domain):
            return name
    return "Proveedor genérico"
