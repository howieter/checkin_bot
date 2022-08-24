import qrcode


def creat_qr_code():
    name = input("Введите ник: ")
    img = qrcode.make(name)
    img.save('/mnt/d/new_bab/21sc/Weeklython/Weeklython._Prototype-0/src/prototype/qrcode_test.png')
