"""Build compact PPTX seminars with embedded speaker notes and editable examples."""
from pathlib import Path
import io,json,re,hashlib,html,zipfile,math
from PIL import Image,ImageFont
from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR
from docx import Document
from docx.shared import Pt as DPt
from lxml import etree
from render import page,native_layout,fmt,C
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parents[1];RELEASE=OUT/'[3] Prezentări pentru seminare'
PX_PER_INCH=144

def rgb(s):return RGBColor.from_string(s.lstrip('#'))
def styled_runs(paragraph,text,size,bold=False,color=C['text'],docx=False):
    markup=fmt(text);parts=re.split(r'(<sub>.*?</sub>|<sup>.*?</sup>)',markup)
    for part in parts:
        if not part:continue
        sub=part.startswith('<sub>');sup=part.startswith('<sup>');plain=html.unescape(re.sub('<[^>]*>','',part));run=paragraph.add_run(plain) if docx else paragraph.add_run()
        if not docx:run.text=plain
        run.font.name='Arial';run.font.size=DPt(size) if docx else Pt(size);run.font.bold=bold
        if docx:
            run.font.subscript=sub;run.font.superscript=sup
        else:
            run.font.color.rgb=rgb(color)
            if sub or sup:run._r.get_or_add_rPr().set('baseline','-25000' if sub else '30000');run.font.size=Pt(size*0.72)
            run._r.get_or_add_rPr().set('lang','ro-RO')

def text_box(slide,box):
    x,y,w,h=box['x'],box['y'],box['w'],box['h'];background=box.get('bg')
    shape=slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,Inches(x/PX_PER_INCH),Inches(y/PX_PER_INCH),Inches(w/PX_PER_INCH),Inches(h/PX_PER_INCH)) if background else slide.shapes.add_textbox(Inches(x/PX_PER_INCH),Inches(y/PX_PER_INCH),Inches(w/PX_PER_INCH),Inches(h/PX_PER_INCH))
    if background:
        shape.fill.solid();shape.fill.fore_color.rgb=rgb(background);shape.line.color.rgb=rgb(C['border']);shape.line.width=Pt(1)
        try:shape.adjustments[0]=0.12
        except Exception:pass
    tf=shape.text_frame;tf.clear();tf.word_wrap=True;tf.vertical_anchor=MSO_ANCHOR.MIDDLE
    pad=30 if background else 0;tf.margin_left=tf.margin_right=Inches(pad/PX_PER_INCH);tf.margin_top=tf.margin_bottom=Inches((20 if background else 0)/PX_PER_INCH)
    if box['text']:
        p=tf.paragraphs[0];p.space_after=Pt(0);p.line_spacing=1.25
        styled_runs(p,box['text'],box['size']/2,box.get('bold',False),box.get('color',C['text']))
    return shape

def native_slide(slide,deck,data):
    slide.background.fill.solid();slide.background.fill.fore_color.rgb=rgb('#F8FBFD')
    # Editable examples use the same grid and palette as the infographic frames.
    for x in range(0,1921,40):
        line=slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x/144),0,Inches(0.45/144),Inches(7.5));line.fill.solid();line.fill.fore_color.rgb=rgb('#EDF2F5');line.line.fill.background()
    for y in range(0,1081,40):
        line=slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,0,Inches(y/144),Inches(13.333333),Inches(0.45/144));line.fill.solid();line.fill.fore_color.rgb=rgb('#EDF2F5');line.line.fill.background()
    common=[dict(x=80,y=65,w=1760,h=45,text=f'Microeconomie · ASEM · Seminarul {deck["seminar"]}',size=26,color=C['muted']),dict(x=80,y=118,w=1760,h=120,text=data['title'],size=68,bold=True,color=C['ink']),dict(x=80,y=1005,w=1560,h=45,text='Seminar · Idei esențiale și aplicație',size=24,color=C['muted']),dict(x=1695,y=1005,w=140,h=45,text=f'{data["number"]:02} / 10',size=24,color=C['muted'])]
    for box in common+native_layout(data):text_box(slide,box)

def put_notes(slide,text,seconds):
    tf=slide.notes_slide.notes_text_frame;tf.clear()
    for i,line in enumerate(('Timp orientativ: '+str(seconds)+' de secunde.\n\n'+text).split('\n\n')):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph();styled_runs(p,line,14,color=C['text'])

