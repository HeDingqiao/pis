from queue import queue
from threading import Thread,Lock
import urllib.parse
import socket
import re
import time

seen_urls=set(['/'])
lock=Lock()