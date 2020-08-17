import json
import urllib.request

log = print

class Check(object):
    def _init_(self, word):
        super(Check, self).__init__()
        self.word = word
        self.key = 'E442BF444FCC75B0CBD92D3D941B4FE0'
        log('sss')
        s = open()
        d = json.loads(s)

        a = d['symbols'][0]
        # log(a)
        log(d['word_name'], ':')

        two = []
        for i in range(3):
            b = a.get('parts')[i]
            log(b.get('part'))
            c = b.get('means')
            aone = []
            aone.append(b.get('part'))
            for I in range(len(c)):
                aone.append(c[I])
                log(c[I])
            log('\n')
            two.append(aone)
        return two




    def speak(self):
        log(self.word)


    def open(self):
        url = 'http://dict-co.iciba.com/api/dictionary.php?type=json&key={}&w={}'.format(self.key, self.word)
        s = urllib.request.urlopen(url).read()
        self.content = s.decode('utf-8')
        log(self.content)
        return self.content

    # def translate(self):
        # s = open()
        # d = json.loads(s)
        #
        # a = d['symbols'][0]
        # # log(a)
        # log(d['word_name'], ':')
        #
        # two = []
        # for i in range(3):
        #     b = a.get('parts')[i]
        #     log(b.get('part'))
        #     c = b.get('means')
        #     aone = []
        #     aone.append(b.get('part'))
        #     for I in range(len(c)):
        #         aone.append(c[I])
        #         log(c[I])
        #     log('\n')
        #     two.append(aone)
        # return two