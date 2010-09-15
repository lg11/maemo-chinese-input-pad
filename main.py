import pinyin
import sys

if __name__ == "__main__":
    b = pinyin.Buffer()
    while(1):
        line = sys.stdin.readline()[:-1]
        #print line
        b.reset()
        for ch in line:
            b.append( ch )
        rs = b.search()
        for r in rs:
            s = r[0] + " " + r[1]
            print s
