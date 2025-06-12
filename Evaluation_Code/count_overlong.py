import os

def line_statics(infile):
    i = 0
    cc = 0
    max = 10000
    with open(infile, 'r', encoding='utf-8') as fin:
        for line in fin:
            ll = len(line)
            if ll > max:
                cc += 1
                print(f"i={i}, length={ll}")
            i += 1
    print(f"lenght > {max}, count={cc}")

if __name__ == '__main__':
    from sys import argv

    if len(argv) > 1:
        line_statics(argv[2])
    else:
        print("no file to statics\n")
