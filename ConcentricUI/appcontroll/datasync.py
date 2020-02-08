import json
from queue import Queue
from threading import Thread
from time import time

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.utils import platform
from oscpy.server import OSCThreadServer


class SendReceive(Widget):
    selected_store = ObjectProperty()

    device_ip = StringProperty()
    other_ip = StringProperty()
    lan_sock = None
    replay_chunk_upload_queue = Queue()
    replay_chunk_download_queue = Queue()

    accept_next_chunk = False

    chunk_size = 1024 * 10
    chunks_total = NumericProperty()
    chunks_uploaded = NumericProperty()
    chunks_downloaded = NumericProperty()
    #  data ratio is unsent:sent
    chunks_ratio = NumericProperty()

    status_text = StringProperty()

    do_polling = None
    polling_thread = None

    # ip = '192.168.0.7' if platform is 'android' else '192.168.0.22'
    # server_ip = StringProperty()
    port = 8002

    successfully_downloaded = []

    # def get_ips_store(self):
    #     store_type = 'ips_store.pydict'
    #     store_path = path.join(App.get_running_app().user_data_dir, store_type)
    #     ips_store = DictStore(store_path)
    #     return ips_store
    #
    # def set_ips(self):
    #     self.ips_store = self.get_ips_store()
    #     self.ips_store['device_ip'] = self.device_ip
    #     self.ips_store['other_ip'] = self.other_ip

    def do_on_pre_enter(self, *args):
        # self.ips_store = self.get_ips_store()
        self.device_ip = '192.168.0.7' if platform is 'android' else '192.168.0.22'
        self.other_ip = '192.168.0.22' if platform is 'android' else '192.168.0.7'
        # try:
        #     self.device_ip = self.ips_store.get('device_ip')
        #     self.other_ip = self.ips_store.get('other_ip')
        # except:
        #     self.device_ip = '192.168.0.'
        #     self.other_ip = '192.168.0.'
        #  fixme actually this should initialise as a client with the ips, and send the server it's details(?)

        if not self.lan_sock:

            # # Importing socket library
            # import socket
            #
            # # Function to display hostname and
            # # IP address
            # def get_Host_name_IP():
            #     try:
            #         host_name = socket.gethostname()
            #         host_ip_info = socket.gethostbyname_ex(host_name)
            #         host_ip_list = host_ip_info[-1]
            #         host_ip = host_ip_list[-1]
            #         print("Hostname :  ", host_name)
            #         print("IP List : ", host_ip_list)
            #         print("IP : ", host_ip)
            #         return str(host_ip)
            #     except:
            #         print("Unable to get Hostname and IP")
            #
            #         # Driver code
            #
            # self.device_ip = get_Host_name_IP()  # Function call

            # if platform == 'android':
            #     print('from AndroidGetIP import getIP')
            #     from AndroidGetIP import getIP
            #     print('self.device_ip = getIP()')
            #     self.device_ip = getIP()
            #     print('...................................')
            # else:
            #     import socket
            #     self.device_ip = [l for l in (
            #     [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [
            #         [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
            #          [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][1][0]
            #     print('**************', self.device_ip)

            self.lan_sock = self.osc.listen(self.device_ip, self.port, default=True)

            #  server  #
            @self.osc.address(b'/receive_data_information')
            def receive_data_information(number_of_items, number_of_chunks):
                #  this is (intended) for the windows device to receive
                self.number_of_items_downloading = number_of_items
                self.chunks_total = number_of_chunks
                self.chunks_downloaded = 0
                self.successfully_downloaded = []
                self.status_text = 'Initialising download of {} item(s)'.format(number_of_items)
                self.last_data_received_time = time()

                while not self.replay_chunk_download_queue.empty():
                    self.replay_chunk_download_queue.get()

                self.polling_check_if_data_stopped = Clock.schedule_interval(self.check_if_data_stopped, 2)

            #  server  #
            @self.osc.address(b'/receive_replay_chunk')
            def receive_replay_chunk(chunk_index, chunk):
                #  this is (intended) for the windows device to receive
                print('D {} / {} -> {}'.format(self.chunks_downloaded, self.chunks_total, chunk))
                self.calculate_download_ratio()
                if chunk not in self.successfully_downloaded:
                    #  when there is an error sending a chunk i go back and send the previous chunk
                    #  this could lead to duplicates so i check to see if it's already added
                    self.successfully_downloaded.append(chunk)
                    self.replay_chunk_download_queue.put((chunk_index, chunk))
                    self.chunks_downloaded += 1
                else:
                    print('THIS CHUNK IS ALREADY DOWNLOADED')
                self.last_data_received_time = time()
                if self.chunks_downloaded < self.chunks_total:
                    print('................', self.chunks_downloaded, self.chunks_total)
                    try:
                        self.osc.answer(b'/next_chunk', [], safer=True)
                    except:
                        self.osc.send_message(b'/next_chunk', [], self.other_ip, 8002, self.lan_sock, safer=True)
                else:
                    self.reconstruct_replay_chunks()
                self.status_text = 'Downloading chunk {} out of {}'.format(self.chunks_downloaded, self.chunks_total)

            #  client  #
            @self.osc.address(b'/next_chunk')
            def next_chunk():
                chunk_index, chunk = self.replay_chunk_upload_queue.get()
                self.chunks_uploaded += 1
                print('U {} / {}'.format(chunk_index, self.chunks_total))
                self.calculate_upload_ratio()
                self.send_replay_chunk(chunk_index, chunk)

            #  client  #
            @self.osc.address(b'/receive_resume_from_chunk')
            def receive_resume_from_chunk(chunk_start):
                print('received instruction to resume from chunk', chunk_start)
                self.status_text = 'Resuming from chunk {} out of {}'.format(self.chunks_downloaded, self.chunks_total)
                self.add_to_upload_queue(chunk_start)

    def check_if_data_stopped(self, *args):
        if time() - self.last_data_received_time > 0.125:
            print('RESUMING FROM CHUNK', self.chunks_downloaded)
            self.resume_from_chunk(self.chunks_downloaded)

    def do_on_pre_leave(self, *args):
        # self.osc.stop()
        self.do_polling = None

    def __init__(self, **kwargs):
        super(SendReceive, self).__init__(**kwargs)
        self.osc = OSCThreadServer(encoding=None)
        self.polling_check_if_data_stopped = None

    def resume_from_chunk(self, chunk_start=None):
        if chunk_start is None:
            chunk_start = self.chunks_downloaded  # + 1#-1 # + 1
        self.status_text = 'Resuming from chunk {} out of {}'.format(self.chunks_downloaded, self.chunks_total)
        self.osc.send_message(b'/receive_resume_from_chunk', [chunk_start], self.other_ip, 8002, self.lan_sock)

    def send_replay_chunk(self, chunk_index, chunk):
        #  this is (intended) for the android device to send
        self.status_text = 'Uploading chunk {} out of {}'.format(self.chunks_downloaded, self.chunks_total)
        self.osc.send_message(b'/receive_replay_chunk', [chunk_index, chunk], self.other_ip, 8002, self.lan_sock,
                              safer=True)

    def send_replay_chunks(self):
        print('going to genrate replay chunks')

        app = App.get_running_app()

        if hasattr(app, 'selected_items') and app.selected_items:
            items = app.selected_items
            print('{} item(s) selected -> {}'.format(len(items), items))
            self.status_text = '{} item(s) selected -> {}'.format(len(items), items)
        else:
            items = dict(self.selected_store)
            print('No items selected. Sending all {} -> '.format(len(items), items))
            self.status_text = 'No items selected. Sending all {} -> '.format(len(items), items)

        if not items:
            self.status_text = 'No items to be sent'
            return

        item_json = json.dumps(items)
        self.item_bytes = item_json.encode()

        number_of_items = len(items)
        unrounded_number_of_chunks = len(self.item_bytes) / self.chunk_size
        self.chunks_total = round(unrounded_number_of_chunks + .5)

        while not self.replay_chunk_upload_queue.empty():
            self.replay_chunk_upload_queue.get()

        self.status_text = 'Initialising upload of {} item(s)'.format(number_of_items)
        self.status_text = 'Initialising upload of {} item(s)'.format(number_of_items)
        print('@@@@', type(self.other_ip), self.other_ip)
        self.osc.send_message(b'/receive_data_information', [number_of_items, self.chunks_total], self.other_ip, 8002,
                              self.lan_sock)
        print('{{{{{{{{{{{{{{{ self.chunks_total', self.chunks_total)

        self.chunks_uploaded = 0
        self.add_to_upload_queue_thread = Thread(target=self.add_to_upload_queue, args=[])
        self.add_to_upload_queue_thread.start()

    def add_to_upload_queue(self, chunk_index=0):
        if not hasattr(self, 'item_bytes'):
            return
        x = chunk_index * self.chunk_size
        first_chunk = True
        while True:
            chunk = self.item_bytes[x:x + self.chunk_size]
            print('adding chunk', chunk_index)
            if chunk:
                #  ie if it's the first chunk
                if first_chunk:
                    first_chunk = False
                    #  the first time you dont need to put it in a queue. just send it.
                    #  this will keep off a send and receive parle between the two devices,
                    #  which will .get the subsequent chunks from the replay_chunk_upload_queue (see the else statement)
                    self.send_replay_chunk(chunk_index, chunk)
                else:
                    self.replay_chunk_upload_queue.put((chunk_index, chunk))
                    print(chunk)

                x += self.chunk_size
                chunk_index += 1

            else:
                break
        print(chunk)
        print('{{{{{{{{{{{{{{{ chunk_index', chunk_index)

    def reconstruct_replay_chunks(self):
        if self.polling_check_if_data_stopped:
            self.polling_check_if_data_stopped.cancel()
        self.polling_check_if_data_stopped = None

        # chunk_list = [None for x in range(self.chunks_total)]
        chunk_list = []
        while not self.replay_chunk_download_queue.empty():
            chunk_index, chunk = self.replay_chunk_download_queue.get()
            print('recon:', chunk_index, chunk)
            chunk_list.append(chunk.decode())
            # chunk_list[chunk_index] = chunk.decode()
            # chunk_list.append(chunk.decode())
            #  decode it here

        for i, x in enumerate(chunk_list):
            if x:
                print('>>>', i, x[-15:])
            else:
                print('>>>', i, x)
        item_json = ''.join(chunk_list)
        # print('reconstructed item_json', item_json)
        item_dict = json.loads(item_json)

        added = 0
        replaced = 0
        selected_store = self.selected_store
        for item_id, item_info in item_dict.items():
            item_id = float(item_id)
            if item_id in selected_store:
                replaced += 1
            else:
                added += 1
            print('item_id', type(item_id), item_id)
            selected_store[item_id] = item_info
        print('{} items added and {} items replaced'.format(added, replaced))

        selected_store.store_load()
        selected_store.store_sync()

    def calculate_upload_ratio(self, *args):
        if self.chunks_total:
            self.chunks_ratio = self.chunks_uploaded / self.chunks_total
        else:
            self.chunks_ratio = 0

    def calculate_download_ratio(self, *args):
        if self.chunks_total:
            self.chunks_ratio = self.chunks_downloaded / self.chunks_total
        else:
            self.chunks_ratio = 0
