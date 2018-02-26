import logging
import json
from flask import request
from flask import make_response
from pca9685_driver import Device
from querystring_parser import parser

from .app import app, devices
from .http import HttpException, create_response

logger = logging.getLogger(__name__)

def check_device(device):
    if device not in devices:
        raise HttpException("Unknown device '%s'" % device, 404)

@app.route('/devices/<device_name>/led/<int:led_number>', methods = ['GET'])
def get_led_value(device_name, led_number):
    check_device(device_name)
    value = devices[device_name].get_pwm(led_number)
    return create_response({'result': 'ok', 'value': value})

@app.route('/devices/<device_name>/led/<int:led_number>', methods = ['PUT'])
def set_led_value(device_name, led_number):
    check_device(device_name)
    value = int(request.form['value'])
    devices[device_name].set_pwm(led_number, value)
    return create_response({'result': 'ok'})

@app.route('/devices/<device_name>/led', methods = ['GET'])
def get_led_values(device_name):
    check_device(device_name)
    result = {}
    dev = devices[device_name]
    for led in range(0, Device.ranges['led_number'][1]+1):
        result[led] = dev.get_pwm(led)
	resp = make_response(json.dumps({'result': 'ok', 'values': result}), 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'PUT,GET, POST, DELETE, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'origin, x-requested-with, content-type'
    return resp

@app.route('/devices/<device_name>/led', methods = ['PUT'])
def set_led_values(device_name):
    check_device(device_name)
    dev = devices[device_name]
    args = parser.parse(request.get_data())
    for led, value in args['led'].items():
        dev.set_pwm(int(led), int(value))
    resp = make_response("{'result': 'ok'})", 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'PUT,GET, POST, DELETE, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'origin, x-requested-with, content-type'
    return resp
#    return create_response({'result': 'ok'})

@app.route('/devices/<device_name>/pwm-frequency', methods = ['GET'])
def get_pwm_frequency(device_name):
    check_device(device_name)
    return create_response({'result': 'ok', 'value': devices[device_name].get_pwm_frequency()})

@app.route('/devices/<device_name>/pwm-frequency', methods = ['PUT'])
def set_pwm_frequency(device_name):
    check_device(device_name)
    value = int(request.form['value'])
    devices[device_name].set_pwm_frequency(value)
    return create_response({'result': 'ok'})

@app.route('/devices/lamp/led', methods = ['OPTIONS'])
def handleCOSRRequest ():
#    resp = response("Foo bar baz")
    resp = make_response("", 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'PUT,GET, POST, DELETE, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'origin, x-requested-with, content-type'
    return resp
