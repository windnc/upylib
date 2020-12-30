from upylib.util.string import substr

class Node:
    def __init__(self):
        self.tag = ""
        self.attr = dict()
        self.child_list = list()

    def add_child(self, child):
        self.child_list.append(child)


class Parser:
    def __init__(self, text):
        self.text = text.strip()
        self.root = Node()


class HTMLParser(Parser):
    def __init__(self, text):
        super().__init__(text)

    def preproc(self):
        if self.text.startswith("<!doctype html>"):
            self.text = self.text[len("<!doctype html>"):].strip()

        self.text = self.text.replace(">", ">\n")

        while True:
            a, b, c = substr(self.text, "<meta", ">", contain_patt=False)
            if a and b and c:
                self.text = a + c
            else:
                break

        while True:
            a, b, c = substr(self.text, "<link", ">", contain_patt=False)
            if a and b and c:
                self.text = a + c
            else:
                break

        while True:
            a, b, c = substr(self.text, "<script>", "</script>", contain_patt=False)
            if a and b and c:
                self.text = a + c
            else:
                break

        while True:
            a, b, c = substr(self.text, "<script ", "</script>", contain_patt=False)
            if a and b and c:
                self.text = a + c
            else:
                break

        while True:
            a, b, c = substr(self.text, "<style>", "</style>", contain_patt=False)
            if a and b and c:
                self.text = a + c
            else:
                break

        while True:
            a, b, c = substr(self.text, "<!--", "-->", contain_patt=False)
            if a and b and c:
                self.text = a + c
            else:
                break



    def find_tag_open(self, i):
        while True:
            if self.text[i] == "<":
                return i+1
            i += 1
            if i >= len(self.text):
                return -1

    def find_tag_close(self, i):
        while True:
            if self.text[i] == ">":
                return i+1
            i += 1
            if i >= len(self.text):
                return -1

    def find_tag_name(self, i):
        start_i = i
        while True:
            # print("%d [%s" % (i, self.text[i]))
            if self.text[i] == " ":
                tag_name = self.text[start_i:i]
                return tag_name, i+1
            i += 1
            if i >= len(self.text):
                return "", -1

    def parse(self):
        num = 0
        while True:

            start_i = 0
            i = self.find_tag_open(start_i)
            if i < 0:
                break

            tag, i = self.find_tag_name(i)
            end_i = self.find_tag_close(i)

            h = self.text[start_i:end_i]

            num += 1
            print(num, h)

            self.text = self.text[end_i:].strip()

            if num > 40:
                break
            # print(start_i, end_i)
            # print(tag, i)
            #
            # n = Node()
            # n.tag = tag
            # self.root.add_child(n)


    def run(self):
        with open("out.html", "w") as fo:
            self.preproc()
            print(self.text, file=fo)


        # print(self.text)k
        # self.parse()
        #
        # print(self.text[0:200])
