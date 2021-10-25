#import local
from base import atOnceOauthSession
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
       sys.exit(1)
    atOnceOauthSession(sys.argv[1])