def docx_notes(deck,path):
    doc=Document();doc.styles['Normal'].font.name='Arial';doc.styles['Normal'].font.size=DPt(12)
    doc.add_heading('Seminarul '+str(deck['seminar'])+' — '+deck['title'],0)
    doc.add_paragraph('Conspect pentru lector · 10 diapozitive · aproximativ 11 minute')
    for data in deck['slides']:
        doc.add_heading(str(data['number'])+'. '+data['title'],level=1);doc.add_paragraph('Timp orientativ: '+str(data['planned_seconds'])+' de secunde.')
        for text in data['notes'].split('\n\n'):
            p=doc.add_paragraph();styled_runs(p,text,12,docx=True)
    doc.save(path)

def validate_dom(page_obj,deck,data):
    # Geometry is inspected at the actual 1920x1080 output resolution.
    return page_obj.evaluate('''() => {
      const issues=[];
      for (const el of document.querySelectorAll('h1,h2,p,.card,.equation,.end-row,.check,.native-box,.cover-visual,.route')) {
        const b=el.getBoundingClientRect();
        if(b.right>1880||b.left<20||b.bottom>1000)issues.push({tag:el.tagName,text:el.innerText.slice(0,90),box:[b.x,b.y,b.width,b.height]});
        if(el.scrollHeight>el.clientHeight+3 && el.classList.contains('native-box'))issues.push({nativeOverflow:el.innerText});
      }
      return issues;
    }''')

def build():
    RELEASE.mkdir(parents=True,exist_ok=True);notesdir=RELEASE/'Conspecte pentru lector';notesdir.mkdir(exist_ok=True)
    plan=json.loads((ROOT/'plan.json').read_text());raster=ROOT/'rendered';raster.mkdir(exist_ok=True);report=[];manifest=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage']);page_obj=browser.new_page(viewport={'width':1920,'height':1080},device_scale_factor=1)
        for deck in plan:
            pres=Presentation();pres.slide_width=Inches(13.333333);pres.slide_height=Inches(7.5);pres.core_properties.title='Seminarul '+str(deck['seminar'])+'. '+deck['title'];pres.core_properties.subject='Introducere pentru seminar și o aplicație';pres.core_properties.language='ro-RO'
            for data in deck['slides']:
                htmlpage=page(deck,data);page_obj.set_content(htmlpage,wait_until='load');page_obj.evaluate('document.fonts.ready')
                issues=validate_dom(page_obj,deck,data)
                if issues:raise ValueError(json.dumps({'seminar':deck['seminar'],'slide':data['number'],'issues':issues},ensure_ascii=False))
                picture=raster/f'{deck["seminar"]:02}-{data["number"]:02}.png';page_obj.screenshot(path=str(picture))
                # Palette compression changes storage only; source HTML and exact labels are retained.
                im=Image.open(picture).convert('RGB');im.quantize(colors=240,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).save(picture,optimize=True)
                slide=pres.slides.add_slide(pres.slide_layouts[6])
                if data['kind'] in ['exercise','solution']:native_slide(slide,deck,data)
                else:
                    shape=slide.shapes.add_picture(str(picture),0,0,width=pres.slide_width,height=pres.slide_height)
                    alt=' '.join([data['title']]+[str(v) for k,v in data.items() if k in ['lead','cards','steps','formula','lines','points']]);shape._element.xpath('.//p:cNvPr')[0].set('descr',alt)
                put_notes(slide,data['notes'],data['planned_seconds']);report.append({'seminar':deck['seminar'],'slide':data['number'],'kind':data['kind'],'notes_words':len(data['notes'].split()),'dom_geometry_ok':True,'native_editable':data['kind'] in ['exercise','solution'],'image_sha256':hashlib.sha256(picture.read_bytes()).hexdigest()})
            name=f'Prezentare - Seminarul {deck["seminar"]}. {deck["title"]}'
            pptx=RELEASE/(name+'.pptx');pres.save(pptx);docx=notesdir/(f'Seminar_{deck["seminar"]}_Conspect_Profesor.docx');docx_notes(deck,docx)
            for file in [pptx,docx]:manifest.append({'path':file.relative_to(OUT).as_posix(),'bytes':file.stat().st_size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
            print('built',deck['seminar'],'slides',len(pres.slides),'pptx bytes',pptx.stat().st_size,flush=True)
        browser.close()
    (ROOT/'render-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));(ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
if __name__=='__main__':build()
