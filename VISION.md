# 1. Pegar el contenido en el portapapeles y escribir el archivo
pbpaste > VISION.md

# 2. Verificar que se guardó correctamente
wc -l VISION.md
head -5 VISION.md
tail -5 VISION.md
grep -c "NCh\|ISO\|D.S.\|Ley" VISION.md