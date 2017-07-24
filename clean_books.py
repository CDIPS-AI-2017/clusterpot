import re
import os


def clean(in_path, out_path):
    text = open(in_path, 'r').read()
    regex = r'\n*Page\s\|\s\d*\s*Harry Potter.*\s*'
    subst = ''
    result = re.sub(regex, subst, text)
    open(out_path, 'w').write(result)


def main():
    filelist = [f for f in os.listdir('./') if '_djvu.txt' in f]
    for f in filelist:
        out_path = f.replace('_djvu', '_clean').replace(' ', '')
        out_path = out_path.replace('-', '').replace("'", '')
        clean(in_path=f, out_path=out_path)


if __name__ == '__main__':
    main()