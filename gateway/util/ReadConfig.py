class ReadConfig(object):

    def __init__(self, config_file, path_file=None):
        import os
        import configparser

        try:

            parser = configparser.ConfigParser()
            try:
                path = os.path.dirname(os.path.dirname(__file__))
            except Exception as ex:
                print(ex)
                path = None

            if path_file is not None and path_file:
                parser.read("%s/%s" % (path_file, config_file))
            else:
                parser.read("%s/config/%s" % (path, config_file))
            self.config = parser

        except Exception as ex:
            import traceback
            import sys

            ei = sys.exc_info()
            traceback.print_exception(ei[0], ei[1], ei[2], None, sys.stderr)
            del ei

            print("Exception: %s" % ex)

    def readConfig(self, section, key=None):
        try:
            if key is None:
                exists = self.config.has_section(section)

                if exists:
                    return self.config.items(section)
                else:
                    print("No exists: %s" % exists)
            else:
                exists = self.config.has_option(section, key)

                if exists:
                    return self.config.get(section, key)
                else:
                    print("No exists: %s" % exists)

        except Exception as ex:
            import traceback
            import sys

            ei = sys.exc_info()
            traceback.print_exception(ei[0], ei[1], ei[2], None, sys.stderr)
            del ei

            print("Exception: %s" % ex)
