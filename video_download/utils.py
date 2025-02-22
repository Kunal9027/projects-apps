# downloader/utils.py
import os
import browser_cookie3
import tempfile
from pathlib import Path

def get_youtube_cookies():
    """Get cookies from browser and save them to a temporary file"""
    try:
        # Try multiple browsers in order of popularity
        browsers = [
            (browser_cookie3.chrome, 'Chrome'),
            (browser_cookie3.firefox, 'Firefox'),
            (browser_cookie3.edge, 'Edge'),
            (browser_cookie3.safari, 'Safari'),
        ]
        
        cookie_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        
        for browser_func, browser_name in browsers:
            try:
                cj = browser_func(domain_name='.youtube.com')
                with open(cookie_file.name, 'w') as f:
                    for cookie in cj:
                        f.write(f'{cookie.domain}\tTRUE\t{cookie.path}\t'
                               f'{"TRUE" if cookie.secure else "FALSE"}\t{cookie.expires}\t'
                               f'{cookie.name}\t{cookie.value}\n')
                return cookie_file.name
            except:
                continue
                
        return None
    except Exception as e:
        print(f"Error getting cookies: {str(e)}")
        return None