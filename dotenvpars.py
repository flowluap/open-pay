def rewrite(key, value):
    with open(".env","r") as f:
        lines = f.readlines()

    with open(".env","w") as f:
        for line in lines:
            if key in line.split("=")[0]:
                f.write("{}={}\n".format(line.split("=")[0], value))
            else:
                f.write(line)
