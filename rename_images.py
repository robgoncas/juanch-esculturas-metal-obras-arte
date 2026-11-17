from datetime import datetime
from pathlib import Path
import re

folder = Path("assets/img")
pattern = re.compile(
    r"WhatsApp Image (\d{4}-\d{2}-\d{2}) at "
    r"(\d{1,2}\.\d{2}\.\d{2} [AP]M)"
    r"(?: \((\d+)\))?(\.[^.]+)$"
)

images = []
for path in folder.iterdir():
    match = pattern.fullmatch(path.name)
    if match:
        date, time, copy_number, extension = match.groups()
        timestamp = datetime.strptime(
            f"{date} {time}", "%Y-%m-%d %I.%M.%S %p"
        )
        images.append(
            (timestamp, int(copy_number or 0), path, extension.lower())
        )

images.sort(key=lambda item: (item[0], item[1]))

destinations = [
    folder / f"img{i}{extension}"
    for i, (_, _, _, extension) in enumerate(images, start=1)
]
if any(path.exists() for path in destinations):
    raise SystemExit("Cancelado: ya existe algún archivo imgN en assets/img.")

# Usar nombres temporales evita colisiones durante el cambio de nombre.
temporary_paths = []
for i, (_, _, source, _) in enumerate(images, start=1):
    temporary = folder / f".rename-temp-{i}"
    source.rename(temporary)
    temporary_paths.append(temporary)

for temporary, destination in zip(temporary_paths, destinations):
    temporary.rename(destination)

print(f"Renombradas {len(images)} imágenes.")