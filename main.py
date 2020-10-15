import telegram
from telegram.ext import Updater, Dispatcher, CommandHandler
import numpy as np
import matplotlib.pyplot as plt
import os

TOKEN = os.getenv('TOKEN')

if __name__ =='__main__':
    print(TOKEN)