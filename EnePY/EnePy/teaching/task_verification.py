import io
import sys
import collections


class TaskVerification:
    def __init__(self, value_list: list, optional_list_values: list, answer_list: list, text: str):
        self.value_list = value_list
        self.answer_list = answer_list
        self.optional_list_values = optional_list_values
        self.text = text
        self.code = self.creating_code()
        self.received_values = []

    def run(self):
        if self.code != SyntaxError:
            if self.optional_list_values:
                for i in self.optional_list_values:
                    olv = ''
                    for j in i:
                        olv += j + '\n'
                    self.code = self.creating_code(optional_text=olv)
                    if self.code != SyntaxError:
                        if self.value_list:
                            for j in self.value_list:
                                de = self.dynamic_execution(value_list=list(j))
                                if de[0]:
                                    self.received_values.append(de[1])
                                else:
                                    return False, de[1]
                        else:
                            de = self.dynamic_execution()
                            if de[0]:
                                self.received_values.append(de[1])
                            else:
                                return False, de[1]
            elif self.value_list:
                for i in self.value_list:
                    de = self.dynamic_execution(value_list=list(i))
                    if de[0]:
                        self.received_values.append(de[1])
                    else:
                        return False, de[1]
            else:
                de = self.dynamic_execution()
                if de[0]:
                    self.received_values.append(de[1])
                else:
                    return False, de[1]
        else:
            return False, self.code

        test = False

        for i in range(len(self.answer_list)):
            if collections.Counter(self.received_values[i]) == collections.Counter(self.answer_list[i]):
                test = True
            else:
                test = False
                break

        if test:
            return True, 'Ошибок нет'
        else:
            return False, 'Алгоритм был реалезован неверно'

    def creating_code(self, optional_text=None):

        try:
            if optional_text:
                return compile(self.text + '\n' + optional_text, "<string>", "exec")
            else:
                return compile(self.text, "<string>", "exec")
        except Exception as te:
            sys.stdout = sys.stderr
            return te

    def dynamic_execution(self, value_list=None):
        output_stream = io.StringIO()
        saved_out = sys.stdout
        saved_out_error = sys.stderr
        sys.stdout = output_stream

        def get_value():
            return str(value_list.pop(0))

        try:
            exec(self.code, {}, {'input': get_value})
            sys.stdout = saved_out
            output_stream.seek(0)

            return True, output_stream.read().strip().split('\n')
        except Exception as ex:
            sys.stdout = saved_out_error
            return False, ex
