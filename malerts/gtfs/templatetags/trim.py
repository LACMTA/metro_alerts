from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def trim(value):
	return value.strip()

@register.filter(name='spotless')
@stringfilter
def spotless(html_string):
	import re
	from django.utils.html import strip_tags
	text_string=strip_tags(html_string)
	rx = re.compile('\W+')
	res = rx.sub(' ', text_string).strip()
	return res

# 
# # found this on djangosnippets, not deployed
# @register.filter(name='plaintext')
# @stringfilter
# def plaintext(value):
# 	from BeautifulSoup import BeautifulSoup, Tag, NavigableString
# 	from django.utils.safestring import mark_safe
# 	#
# 	soup = BeautifulSoup(value)
# 	anchors = soup.findAll('a')
# 	for a in anchors:
# 		substitute = Tag(soup, 'span')
# 		substitute.insert(0,a.string)
# 		meta = []
# 		attrs = [k for k,v in a.attrs]
# 		if 'title' in attrs: meta.append(a['title'])
# 		if 'href' in attrs: meta.append(a['href'])
# 		if meta: substitute.insert(1,NavigableString(' (%s)' % ', '.join(meta)))
# 		a.replaceWith(substitute)
# 	#
# 	images = soup.findAll('img')
# 	for img in images:
# 		substitute = Tag(soup,'span')
# 		meta = []
# 		attrs = [k for k,v in img.attrs]
# 		if 'src' in attrs: meta.append(img['src'])
# 		if 'title' in attrs: meta.append(img['title'])
# 		if 'alt' in attrs: meta.append(img['alt'])
# 		if meta: substitute.insert(0,NavigableString(' (%s)' % ', '.join(meta)))
# 		img.replaceWith(substitute)
# 	return mark_safe(''.join(soup.findAll(text=True)))
# plaintext.mark_safe = True
