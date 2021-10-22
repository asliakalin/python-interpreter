from os import error
from flask import Flask, jsonify, request
from flask import Response
from flask_cors import CORS
import sys
from io import StringIO
import contextlib
import traceback

class InterpreterError(Exception): pass

app = Flask(__name__)
cors = CORS(app, resources={r"/tester": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


def execute_code(code, inputs, solutions):
    res = ""
    cons = ""
    print_output = ""
    res_list = []
    te = 1
    correct, wrong, tot = 0, 0, len(solutions)
    for index in range(len(inputs)):
        i = inputs[index]
        sol = solutions[index]
        if te != 1: res += "\n"
        res += "------------------ TEST #" + str(te) + ": input = " + str(i) + " --------------------"
        print_output = ""
        try:
            codeObejct = compile("input = " + str(i) + "\n" + code, 'sumstring', 'exec')
            loc = {}
            exec(codeObejct, globals(), loc)
            return_workaround = loc['output']
            to_print = loc['to_print']
            for printer in to_print:
                print_output += "> "+str(printer) + "\n"
            res +=  "\nExpected output to be: " + str(sol) + ".\nYour code returned: " + str(return_workaround)
            failed = str(sol) != str(return_workaround)
            if failed:
                if index != (len(inputs)-1):
                    cons += "Failed Test #" + str(te) + "\n"
                else:
                    cons += "Failed Test #" + str(te)
            res += "\nTEST FAILED.\n\n" if failed else "\nTEST PASSED.\n\n"
            res += "Print Output:\n" + print_output
            wrong += 1 if failed else 0
            correct += 1 if not failed else 0
            res_list.append(return_workaround)
            res = res.replace("to_print.append", "print")




        except SyntaxError as err:
            error_class = err.__class__.__name__
            line_number = err.lineno
            detail = err.args[0]
            if str("'return' outside function") in str(detail):
                res += "\nERROR: Extra 'return' statement on line %s.\n>>> The function is given with a 'return output' statement on the last line." % str(line_number-2)
            else:
                res += "\nERROR: %s on line %d.\n>>> %s" % (error_class, line_number-2, detail)
            break
        except Exception as err:
            error_class = err.__class__.__name__
            detail = err.args[0]
            cl, exc, tb = sys.exc_info()
            line_number = traceback.extract_tb(tb)[-1][1]
            if str("'return' outside function") in str(detail):
                res += "\nERROR: Unexpected 'return' statement.\n>>> You do not need to include a return statement as'return outputs' is given as the last line of code."
            elif (str(detail) == "output"): #KeyError
                res += "\nERROR: %s\nMake sure you are asigning a value to `output`." % (str(error_class))
            else:
                res = res + "\nERROR: %s on line %d.\n>>> %s ." % (str(error_class), line_number-2,detail)


            break

        te += 1

    return (res, res_list, cons, correct, wrong, tot)

#Testing Route
@app.route('/', methods=['GET'])
def getDefault():
    return jsonify({'response': 'Hello to my users api!'})

#Testing Route
@app.route('/tester', methods=['POST'])
def tester():
    inputs = request.json['inputs']
    solutions = request.json['solutions']
    code = request.json['code']

    """
    Example
    {
    "inputs": [0,1,2,3],
    "solutions": [0,2,4,6],
    "code": "output = input*2"
    }
    """

    var = execute_code("to_print = []\n" + code.replace("print", "to_print.append"), inputs, solutions)

    equal = True
    if var[1] != solutions:
        equal = False
    return jsonify({'prints': var[2], 'console':var[0], 'result':equal, 'solution': var[1], 'correct':var[3], 'wrong':var[4], 'tot':var[5] })


if __name__ == '__main__':
    app.run(debug=True, port=8000)