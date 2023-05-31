import pygameadmob
import pygame as pg
import Settings
class AdManager():
    def __init__(self, ad_id : str):
        pygameadmob.pygameadmob_init()
        self.ad = pygameadmob.Interstitial(ad_id)
        # self.banner = pygameadmob.Banner(pygameadmob.TEST_BANNER_ID, "TOP")
        # self.banner.load_ad()
        # self.ad = pygameadmob.Rewarded()
        self.timeout = False
        self.loaded = False
        self.showed = True
        
    def may_show(self):
        print(f'AdManager : may_show : timeout : {self.timeout}, ad loaded : {self.ad.is_loaded()}')
        if self.timeout and self.ad.is_loaded():
            print('AdManager : show')
            self.ad.show()
            self.timeout = False
            self.loaded = False
            self.showed = True
            
    def reload(self): 
        print('AdManager : reloading')
        if self.ad.is_loading():
            return
        if not self.loaded or not self.ad.is_loaded():
            print('AdManager : reload ad')
            self.ad.load_ad()
            self.loaded = True
            if self.showed:
                print('AdManager : reset timer')
                self.showed = False
                pg.time.set_timer(Settings.EVENT_AD, Settings.AD_TIME_MS)
                self.timeout = False
        
    def on_timeout(self):
        print('AdManager : timeout')
        self.timeout = True
        # self.banner.set_visibility(not self.banner.get_visibility())
        
