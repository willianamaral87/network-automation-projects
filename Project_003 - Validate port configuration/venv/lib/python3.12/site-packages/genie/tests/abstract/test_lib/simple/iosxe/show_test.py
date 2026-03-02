from genie.metaparser import MetaParser

class TestParser(MetaParser):
    cli_command = 'test command'
    def cli(self, output=None):
        return {'test': 'command'}