from genie.abstract import lookup

# from genie import abstract
# abstract.declare_token(one='simple')

class Ospf(object):

    # os = 'nxos'

    @lookup
    def abc(self):
        'abc'
        print('local')

    @lookup
    def bcd(self):
        'bcd'
        print('local')

    def __call__(self):
        print('class OSPF defined in %s' % type(self).__module__)
