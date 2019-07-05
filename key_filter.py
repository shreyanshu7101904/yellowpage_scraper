
import re
def key_filter(s):
    s1 = re.sub('[^A-Za-z0-9]+', '_',s.lower().strip())
    print(s1)





if __name__ == '__main__':
    key_filter("  viKKKay _____//###6^^^^$$___chsudiifjihvpjskjvjspovj%%%%%%%")