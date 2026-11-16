import json,os,random,sys,urllib.request
U=os.environ.get("MAKEFUN_ENV_URL")or sys.exit("MAKEFUN_ENV_URL not set")
V=[0,100,320,330,500,900,20000]
KN=[-33,-31,-18,-14,14,18,31,33]
KG=[-17,-16,-15,-1,1,15,16,17]
DG=[-17,-15,15,17]
OG=[-16,-1,1,16]
R=random.Random(99)
Z=[R.getrandbits(64) for _ in range(1465)]
B=[9]*256
SD=1
CR=0
EP=-1
HM=0
KS=[68,180]
H=0
N=[0]
BUD=75000
TT={}
KI=[[0,0] for _ in range(512)]
D={'P':1,'N':2,'B':3,'R':4,'Q':5,'K':6,'p':-1,'n':-2,'b':-3,'r':-4,'q':-5,'k':-6}
class Stop(Exception):pass
def zi(p,s):return (p-1 if p>0 else 5-p)*120+s-64
def hf():
 h=0
 for s in range(64,184):
  if s&8:continue
  p=B[s]
  if p and p!=9:h^=Z[zi(p,s)]
 if SD<0:h^=Z[1440]
 h^=Z[1441+CR]
 if EP>=0:h^=Z[1457+(EP&7)]
 return h
def setup(fen):
 global B,SD,CR,EP,HM,KS,H
 f=fen.split()
 B=[9]*256
 for s in range(64,184):
  if not s&8:B[s]=0
 r=7
 for row in f[0].split('/'):
  c=0
  for ch in row:
   if ch.isdigit():c+=int(ch)
   else:
    p=D[ch];s=64+r*16+c;B[s]=p
    if abs(p)==6:KS[0 if p>0 else 1]=s
    c+=1
  r-=1
 SD=1 if f[1]=='w' else -1
 CR=(1 if 'K' in f[2] else 0)|(2 if 'Q' in f[2] else 0)|(4 if 'k' in f[2] else 0)|(8 if 'q' in f[2] else 0)
 EP=-1 if f[3]=='-' else 64+(int(f[3][1])-1)*16+ord(f[3][0])-97
 HM=int(f[4])
 H=hf()
def atk(s,by):
 if B[s-15*by]==by or B[s-17*by]==by:return 1
 for o in KN:
  if B[s+o]==by*2:return 1
 for o in KG:
  if B[s+o]==by*6:return 1
 for o in DG:
  t=s+o
  while B[t]!=9:
   if B[t]==by*3 or B[t]==by*5:return 1
   if B[t]:break
   t+=o
 for o in OG:
  t=s+o
  while B[t]!=9:
   if B[t]==by*4 or B[t]==by*5:return 1
   if B[t]:break
   t+=o
 return 0
def gen(cap):
 ms=[]
 for s in range(64,184):
  if s&8:continue
  p=B[s]
  if not p or p==9 or p*SD<0:continue
  a=abs(p)
  if a==1:
   d=16*SD;t=s+d
   if B[t]==0 and not cap:
    if t>>4 in (11,4):
     for q in (5,4,3,2):ms.append(s+(t<<8)+(q<<16))
    else:
     ms.append(s+(t<<8))
     if (s>>4)==(5 if SD>0 else 10) and B[t+d]==0:ms.append(s+((t+d)<<8))
   for o in (15,17):
    t=s+o*SD
    if (B[t]*SD<0 and B[t]!=9) or t==EP:
     if t>>4 in (11,4):
      for q in (5,4,3,2):ms.append(s+(t<<8)+(q<<16))
     else:ms.append(s+(t<<8))
  elif a==2:
   for o in KN:
    t=s+o
    if B[t]!=9 and B[t]*SD<=0 and (not cap or B[t]):ms.append(s+(t<<8))
  elif a==6:
   for o in KG:
    t=s+o
    if B[t]!=9 and B[t]*SD<=0 and (not cap or B[t]):ms.append(s+(t<<8))
   if not cap and SD>0 and s==68:
    if CR&1 and B[69]==0 and B[70]==0 and B[71]==4 and not atk(68,-1) and not atk(69,-1) and not atk(70,-1):ms.append(68+(70<<8))
    if CR&2 and B[67]==0 and B[66]==0 and B[65]==0 and B[64]==4 and not atk(68,-1) and not atk(67,-1) and not atk(66,-1):ms.append(68+(66<<8))
   elif not cap and SD<0 and s==180:
    if CR&4 and B[181]==0 and B[182]==0 and B[183]==-4 and not atk(180,1) and not atk(181,1) and not atk(182,1):ms.append(180+(182<<8))
    if CR&8 and B[179]==0 and B[178]==0 and B[177]==0 and B[176]==-4 and not atk(180,1) and not atk(179,1) and not atk(178,1):ms.append(180+(178<<8))
  else:
   ds=DG if a==3 else OG if a==4 else DG+OG
   for o in ds:
    t=s+o
    while B[t]!=9:
     if B[t]*SD>0:break
     if not cap or B[t]:ms.append(s+(t<<8))
     if B[t]:break
     t+=o
 out=[]
 for m in ms:
  t=(m>>8)&255
  if cap and B[t]==0 and t!=EP:continue
  u=mk(m)
  if not atk(KS[0 if SD<0 else 1],SD):out.append(m)
  un(m,u)
 return out
