def rewrite(key, value):
    try:
        with open("/home/pi/jufö/.env","r") as f:
            with open("/home/pi/jufö/.env","w") as w:
                for line in f.readlines():
                    if key in line.split("=")[0]:
                        w.write("{}={}\n".format(line.split("=")[0], value))
                    else:
                        w.write(line)
    except Exception as e:
        print(e)
