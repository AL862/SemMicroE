"""Shared inline components for Moodle's editable HTML content."""
import html,json
from pathlib import Path
ROOT=Path(__file__).parent
INK='#123B5D';MUTED='#556374';BORDER='#E2E8EF';SURFACE='#F6F8FB'
def intro(description):
 return '<div data-course-intro style="padding:16px 20px;background:'+SURFACE+';border-left:4px solid '+INK+';border-radius:12px;margin-bottom:20px;"><h3 style="font-size:14px;line-height:1.5;letter-spacing:1px;text-transform:uppercase;color:'+MUTED+';margin:0 0 8px;">Ideea seminarului</h3><p style="font-size:18px;line-height:1.6;max-width:75ch;margin:0;">'+description+'</p></div>'
def objectives(items,fmt):
 rows=[]
 for i,t in enumerate(items,1):rows.append('<li style="display:flex;align-items:flex-start;gap:12px;padding:12px 16px;background:'+SURFACE+';border:1px solid '+BORDER+';border-radius:10px;min-width:0;"><span aria-hidden="true" style="flex:0 0 28px;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:'+INK+';color:#FFFFFF;font-size:14px;font-weight:700;">'+str(i)+'</span><span style="min-width:0;">'+fmt(t)+'</span></li>')
 return '<ol style="list-style:none;padding:0;margin:0;display:grid;gap:8px;">'+''.join(rows)+'</ol>'
def contents(titles,h3):
 labels=['Obiective','Teorie și model interactiv','Formule și notații','Probleme rezolvate','10 probleme pentru exersare','Întrebări și teste cu răspunsuri','Concluzii','Materiale']
 return '<nav id="cuprins" aria-label="Cuprins" style="padding:16px;background:'+SURFACE+';border:1px solid '+BORDER+';border-radius:12px;margin:24px 0;">'+h3('Alegeți secțiunea')+'<div style="display:flex;flex-wrap:wrap;gap:8px;">'+''.join('<a class="course-jump" href="#s'+str(i)+'" style="display:flex;align-items:center;gap:10px;flex:1 1 220px;min-width:0;padding:12px;background:#FFFFFF;border:1px solid '+BORDER+';border-radius:10px;min-height:48px;font-size:16px;line-height:1.45;color:'+INK+';text-decoration:none;"><span aria-hidden="true" style="font-weight:700;">'+str(i).zfill(2)+'</span><span>'+label+'</span></a>' for i,label in enumerate(labels,1))+'</div></nav>'
def navigation(n,titles):
 file=ROOT/'navigation.json'
 cfg=json.loads(file.read_text()) if file.exists() else {'course_url':'https://moodle.ase.md/course/view.php?id=4708','seminars':{}}
 slots=[]
 if n>1:slots.append((n-1,'Seminarul anterior','← Seminarul '+str(n-1),titles[n-1]))
 slots.append((0,'Navigarea cursului','Toate seminarele','Reveniți la lista temelor'))
 if n<11:slots.append((n+1,'Seminarul următor','Seminarul '+str(n+1)+' →',titles[n+1]))
 out='<nav aria-label="Navigarea cursului" style="display:flex;flex-wrap:wrap;gap:12px;margin-top:32px;padding-top:20px;border-top:1px solid '+BORDER+';">'
 for number,kicker,label,sub in slots:
  center=number==0;url=cfg['course_url'] if center else cfg['seminars'].get(str(number));fg='#FFFFFF' if center else INK;bg=INK if center else '#FFFFFF';tag='a' if url else 'span'
  attr=' href="'+html.escape(url,quote=True)+'"' if url else ' aria-disabled="true" data-link-slot="seminar-'+str(number)+'"'
  style='display:flex;flex-direction:column;justify-content:center;gap:6px;flex:1 1 230px;min-width:0;padding:16px 18px;min-height:108px;border:1px solid '+(INK if center else BORDER)+';border-radius:12px;background:'+bg+';color:'+fg+';text-decoration:none;'
  if not url:style+='border-style:dashed;background:'+SURFACE+';'
  out+='<'+tag+attr+' class="course-nav-card" style="'+style+'"><span style="font-size:14px;line-height:1.4;">'+kicker+'</span><strong style="font-size:18px;line-height:1.4;">'+label+'</strong><span style="font-size:14px;line-height:1.45;">'+html.escape(sub)+'</span></'+tag+'>'
 return out+'</nav>'
STYLE='[data-course-seminar] .course-jump:hover,[data-course-seminar] a.course-nav-card:hover{box-shadow:0 4px 12px #123b5d16;border-color:#1F6388!important}[data-course-seminar] a:focus-visible,[data-course-seminar] summary:focus-visible{outline:3px solid #1F6388;outline-offset:3px}[data-course-seminar] section{scroll-margin-top:20px}'
