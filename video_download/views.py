from django.shortcuts import render
from django.http import JsonResponse
import yt_dlp
import instaloader
import re
from urllib.parse import urlparse
from django.views.decorators.http import require_http_methods

def get_platform(url):
    """Determine the platform from the URL"""
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    
    platforms = {
        ('youtube.com', 'youtu.be'): 'youtube',
        ('instagram.com',): 'instagram',
        ('twitter.com', 'x.com'): 'twitter',
        ('facebook.com', 'fb.com'): 'facebook',
        ('reddit.com',): 'reddit',
        ('vimeo.com',): 'vimeo',
        ('dailymotion.com',): 'dailymotion',
        ('tiktok.com',): 'tiktok',
    }
    
    for domains, platform in platforms.items():
        if any(d in domain for d in domains):
            return platform
    return None

def extract_video_url(url, platform):
    """Extract video URL using yt-dlp with platform-specific options"""
    ydl_opts = {
        'format': 'best',  # Get best quality
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    # Platform-specific options
    if platform == 'facebook':
        ydl_opts.update({
            'facebook_dl_timeout': 30,  # Timeout for Facebook downloads
        })
    elif platform == 'reddit':
        ydl_opts.update({
            'extract_flat': True,  # Better for Reddit galleries
        })
    elif platform == 'instagram':
        return get_instagram_link(url)
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'url' in info:
                return {'success': True, 'url': info['url'], 'title': info.get('title', '')}
            elif 'entries' in info and info['entries']:
                # Handle playlists or galleries
                first_video = info['entries'][0]
                return {'success': True, 'url': first_video['url'], 'title': first_video.get('title', '')}
            else:
                return {'success': False, 'error': 'No video URL found'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_instagram_link(url):
    """Special handling for Instagram"""
    try:
        L = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(L.context, url.split("/p/")[1].split("/")[0])
        if post.is_video:
            return {'success': True, 'url': post.video_url, 'title': f'Instagram video - {post.date}'}
        return {'success': False, 'error': 'Not a video post'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@require_http_methods(["GET", "POST"])
def download_view(request):
    if request.method == 'POST':
        url = request.POST.get('url', '').strip()
        
        if not url:
            return JsonResponse({'success': False, 'error': 'No URL provided'})
        
        platform = get_platform(url)
        if not platform:
            return JsonResponse({'success': False, 'error': 'Unsupported platform'})
        
        result = extract_video_url(url, platform)
        if result['success']:
            result['platform'] = platform
        return JsonResponse(result)
    
    return render(request, 'downloder/download.html')