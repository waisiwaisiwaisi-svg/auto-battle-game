#!/usr/bin/env python3
# index.html から 日本語の 文（訳す もと）を ぬきだす：python3 tools/i18n/extract.py 出力.json [index.html]
# I18N ブロック（訳）が 入っていない index.html から ぬくこと（入っていると 訳も ひろってしまう）
import re,json,sys
s=open(sys.argv[2] if len(sys.argv)>2 else 'index.html',encoding='utf-8').read()
JP=re.compile(r'[\u3040-\u30ff\u4e00-\u9fff\uff01-\uff5e]')
# strip big data blobs (base64) quickly irrelevant
segs={}
def add(t,src):
  t=t.strip()
  t=re.sub(r'\s+',' ',t)
  if not t or not re.search(r'[\u3040-\u30ff\u4e00-\u9fff]',t): return
  if len(t)>400: return
  segs.setdefault(t,src)
def tpl_parts(body):
  # replace ${...} with ⟦n⟧ handling nesting
  out='';i=0;n=0
  while i<len(body):
    if body.startswith('${',i):
      d=0;j=i+1
      while j<len(body):
        if body[j]=='{': d+=1
        elif body[j]=='}':
          d-=1
          if d==0: break
        j+=1
      out+='⟦%d⟧'%n;n+=1;i=j+1
    else: out+=body[i];i+=1
  return out
def split_html(t,src):
  # attributes
  for a in re.findall(r'(?:title|placeholder|aria-label|alt)="([^"]*)"',t): add(a,src)
  for p in re.split(r'<[^>]*>',t): 
    # renumber placeholders per segment
    k=[0];m={}
    def rn(mo):
      m.setdefault(mo.group(0),len(m)); return '⟦%d⟧'%m[mo.group(0)]
    add(re.sub(r'⟦\d+⟧',rn,p),src)
# JS part: find script blocks
NEST=[]
def scan(js):
  i=0;L=len(js)
  while i<L:
    c=js[i]
    if c=='/' and js.startswith('//',i):
      e=js.find('\n',i); i=L if e<0 else e; continue
    if c=='/' and js.startswith('/*',i):
      e=js.find('*/',i+2); i=L if e<0 else e+2; continue
    if c in '\'"`':
      j=i+1;buf=''
      while j<L:
        if js[j]=='\\': buf+=js[j:j+2]; j+=2; continue
        if c=='`' and js.startswith('${',j):
          d=0;k=j+1
          while k<L:
            if js[k]=='{': d+=1
            elif js[k]=='}':
              d-=1
              if d==0: break
            k+=1
          NEST.append(js[j+2:k])
          buf+=js[j:k+1]; j=k+1; continue
        if js[j]==c: break
        if c!='`' and js[j]=='\n': break
        buf+=js[j]; j+=1
      if JP.search(buf) and 'base64' not in buf[:40]:
        body=tpl_parts(buf) if c=='`' else buf
        body=body.replace('\\n','\n').replace("\\'","'").replace('\\"','"')
        split_html(body,'js')
      i=j+1; continue
    i+=1

for sm in re.finditer(r'<script[^>]*>(.*?)</script>',s,re.S):
  scan(sm.group(1))
while NEST:
  scan(NEST.pop())
# HTML outside scripts
html=re.sub(r'<script[^>]*>.*?</script>','',s,flags=re.S)
html=re.sub(r'<style[^>]*>.*?</style>','',html,flags=re.S)
split_html(html,'html')
print(len(segs), sum(len(k) for k in segs))
json.dump(list(segs.keys()),open(sys.argv[1],'w'),ensure_ascii=False,indent=0)
