def rewrite(key, value):
    try:
        with open(".env","r+") as f:
            for line in f.readlines():
                if key in line.split("=")[0]:
                    f.write("{}={}\n".format(line.split("=")[0], value))
                else:
                    f.write(line)
    except Exception as e:
        with open("log.txt","w") as f:
            f.write(e)
