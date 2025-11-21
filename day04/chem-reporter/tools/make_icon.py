from PIL import Image
Image.open("assets/icon.png").save(
    "assets/icon.ico",
    sizes=[(256,256),(128,128),(64,64),(32,32),(16,16)]
)
