import simpleam
import pygame as pg
import Settings
class AdManager():
    def __init__(self,app_id : str, ad_id : str):
        simpleam.simpleam_init(app_id)
        self.interstitial = simpleam.Interstitial(ad_id)
        self.timeout = False
        self.loaded = False
        
    def may_show(self):
        print(f'AdManager : may_show : timeout : {self.timeout}, ad loaded : {self.interstitial.is_loaded()}')
        if self.timeout and self.interstitial.is_loaded():
            print('AdManager : show')
            self.interstitial.show()
            self.timeout = False
            self.loaded = False
            
    def reload(self): 
        print('AdManager : reloading')
        if self.interstitial.is_loading():
            return
        if not self.loaded or not self.interstitial.is_loaded():
            print('AdManager : reset timer')
            self.interstitial.load_ad()
            self.loaded = True
            pg.time.set_timer(Settings.EVENT_AD, Settings.AD_TIME_MS)
        
    def on_timeout(self):
        print('AdManager : timeout')
        self.timeout = True
        