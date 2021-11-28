import os

import hikari
import lightbulb


class Bot(lightbulb.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hikari = hikari.Hikari(self.config)