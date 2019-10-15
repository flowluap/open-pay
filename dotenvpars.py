def rewrite(key, value):
    try:
        with open("/home/pi/jufö/.env","r+") as f:
            for line in f.readlines():
                if key in line.split("=")[0]:
                    f.write("{}={}\n".format(line.split("=")[0], value))
                else:
                    f.write(line)
    except Exception as e:
        print(e)
