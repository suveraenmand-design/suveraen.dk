#!/usr/bin/env python3
"""Dependency-free checks for the static suveræn.dk website."""
from __future__ import annotations
import re, sys, urllib.error, urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]; EXCLUDED={'.git','_site','vendor'}
EXPECTED={'/','/om-bogen/','/laeseliste/','/ressourcer/'}; ERRORS=[]; WARNINGS=[]
class P(HTMLParser):
 def __init__(self):
  super().__init__(); self.links=[]; self.images=[]; self.canonicals=[]; self.headings=[]; self.lang=None; self.title=False; self.title_text=''; self.metas={}
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='html': self.lang=d.get('lang')
  if tag=='a' and d.get('href'): self.links.append(d['href'])
  if tag=='img' and d.get('src'): self.images.append((d['src'],d.get('alt')))
  if tag=='link' and d.get('rel')=='canonical' and d.get('href'): self.canonicals.append(d['href'])
  if tag in {f'h{i}' for i in range(1,7)}: self.headings.append(int(tag[1]))
  if tag=='meta':
   key=d.get('name') or d.get('property')
   if key and d.get('content'): self.metas[key]=d['content']
  if tag=='title': self.title=True
 def handle_endtag(self,tag):
  if tag=='title': self.title=False
 def handle_data(self,data):
  if self.title: self.title_text+=data
def target(url):
 p=urlparse(url)
 if p.scheme or p.netloc or url.startswith(('mailto:','tel:','#')): return None
 t=ROOT/p.path.lstrip('/')
 if p.path.endswith('/') or not t.suffix: t/='index.html'
 return t
def site_path(file):
 rel=file.relative_to(ROOT).as_posix()
 if rel=='index.html': return '/'
 if rel.endswith('/index.html'): return '/'+rel[:-10]
 return '/'+rel
html=[p for p in ROOT.rglob('*.html') if not any(x in EXCLUDED for x in p.parts)]
found={site_path(p) for p in html if p.name!='404.html'}
if found!=EXPECTED: ERRORS.append(f'Page set differs: expected {sorted(EXPECTED)}, got {sorted(found)}')
external=set()
for file in html:
 p=P(); p.feed(file.read_text(encoding='utf-8')); rel=file.relative_to(ROOT)
 if p.lang!='da': ERRORS.append(f'{rel}: missing lang=da')
 if not p.title_text.strip(): ERRORS.append(f'{rel}: missing title')
 if 'description' not in p.metas: ERRORS.append(f'{rel}: missing meta description')
 if file.name!='404.html':
  canonical='https://xn--suvern-tua.dk'+site_path(file)
  if p.canonicals!=[canonical]: ERRORS.append(f'{rel}: canonical should be {canonical}')
  for key in ('og:title','og:description','og:url','og:image','twitter:card'):
   if key not in p.metas: ERRORS.append(f'{rel}: missing {key}')
 if not p.headings or p.headings[0]!=1: ERRORS.append(f'{rel}: first heading must be h1')
 if p.headings.count(1)!=1: ERRORS.append(f'{rel}: expected exactly one h1')
 for before,after in zip(p.headings,p.headings[1:]):
  if after>before+1: ERRORS.append(f'{rel}: heading jumps h{before} to h{after}')
 for src,alt in p.images:
  if alt is None: ERRORS.append(f'{rel}: image {src} has no alt')
  t=target(src)
  if t and not t.exists(): ERRORS.append(f'{rel}: missing image {src}')
 for href in p.links:
  if href.startswith(('http://','https://')): external.add(href); continue
  t=target(href)
  if t and not t.exists(): ERRORS.append(f'{rel}: broken internal link {href}')
for path in ('404.html','robots.txt','sitemap.xml','CNAME','assets/images/favicon.svg','assets/images/social-card.webp','assets/images/9788785340085.jpg','assets/images/background.png','assets/images/book-cover.webp','assets/images/book-cover-640.webp','assets/images/background.webp','assets/images/background-mobile.webp','assets/images/leviathan-bg.webp'):
 if not (ROOT/path).exists(): ERRORS.append(f'Missing required file: {path}')
if (ROOT/'CNAME').read_text().strip()!='xn--suvern-tua.dk': ERRORS.append('CNAME must use punycode apex')
sitemap=(ROOT/'sitemap.xml').read_text()
for p in EXPECTED:
 if f'https://xn--suvern-tua.dk{p}' not in sitemap: ERRORS.append(f'sitemap missing {p}')
if 'Sitemap: https://xn--suvern-tua.dk/sitemap.xml' not in (ROOT/'robots.txt').read_text(): ERRORS.append('robots has wrong sitemap')
patterns={'GitHub token':r'gh[pousr]_[A-Za-z0-9_]{20,}','private key':r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----','generic secret assignment':r'''(?i)(?:api[_-]?key|password|secret|token)s*[:=]s*['"][^'"]{8,}['"]'''}
for file in ROOT.rglob('*'):
 if not file.is_file() or any(x in EXCLUDED for x in file.parts) or file.suffix.lower() in {'.webp','.png','.jpg','.jpeg','.gif'}: continue
 try: text=file.read_text(encoding='utf-8')
 except UnicodeDecodeError: continue
 for label,pattern in patterns.items():
  if re.search(pattern,text): ERRORS.append(f'Possible {label} in {file.relative_to(ROOT)}')
if '--external' in sys.argv:
 opener=urllib.request.build_opener(); opener.addheaders=[('User-Agent','suveraen.dk-link-check/1.0')]
 for url in sorted(external):
  try:
   with opener.open(url,timeout=20) as response:
    if response.status>=400: WARNINGS.append(f'External {response.status}: {url}')
  except urllib.error.HTTPError as exc:
   (WARNINGS if exc.code in (401,403,429) else ERRORS).append(f'External {exc.code}: {url}')
  except Exception as exc: WARNINGS.append(f'External check failed ({type(exc).__name__}): {url}')
for x in WARNINGS: print('WARNING:',x)
for x in ERRORS: print('ERROR:',x)
print(f'Checked {len(html)} HTML files, {len(external)} external URLs; {len(ERRORS)} error(s), {len(WARNINGS)} warning(s).')
sys.exit(1 if ERRORS else 0)
