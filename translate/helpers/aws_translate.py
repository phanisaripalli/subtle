import io
import re
import time

import boto3


class AWSTranslate:
    def __init__(self, auth, from_lang, to_lang, content, bulk):
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.content = content
        self.bulk = bulk

        self.__set_auth(auth)

    def __set_auth(self, auth):
        self.aws_trans = boto3.client(service_name='translate',
                                      use_ssl=True,
                                      aws_access_key_id=auth['aws_access_key_id'],
                                      aws_secret_access_key=auth['aws_secret_access_key']
                                      )

    def __get_from_aws(self, text):
        try:
            result = self.aws_trans.translate_text(Text=text,
                                                   SourceLanguageCode=self.from_lang,
                                                   TargetLanguageCode=self.to_lang
                                                   )

            return result.get('TranslatedText')
        except Exception as e:
            print(e)
            print('Error for source text : {}'.format(text))
            raise

    def __get_translation_dialogue(self):
        t0 = time.time()

        translated = ""
        to_trans = ''

        buf = io.StringIO(self.content)

        with buf as fi:
            for line in fi:
                line = line.replace('\n', '')
                line = line.replace('\r', '')

                number_condition = line.isdigit()

                pattern_time = r"(?P<h1>\d+):(?P<m1>\d+):(?P<s1>\d+),(?P<ms1>\d+)\W*-->\W*(?P<h2>\d+):(?P<m2>\d+):(?P<s2>\d+),(?P<ms2>\d+)$"
                time_match = re.match(pattern_time, line)

                if number_condition or time_match:
                    # write as it is
                    translated += line + '\r\n'
                    pass
                else:
                    if len(line) > 0:
                        to_trans += line
                    else:
                        if len(to_trans) > 0:
                            trans_text = self.__get_from_aws(text=to_trans)
                            translated += trans_text + '\r\n'
                            to_trans = ''

                        translated += '\r\n'

        if len(to_trans) > 0:
            trans_text = self.__get_from_aws(text=to_trans)
            translated += trans_text + '\r\n'

        t1 = time.time()

        print('Took {}'.format(t1 - t0))

        return translated

    def __get_translation_bulk(self):
        t0 = time.time()

        buf = io.StringIO(self.content)

        translated = ''

        with buf as fi:
            cnt = 0
            batch = ''

            for line in fi:
                cnt += 1
                if len(line) != 0:
                    batch += line

                if (cnt % 100) == 0:
                    if len(batch) == 0:
                        continue

                    trans_batch = self.__get_from_aws(text=batch)
                    translated = translated + trans_batch

                    batch = ''

            if len(batch) > 0:
                trans_batch = self.__get_from_aws(text=batch)
                translated = translated + trans_batch

        t1 = time.time()

        print('Took {}'.format(t1 - t0))

        return translated

    def get_translation(self):
        try:
            if self.bulk:
                return self.__get_translation_bulk()
            else:
                return self.__get_translation_dialogue()
        except Exception as e:
            print('exception {}'.format(e))
