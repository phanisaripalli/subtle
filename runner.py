import argparse

from translate.translate import Translate

SUPPORTED_LANGS = ['en', 'fr', 'nl', 'es']


def validate(media_id, from_lang, to_lang):
    is_valid_args = True

    if not media_id:
        print('provide media_id')
        is_valid_args = False

    if not to_lang:
        print('Provide to')
        is_valid_args = False
    else:
        if to_lang not in SUPPORTED_LANGS:
            print('to lang should be in {}'.format(SUPPORTED_LANGS))
            is_valid_args = False

    if from_lang and (from_lang not in SUPPORTED_LANGS):
        print('from lang should be in {}'.format(SUPPORTED_LANGS))
        is_valid_args = False

    return is_valid_args


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--media_id", help="id", type=str, dest='media_id')
    parser.add_argument("--from", help="from language", type=str, dest='from_lang')
    parser.add_argument("--to", help="to language", type=str, dest='to_lang')
    args = parser.parse_args()

    media_id = args.media_id
    from_lang = args.from_lang
    to_lang = args.to_lang

    is_valid = validate(media_id, from_lang, to_lang)

    print(media_id, from_lang, to_lang)

    if not is_valid:
        exit(0)

    trans = Translate(media_id=media_id, from_lang=from_lang, to_lang=to_lang)
    trans.run()
