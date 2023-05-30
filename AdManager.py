import pygameadmob
import pygame as pg
import Settings
class AdManager():
    def __init__(self,app_id : str, ad_id : str):
        pygameadmob.pygameadmob_init(app_id)
        self.ad = pygameadmob.Interstitial(ad_id)
        # self.banner = pygameadmob.Banner()
        # self.banner.load_ad()
        # self.ad = pygameadmob.Rewarded()
        self.timeout = False
        self.loaded = False
        
    def may_show(self):
        print(f'AdManager : may_show : timeout : {self.timeout}, ad loaded : {self.ad.is_loaded()}')
        if self.timeout and self.ad.is_loaded():
            print('AdManager : show')
            self.ad.show()
            self.timeout = False
            self.loaded = False
            
    def reload(self): 
        print('AdManager : reloading')
        if self.ad.is_loading():
            return
        if not self.loaded or not self.ad.is_loaded():
            print('AdManager : reset timer')
            self.ad.load_ad()
            self.loaded = True
            pg.time.set_timer(Settings.EVENT_AD, Settings.AD_TIME_MS)
        
    def on_timeout(self):
        print('AdManager : timeout')
        self.timeout = True
        # self.banner.set_visibility(not self.banner.visible)
        
