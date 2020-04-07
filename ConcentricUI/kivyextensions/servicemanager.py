import os
from functools import partial
from json import dumps

from kivy.app import App
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass
else:
    from ConcentricUI.utilities.killablethread import KillableThread


class ServiceManager(object):
    running_services = {}

    def __init__(self, package_name, package_domain):
        self.package_name = package_name
        self.package_domain = package_domain

        self.environment_json = None

        if platform == 'android':
            self.mActivity = autoclass('org.kivy.android.PythonActivity').mActivity

    def load_and_start_service(self, service_name, osc_port):
        service = self.load_service(service_name, osc_port)
        self.start_service(service)

        return service

    def load_service(self, service_name, osc_port, *args):


        #  first set the environment variables (why not)
        app_dir = App.get_running_app().directory
        #config_dir = os.path.dirname(App.get_running_app().get_application_config())
        user_data_dir = App.get_running_app().user_data_dir
        main_port = App.get_running_app().port
        environment_json = dumps((app_dir, user_data_dir, main_port, osc_port))

        print('initiating start of service', type(service_name), service_name)
        if service_name not in self.running_services.keys():
            print('service {} not already running. continuing with service start'.format(service_name))
            service_formatted_name = '{}.{}.Service{}'.format(self.package_name, self.package_domain,
                                                              service_name.capitalize())
            if platform == 'android':
                service = autoclass(service_formatted_name)
            else:

                os.environ['PYTHON_SERVICE_ARGUMENT'] = environment_json

                services_path = os.path.join(App.get_running_app().directory, 'service')
                for file in os.listdir(services_path):
                    if file.endswith(".py"):
                        if file.lower().startswith(service_name.lower()):
                            service_path = os.path.join(services_path, file)
                            #  importing file by file name:
                            import importlib.util
                            spec = importlib.util.spec_from_file_location("service_file", service_path)
                            service_file = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(service_file)
                            break
                else:
                    #  if no file is found
                    raise Exception("File for service {} not found!".format(service_formatted_name))

                def service_thread(*args):
                    service_file.run_service()

                service = KillableThread(target=service_thread, args=[])

            #  this should allow me to call .stop_service() without navimActivity
            service.start_service = partial(self.start_service, service)
            service.stop_service = partial(self.stop_service, service)

            service.port = osc_port

            service.set = partial(App.get_running_app().osc.outbound_variable_setter, osc_port)
            service.get = partial(App.get_running_app().osc.outbound_variable_getter, osc_port)
            service.function = partial(App.get_running_app().osc.outbound_function_caller, osc_port)
            service.return_function = partial(App.get_running_app().osc.outbound_function_caller_with_return, osc_port)

            service.environment_json = environment_json

            self.running_services[service_name] = service

            return service

        else:
            print('service {} was not set up as the service is already referenced'.format(service_name))
            service = self.running_services[service_name]
            return service

    def start_service(self, service=None, service_name=None, *args):

        if not (service or service_name):
            raise Exception('You must specify either a service or a service name')
        elif service and service_name:
            if service is not service_name:
                raise Exception('You specified a service and a service name but they dont match')
        elif service_name:
            service = self.running_services[service_name]

        if platform == 'android':
            service.start(self.mActivity, service.environment_json)
        else:
            service.start()

    def stop_service(self, service=None, service_name=None, *args):

        if not (service or service_name):
            raise Exception('You must specify either a service or a service name')
        elif service and service_name:
            if service is not service_name:
                raise Exception('You specified a service and a service name but they dont match')
        elif service_name:
            service = self.running_services[service_name]

        service.stop()

        print("service {} stopped".format(service_name))

        if platform == 'win':
            del self.running_services[service_name]

    def stop_all_services(self):
        for service_name, service in self.running_services.items():
            service.stop_service()
            print("stopping service {} ...".format(service_name))
