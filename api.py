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
    res_list = []
    te = 1
    for index in range(len(inputs)):
        i = inputs[index]
        sol = solutions[index]
        if te != 1: res += "\n"
        res += "$> ---------------- TEST #" + str(te) + " ------------------\nTest Input = " + str(i) + "\nExpected Output: " + str(sol) + "\n"
        aux = {}
        try:
            codeObejct = compile("input = " + str(i) + "\n" + code, 'sumstring', 'exec')
            loc = {}
            exec(codeObejct, globals(), loc)
            return_workaround = loc['output']
            to_print = loc['to_print']
            for printer in to_print:
                cons += str(printer)
            cons += + " \n-----------------------------------\n"
            res +=  "Your Output: " + str(return_workaround)
            res += "\nTEST FAILED." if str(sol) != str(return_workaround) else "\nTEST PASSED."

            res_list.append(return_workaround)

        except SyntaxError as err:
            error_class = err.__class__.__name__
            line_number = err.lineno
            detail = err.args[0]

            res += "\nERROR: %s on line %d.\n>>> %s" % (error_class, line_number-2, detail) + "\nTEST FAILED."
            break
        except Exception as err:
            error_class = err.__class__.__name__
            detail = err.args[0]
            cl, exc, tb = sys.exc_info()
            line_number = traceback.extract_tb(tb)[-1][1]
            if str("'return' outside function") in str(detail):
                res += "\nERROR: Unexpected 'return' statement.\n>>> You do not need to include a return statement as'return outputs' is given as the last line of code."
            elif (str(detail) == "output"):
                res += "\nERROR: Internal-API Error.\nPlease contact the organizers if repeated."
            else:
                res = res + "\nERROR: %s on line %d.\n>>> %s ." % (str(error_class), line_number-2,detail) + "\nTEST FAILED."
            
                
            break

        te += 1

    return (res, res_list, cons)

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
    return jsonify({'prints': var[2], 'console':var[0], 'result':equal, 'solution': var[1], })


if __name__ == '__main__':
    app.run(debug=True, port=8000)