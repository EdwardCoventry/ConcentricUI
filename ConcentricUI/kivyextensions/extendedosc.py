from kivy.app import App


import json
from functools import partial

from oscpy.server import OSCThreadServer

from ConcentricUI.utilities.runinthread import run_in_thread

from ConcentricUI.utilities.clearablequeue import ClearableQueue
from ConcentricUI.utilities.runinthread import run_in_thread

from time import sleep

class ExtendedOsc(OSCThreadServer):

    @run_in_thread
    def run_status_queue(self):
        while True:
            #  get from the queue
            kwargs = self.status_queue.get()
            #  set it in the main
            self.set('status', kwargs['status'])
            #  sleep for the minimum display time
            sleep(kwargs['min_display_time'])
            #  if there is nothing in the queue, and there is a max display time set, and the max is more than the min
            if self.status_queue.empty() and kwargs['max_display_time'] and kwargs['max_display_time'] > kwargs['min_display_time']:
                #  'sleep' for the time difference, but allow it to be interupted by a new queue item
                #  (this is the maximum wait time, after all)
                interupting = self.status_queue.get(timeout=kwargs['max_display_time'] - kwargs['min_display_time'])
                if interupting:
                    #  if there was an interrupt carefully put it back in the queue
                    #  to be gotten again on the immediate next loop
                    self.status_queue.put(interupting)
                else:
                    self.set('status', '')
                    #  if there was no interrupt then clear the queue

    def set_status(self, status, min_display_time=0.1, max_display_time=0.1, *args):
        self.status_queue.put({'status': status,
                               'min_display_time': min_display_time,
                               'max_display_time': max_display_time})

    def __init__(self, root, port, main_port=None, **kwargs):

        print('iiiinnnnnnnnnnnitttttttttttttttttttttt port={}, main_port={}'.format(port, main_port))

        self.root = root
        self.port = port
        if App.get_running_app():
            App.get_running_app().port = port
        self.main_port = main_port
        super(ExtendedOsc, self).__init__(encoding='utf8')
        self.sock = self.listen('localhost', self.port, default=True)

        self.set = partial(self.outbound_variable_setter, self.main_port)
        self.get = partial(self.outbound_variable_getter, self.main_port)
        self.function = partial(self.outbound_function_caller, self.main_port)
        self.return_function = partial(self.outbound_function_caller_with_return, self.main_port)

        print('initialised with port {}'.format(self.port))

        self.status_queue = ClearableQueue()
        self.run_status_queue()

        @self.address(b'/inbound_variable_setter')
        def inbound_variable_setter(value_json):
            variable_name, value = json.loads(value_json)

            variable_domain, variable_name = self.get_domain_and_variable_name(variable_name)

            setattr(variable_domain, variable_name, value)

            #  done

        @self.address(b'/inbound_variable_getter')
        def inbound_variable_getter(json_variable_name):

            variable_name, return_variable_name = json.loads(json_variable_name)

            value = self.get_variable(variable_name)

            return_json = json.dumps((return_variable_name, value))

            self.answer(address=b'/inbound_variable_setter',
                        values=[return_json])
            #  done

        @self.address(b'/inbound_function_caller')
        def inbound_function_caller(json_value):
            function_name, args, kwargs = json.loads(json_value)

            func = self.get_variable(function_name)

            if not func:
                raise Exception("Could not find function {}".format(function_name))

            # if len(args) == 1:
            #     func(args[0], **kwargs or {})
            # else:
            func(*args or [], **kwargs or {})
            #  done

        @self.address(b'/inbound_function_caller_with_return')
        def inbound_function_caller_with_return(json_value):
            function_name, result_domain, args, kwargs = json.loads(json_value)

            func = self.get_variable(function_name)
            return_result = func(*args or [], **kwargs or {})

            return_values_json = json.dumps((result_domain, return_result))

            print('answering with {}, {}'.format(result_domain, return_result))

            self.answer(address=b'/inbound_variable_setter',
                        values=[return_values_json])
            #  done

    """ These functions need a port to apply it to """

    @run_in_thread
    def outbound_variable_setter(self, port, variable_name, value, safer=False):
        value_json = json.dumps((variable_name, value))

        self.send_message(osc_address=b'/inbound_variable_setter',
                          values=[value_json],
                          ip_address='localhost',
                          port=port,
                          safer=safer)
    @run_in_thread
    def outbound_variable_getter(self, port, variable_name, return_variable_name=None, safer=False):

        if not return_variable_name:
            return_variable_name = variable_name

        variable_names_json = json.dumps((variable_name, return_variable_name))

        self.send_message(osc_address=b'/inbound_variable_getter',
                          values=[variable_names_json],
                          ip_address='localhost',
                          port=port,
                          safer=safer)
    @run_in_thread
    def outbound_function_caller(self, port, function_name, args=None, kwargs=None, safer=False):
        values_json = json.dumps((function_name, args, kwargs))

        self.send_message(osc_address=b'/inbound_function_caller',
                          values=[values_json],
                          ip_address='localhost',
                          port=port,
                          safer=safer)
    @run_in_thread
    def outbound_function_caller_with_return(self, port, function_name, result_domain, args=None, kwargs=None, safer=False):
        values_json = json.dumps((function_name, result_domain, args, kwargs))

        self.send_message(osc_address=b'/inbound_function_caller_with_return',
                          values=[values_json],
                          ip_address='localhost',
                          port=port,
                          safer=safer)

    def get_domain_and_variable_name(self, full_variable_name):
        """ This function takes something like the string
            'self.something_manager.something_else.you_get_the_idea.cool_variable'
            and returns the variable domain as an object (eg self.something_manager.something_else.you_get_the_idea)
            and the string name of the variable (eg. 'cool_variable').
            We do this so that it works with setattr """


        variable_domains = full_variable_name.split('.')
        variable_domains, variable_name = variable_domains[:-1], variable_domains[-1]
        #  for the domains we want all until the last part, and for the variable_name we want the last part

        variable_domain = self.root
        if not variable_name:
            raise Exception("Osc has not been assigned to a service yet")

        try:
            #  the starting domain
            for variable in variable_domains:
                variable_domain = getattr(variable_domain, variable)
        except AttributeError as e:
            raise Exception("Could not get domain {}. exception given: {}".format(full_variable_name, e))

        return variable_domain, variable_name

    def get_variable(self, variable_name):
        """ This calls get_domain_and_variable_name and the getattr to get the variable value, which it returns """

        variable_domain, variable_name = self.get_domain_and_variable_name(variable_name)
        try:
            return getattr(variable_domain, variable_name)
        except Exception as e:
            print('tried and failed to get variable {} on domain {}: exception: {}'.format(variable_name,
                                                                                           variable_domain,
                                                                                           e))