def mk(m):
 global SD,CR,EP,HM,H
 f=m&255;t=(m>>8)&255;q=(m>>16)&7
 p=B[f];cap=B[t];cs=t;rf=0;rt=0
 if t==EP and abs(p)==1:cs=t-16*SD;cap=B[cs]
 u=(cap,cs,CR,EP,HM,H,rf,rt)
 H^=Z[zi(p,f)]
 if cap:H^=Z[zi(cap,cs)]
 if q:H^=Z[zi(q*SD,t)]
 else:H^=Z[zi(p,t)]
 if EP>=0:H^=Z[1457+(EP&7)]
 H^=Z[1441+CR]
 B[f]=0;B[t]=q*SD if q else p
 if cs!=t:B[cs]=0
 if abs(p)==6 and abs(t-f)==2:
  rf=t+1 if t>f else t-2;rt=t-1 if t>f else t+1
  H^=Z[zi(B[rf],rf)]^Z[zi(B[rf],rt)];B[rt]=B[rf];B[rf]=0
  u=(cap,cs,CR,EP,HM,u[5],rf,rt)
 if abs(p)==6:KS[0 if SD>0 else 1]=t
 if abs(p)==6:CR&=12 if SD>0 else 3
 if f==64 or t==64:CR&=~2
 if f==71 or t==71:CR&=~1
 if f==176 or t==176:CR&=~8
 if f==183 or t==183:CR&=~4
 EP=f+16*SD if abs(p)==1 and abs(t-f)==32 else -1
 HM=0 if abs(p)==1 or cap else HM+1
 H^=Z[1441+CR]
 if EP>=0:H^=Z[1457+(EP&7)]
 H^=Z[1440]
 SD=-SD
 return u
def un(m,u):
 global SD,CR,EP,HM,H
 f=m&255;t=(m>>8)&255;q=(m>>16)&7
 cap,cs,CR,EP,HM,H,rf,rt=u
 SD=-SD
 if abs(B[t])==6:KS[0 if SD>0 else 1]=f
 B[f]=SD if q else B[t]
 B[t]=0
 if cap:B[cs]=cap
 if rf:B[rf]=B[rt];B[rt]=0
def ev():
 s=0;M=0;kc=0;bp=[0,0];wf=[0]*8;bf=[0]*8
 for sq in range(64,184):
  if sq&8:continue
  p=B[sq]
  if not p or p==9:continue
  a=abs(p);w=1 if p>0 else -1
  if a!=6:M+=V[a];s+=V[a]*w
  f=sq&7;r=(sq>>4)-4;rr=r if p>0 else 7-r
  c=(7-abs(2*f-7))+(7-abs(2*rr-7))
  if a==1:
   s+=(10*rr+2*(7-abs(2*f-7)))*w
   (wf if p>0 else bf)[f]+=1
   if rr>=3:
    t=sq+16*w;pp=1
    while 64<=t<192:
     if B[t-1]==-w or B[t]==-w or B[t+1]==-w:pp=0;break
     t+=16*w
    if pp:s+=15*rr*w
  elif a==2:s+=7*c*w
  elif a==3:s+=5*c*w;bp[0 if p>0 else 1]+=1
  elif a==4:s+=(3*c+(14 if rr==6 else 0))*w
  elif a==5:s+=2*c*w
  else:kc+=c*w
 s+=(10 if M<2600 else -6)*kc
 if bp[0]==2:s+=30
 if bp[1]==2:s-=30
 if M>=2600:
  for j in (0,1):
   k=KS[j];w=1 if j==0 else -1;d=16*w
   n=(B[k+d-1]==w)+(B[k+d]==w)+(B[k+d+1]==w)
   s+=(12*n-(30 if n==0 else 0))*w
 for f in range(8):
  if wf[f]>1:s-=12*(wf[f]-1)
  if bf[f]>1:s+=12*(bf[f]-1)
  if wf[f] and not (wf[f-1] if f else 0) and not (wf[f+1] if f<7 else 0):s-=10
  if bf[f] and not (bf[f-1] if f else 0) and not (bf[f+1] if f<7 else 0):s+=10
 return s if SD>0 else -s
