from kivy.app import App
from kivy.properties import AliasProperty

from ConcentricUI.appcontroll.storage import Storage


def get_last_saved_location(self):

    # current_journey
    # saved_journeys


    for store_name in ('current_journey', 'saved_journeys'):

        store = App.get_running_app().storage.get_store_reference(store_name)

        store.store_load()

        for journey_id, journey in dict(store).items():
            try:
                # location = journey['phone sensor readings']['gps location'][-1]
                # if location:
                #     return location
                return journey['phone sensor readings']['gps location'][-1]
            except:
                print('No gps location found in'.format(store_name, journey_id))
    return None


LastSavedLocation = AliasProperty(get_last_saved_location, None, rebind=True)


def get_best_location(self):

    if self.gps_location:
        location = self.gps_location
    elif self.rough_location:
        location = self.rough_location
    else:
        print('nonononononono')
        location = get_last_saved_location(App.get_running_app())

    return location


BestLocation = AliasProperty(get_best_location, None, rebind=True,
                             bind=['gps_location', 'rough_location', 'last_saved_location'])
