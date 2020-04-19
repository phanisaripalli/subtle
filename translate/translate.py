import os

import yaml

from .helpers.aws_dynamo import AWSDynamo
from .helpers.aws_s3 import get_content, s3_write
from .helpers.aws_translate import AWSTranslate


class Translate:

    def __init__(self, media_id, from_lang, to_lang):
        self.media_id = media_id
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.config = None

        self.__set_config()
        self.__set_dynamo_handler()

    def __set_config(self):
        try:
            curr_dir = os.path.dirname(os.path.realpath(__file__))
            path = curr_dir + '/../config.yml'
            with open(path) as file:
                self.config = yaml.safe_load(file)
                print(self.config)
        except Exception as e:
            print(e)
            raise
            exit(-1)

    def __set_dynamo_handler(self):
        self.dh = AWSDynamo(auth=self.config['aws']['auth'], table_name=self.config['aws']['dynamodb'])

    def __get_translation(self, content):
        try:
            # print(content)
            aws_trans = AWSTranslate(auth=self.config['aws']['auth'],
                                     content=content,
                                     from_lang=self.from_lang,
                                     to_lang=self.to_lang,
                                     bulk=False
                                     )
            return aws_trans.get_translation()
        except Exception as e:
            print(e)
            raise

    def __read_source(self):
        filename = None
        if self.from_lang:
            filename = '{}.srt'.format(self.from_lang.upper())
        else:
            pass

        s3_key = self.media_id + '/' + filename
        content = get_content(self.config['aws']['auth'],
                              self.config['aws']['s3'],
                              s3_key
                              )

        return content

    def __save_translation(self, translated):
        filename = '{}.srt'.format(self.to_lang.upper())
        key = self.media_id + '/' + filename

        s3_write(self.config['aws']['auth'], self.config['aws']['s3'], key, translated)

    def __is_under_processing(self):
        key = {
            'id': '{}-{}-{}'.format(self.media_id, self.from_lang, self.to_lang)
        }

        item = self.dh.get(key=key)

        if item:
            return True
        else:
            False

    def __record_start(self):
        item = {
            'id': '{}-{}-{}'.format(self.media_id, self.from_lang, self.to_lang)
        }

        self.dh.put(item=item)

    def __record_flush(self):
        item = {
            'id': '{}-{}-{}'.format(self.media_id, self.from_lang, self.to_lang)
        }
        self.dh.delete(key=item)

    def __translate(self):
        pass

    def run(self):
        print('Translating {} from {} to {}'.format(self.media_id, self.from_lang, self.to_lang))

        under_processing = self.__is_under_processing()

        if under_processing:
            print('is under processing.')
            exit(0)
        else:
            self.__record_start()

        content = self.__read_source()
        translated = self.__get_translation(content=content)
        self.__save_translation(translated)

        self.__record_flush()