def qs(a,b,pl):
 N[0]+=1
 if N[0]>BUD:raise Stop
 if pl>100:return ev()
 me=SD;ik=atk(KS[0 if me>0 else 1],-me)
 st=ev()
 if not ik:
  if st>=b:return b
  if st>a:a=st
 ms=gen(0 if ik else 1)
 if not ms:return -19990+pl if ik else a
 ms.sort(key=lambda m:V[abs(B[(m>>8)&255])]*16-V[abs(B[m&255])] if B[(m>>8)&255] else 0,reverse=True)
 for m in ms:
  u=mk(m)
  if not ik and not (m>>16)&7 and st+V[abs(u[0])]+200<a and not atk(KS[0 if me<0 else 1],me):
   un(m,u);continue
  try:sc=-qs(-b,-a,pl+1)
  except Stop:un(m,u);raise
  un(m,u)
  if sc>=b:return b
  if sc>a:a=sc
 return a
def srch(d,a,b,pl):
 global SD,EP,H
 N[0]+=1
 if N[0]>BUD:raise Stop
 if HM>=100:return 0
 me=SD;ik=atk(KS[0 if me>0 else 1],-me)
 if ik and pl<40:d+=1
 if d<=0:return qs(a,b,pl)
 e=TT.get(H);tm=0
 if e:
  if e[0]>=d:
   sc=e[1]
   if e[2]==0:return sc
   if e[2]==1 and sc>=b:return sc
   if e[2]==2 and sc<=a:return sc
  tm=e[3]
 if d>2 and not ik:
  e0=EP;h0=H;SD=-SD;H^=Z[1440]
  if EP>=0:H^=Z[1457+(EP&7)]
  EP=-1
  try:sc=-srch(d-3,-b,-b+1,pl+1)
  except Stop:EP=e0;H=h0;SD=-SD;raise
  EP=e0;H=h0;SD=-SD
  if sc>=b:return b
 ms=gen(0)
 if not ms:return -19990+pl if ik else 0
 def key(m):
  t=(m>>8)&255;v=B[t];s=0
  if v:s=1000+V[abs(v)]*16-V[abs(B[m&255])]
  elif t==EP:s=1000+1500
  if m==tm:s+=100000
  if m==KI[pl][0]:s+=9000
  elif m==KI[pl][1]:s+=8000
  return s
 ms.sort(key=key,reverse=True)
 best=-30000;bm=0;fl=2
 for i,m in enumerate(ms):
  t=(m>>8)&255;cap=B[t]!=0 or t==EP
  u=mk(m)
  try:
   if i>3 and d>2 and not cap and not (m>>16)&7 and m!=tm and m!=KI[pl][0]:
    sc=-srch(d-2,-b,-a,pl+1)
    if sc>a:sc=-srch(d-1,-b,-a,pl+1)
   else:sc=-srch(d-1,-b,-a,pl+1)
  except Stop:un(m,u);raise
  un(m,u)
  if sc>best:best=sc;bm=m
  if sc>a:a=sc;fl=0
  if a>=b:
   if not B[(m>>8)&255]:
    if m!=KI[pl][0]:KI[pl][1]=KI[pl][0];KI[pl][0]=m
   fl=1;break
 TT[H]=(d,best,fl,bm)
 if len(TT)>300000:TT.clear()
 return best
def root():
 ms=gen(0)
 if len(ms)==1:return ms[0]
 if not ms:return 0
 for k in range(512):KI[k][0]=0;KI[k][1]=0
 N[0]=0;best=ms[0]
 for d in range(1,13):
  try:
   a=-30000;bb=0
   for m in ms:
    u=mk(m)
    try:sc=-srch(d-1,-30000,-a,1)
    except Stop:un(m,u);raise
    un(m,u)
    if sc>a:a=sc;bb=m
   best=bb;ms.remove(bb);ms.insert(0,bb)
  except Stop:break
 return best
def uci(m):
 f=m&255;t=(m>>8)&255;q=(m>>16)&7
 s="abcdefgh"[f&7]+str((f>>4)-3)+"abcdefgh"[t&7]+str((t>>4)-3)
 return s+("nbrq"[q-2] if q else "")
def choose(fen,legal):
 setup(fen)
 try:
  m=root();u=uci(m)
  if u in legal:return u
 except Exception:pass
 bv=-1;bu=legal[0]
 for u in legal:
  t=64+(int(u[3])-1)*16+ord(u[2])-97
  v=abs(B[t])
  if v>bv:bv=v;bu=u
 return bu
#===DRIVER===
def post(p,b):
 q=urllib.request.Request(U+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
 try:
  with urllib.request.urlopen(q) as r:return json.load(r)
 except Exception as e:return {"status":"error","error":str(e)}
errs=0
while True:
 g=post("/game",{})
 if g.get("status")=="done":break
 if g.get("status")=="error":
  errs+=1
  if errs>5:sys.exit("env error")
  continue
 errs=0
 while g.get("status")=="your_move":
  try:mv=choose(g["fen"],g["legal_moves"])
  except Exception:mv=g["legal_moves"][0]
  h=post("/move",{"game":g["game"],"move":mv})
  if h.get("status")=="error":h=post("/game",{})
  g=h
 sys.stderr.write(f"game {g.get('game')}: {g.get('outcome')} by {g.get('reason')}\n")
sys.stderr.write(f"done: {g.get('wins')}W {g.get('draws')}D {g.get('losses')}L\n")
