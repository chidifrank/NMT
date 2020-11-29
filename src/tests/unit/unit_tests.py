import unittest

from src.components.util.call_model import call_model


def replace_all(text, replace, replacement):
    while text.__contains__(replace):
        text = text.replace(replace, replacement)
    return text


class TranslationTests(unittest.TestCase):
    def test_if_model_exists(self):
        model = None

        try:
            model = open('/var/www/FlaskApp/FlaskApp/model/model_step_100000.pt')
            model.close()
        except FileNotFoundError:
            pass

        self.assertIsNotNone(model)

    def test_if_model_call_exists(self):
        model_call = None

        try:
            model_call = open('/var/www/FlaskApp/FlaskApp/model_call.bat')
            model_call.close()
        except FileNotFoundError:
            pass

        self.assertIsNotNone(model_call)

    def test_cases(self):
        english_cases = open(replace_all('\\var\\www\\FlaskApp\\FlaskApp\\tests\\unit\\cases\\english.txt', '\\', '/'))
        english_text = english_cases.readlines()
        english_cases.close()

        dutch_cases = open(replace_all('\\var\\www\\FlaskApp\\FlaskApp\\tests\\unit\\cases\\dutch.txt', '\\', '/'))
        dutch_text = dutch_cases.readlines()
        dutch_cases.close()

        for i in range(len(english_text)):
            test = open(replace_all('\\var\\www\\FlaskApp\\FlaskApp\\data\\speech\\test.txt', '\\', '/'), 'w')
            test.write(str(english_text[i]))
            test.close()

            call_model()

            translation = open(replace_all('\\var\\www\\FlaskApp\\FlaskApp\\data\\speech\\translation.txt', '\\', '/'))
            translation_text = translation.read()
            translation.close()

            translation_text = translation_text.strip()
            test_text = dutch_text[i].strip()

            self.assertIn(test_text, translation_text)


if __name__ == '__main__':
    unittest.main()
