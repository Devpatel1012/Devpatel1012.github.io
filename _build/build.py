import re, os
SRC='/mnt/user-data/uploads'; OUT='/home/claude/site'
DRIVE='https://drive.google.com/file/d/1fnqYmCmQJ8C3AVjno1M2IQzjCF0plIcq/view?usp=drive_link'
CERT='https://drive.google.com/file/d/1Mt5ruWlT1txzvO5x-bUfxy7nGqrc6HCK/view?usp=drive_link'
GH='https://github.com/Devpatel1012'; LI='https://www.linkedin.com/in/dev-delvadiya'; HF='https://huggingface.co/devpatel1012'; MAIL='devp63081@gmail.com'
NAV=[('index.html','Hello','01'),('research.html','Work','02'),('projects.html','Projects','03'),('reading.html','Shelf','04'),('about.html','About','05')]

def head(title, desc, page):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="https://devpatel1012.github.io/{page}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="https://devpatel1012.github.io/{page}">
  <meta property="og:image" content="https://devpatel1012.github.io/assets/og-image.png">
  <script>
    (function () {{ try {{ localStorage.removeItem('dev_portfolio_theme'); }} catch (e) {{}} document.documentElement.setAttribute('data-theme', 'bright'); }})();
  </script>
  <link rel="stylesheet" href="style.css">
</head>
<body>
'''

def shell_open(active):
    def cls(h): return ' class="active"' if h==active else ''
    rail=''.join('<a href="%s"%s><i>%s</i>%s</a>'%(h,cls(h),n,l) for h,l,n in NAV)
    drawer=''.join('<a href="%s"%s><span>%s</span><span>→</span></a>'%(h,cls(h),l) for h,l,n in NAV)
    return f'''
  <aside class="rail" aria-label="Primary">
    <a href="index.html" class="brand"><b>Dev Delvadiya</b><span>AI engineer &amp; researcher</span></a>
    <nav aria-label="Primary Navigation">{rail}</nav>
    <div class="rail-foot">
      <a class="btn sm primary" href="{DRIVE}" target="_blank" rel="noopener">Resume ↗</a>
      <div class="links"><a href="{GH}" target="_blank" rel="noopener">GitHub</a><a href="{LI}" target="_blank" rel="noopener">LinkedIn</a><a href="{HF}" target="_blank" rel="noopener">Hugging Face</a><a href="mailto:{MAIL}">Email</a></div>
    </div>
  </aside>
  <header class="topbar">
    <a href="index.html" class="brand"><b>Dev Delvadiya</b></a>
    <button class="mobile-toggle" type="button" aria-label="Toggle navigation menu" aria-expanded="false">☰</button>
  </header>
  <div class="mobile-nav-drawer" role="dialog" aria-modal="true" aria-label="Mobile Navigation">
    <div class="mobile-nav-links">{drawer}<a href="{DRIVE}" target="_blank" rel="noopener"><span>Resume</span><span>↗</span></a></div>
    <div class="mobile-nav-footer"><a href="{GH}" target="_blank" rel="noopener">GitHub ↗</a><a href="{LI}" target="_blank" rel="noopener">LinkedIn ↗</a><a href="{HF}" target="_blank" rel="noopener">Hugging Face ↗</a><a href="mailto:{MAIL}">Email ↗</a></div>
  </div>
  <div class="page">
  <main>
'''
FOOT=f'''
  </main>
  </div>
  <footer class="site-footer">
    <div class="wrap">
      <span>Ahmedabad, Gujarat, India</span>
      <span>Made with care by Dev Delvadiya · 2026</span>
      <span><a href="{GH}" target="_blank" rel="noopener">GitHub ↗</a> · <a href="{LI}" target="_blank" rel="noopener">LinkedIn ↗</a> · <a href="mailto:{MAIL}">Email ↗</a></span>
    </div>
  </footer>
  <script src="script.js"></script>
</body>
</html>
'''
def page(fn,title,desc,active,body):
    open(f'{OUT}/{fn}','w',encoding='utf-8').write(head(title,desc,fn)+shell_open(active)+body+FOOT)

CONTACT=f'''<section><div class="wrap"><div class="contact">
  <div class="note">say hello</div>
  <h2>Let's talk about ideas, research or a good book.</h2>
  <p>I'm open to research collaborations, internships and thoughtful conversations.</p>
  <div class="btn-row"><a class="btn primary" href="mailto:{MAIL}">{MAIL}</a><a class="btn" href="{DRIVE}" target="_blank" rel="noopener">Resume ↗</a></div>
</div></div></section>'''

AUDRIA='''<article class="card tl-item now-role">
  <div class="meta"><span>Sep 2026 — Present</span><span>Industry experience</span></div>
  <h3><a href="https://audria.tech" target="_blank" rel="noopener">audria.tech ↗</a></h3>
  <div class="role">AI Intern · Audio intelligence</div>
  <div class="legend"><span><i style="background:#C8553D"></i>Speaker A</span><span><i style="background:#7A9A7E"></i>Speaker B</span><span><i style="background:#E9B44C"></i>Speaker C</span></div>
  <div class="wave" data-wave aria-hidden="true"></div>
  <p class="viz-cap">Illustration: speaker turns in a diarized recording.</p>
  <ul>
    <li>Developing a linear pipeline that addresses audio difficulty using the ISA algorithm, evaluated on <span class="ph" data-ph>120 hours</span> of audio and running <span class="ph" data-ph>3.2x</span> faster than the previous baseline.</li>
    <li>Improving the audio diarization pipeline, lowering diarization error rate from <span class="ph" data-ph>18.4%</span> to <span class="ph" data-ph>12.1%</span> on an internal evaluation set.</li>
  </ul>
  <div class="chips"><span class="chip">Audio pipelines</span><span class="chip">Speaker diarization</span></div>
</article>'''
XU='''<article class="card tl-item">
  <div class="meta"><span>Feb 2026 — Present</span><span>Remote</span></div>
  <h3><a href="https://www.cs.cmu.edu/~mxu1/" target="_blank" rel="noopener">Xu Lab, Carnegie Mellon University ↗</a></h3>
  <div class="role">Research Intern · Advisor: Prof. Min Xu</div>
  <ul>
    <li>Developed deep learning models for brain MRI surface registration, improving anatomical alignment and preserving geometric consistency across datasets.</li>
    <li>Designed end-to-end pipelines for learning-based anatomical alignment, ensuring spatial structure preservation in medical imaging tasks.</li>
    <li>Distributed a fully preprocessed IXI benchmark subject in a public repository to lower the barrier for 3D medical researchers.</li>
  </ul>
  <div class="foot"><a href="project-brain-mri.html">Case study →</a><a href="https://github.com/Devpatel1012/Brain-MRI-Surface-Registration" target="_blank" rel="noopener">Repository ↗</a></div>
</article>'''
INFOSYS=f'''<article class="card tl-item">
  <div class="meta"><span>Nov 2025 — Jan 2026</span><span>Remote</span></div>
  <h3>Infosys Springboard</h3>
  <div class="role">Machine Learning Intern</div>
  <ul>
    <li>Led development of ANPR and ATCC systems, building deep learning models for multi-class vehicle detection and classification.</li>
    <li>Engineered automated data pipelines and applied data augmentation techniques, improving model robustness and scalability.</li>
    <li>Achieved 85% accuracy across 12 vehicle classes and improved overall performance by 4%.</li>
  </ul>
  <div class="chips"><span class="chip sage">Object detection</span><span class="chip sage">Data augmentation</span><span class="chip sage">12 vehicle classes</span></div>
  <div class="foot"><a href="{CERT}" target="_blank" rel="noopener">Certificate ↗</a></div>
</article>'''
GTU='''<article class="card tl-item">
  <div class="meta"><span>Jun 2025 — Aug 2025</span><span>Ahmedabad</span></div>
  <h3>GTU: Brain Tumor Classification</h3>
  <div class="role">Undergraduate Researcher · Advisor: Prof. Raj Hakani</div>
  <ul>
    <li>Designed a CNN-based MRI tumor classification model, improving generalization across multi-class datasets.</li>
    <li>Implemented a two-stage training strategy (classification head, then fine-tuning) on a VGG16-based architecture.</li>
    <li>Achieved 97.88% classification accuracy; the work was accepted at ICMLDE 2025.</li>
  </ul>
  <div class="foot"><a href="project-brainscan-ai.html">BrainScan AI →</a><a href="https://github.com/Devpatel1012/BrainTumorClassification-" target="_blank" rel="noopener">Repository ↗</a></div>
</article>'''

BIB='''@inproceedings{delvadiya2025braintumor,
  title={Two-Stage Transfer Learning with Modified VGG16 for Multi-Class Brain Tumor Classification on Heterogeneous MRI},
  author={Delvadiya, Dev and Hakani, Raj},
  booktitle={Proceedings of the International Conference on Machine Learning and Data Engineering (ICMLDE)},
  year={2025},
  note={Accepted for publication}
}'''
PUB=f'''<article class="card">
  <div class="meta"><span>ICMLDE 2025 · Elsevier Procedia Computer Science</span><span>First author</span></div>
  <h3>Two-Stage Transfer Learning with Modified VGG16 for Multi-Class Brain Tumor Classification on Heterogeneous MRI</h3>
  <p>Dev Delvadiya, Raj Hakani. A two-stage transfer learning approach for brain tumor classification from MRI, covering glioma, meningioma, pituitary and normal scans.</p>
  <div class="foot">
    <a href="https://github.com/Devpatel1012/BrainTumorClassification-" target="_blank" rel="noopener">Code ↗</a>
    <button type="button" class="pub-btn" data-bibtex-toggle="bibtex-box">BibTeX</button>
    <button type="button" class="pub-btn primary" data-bibtex-copy="bibtex-code">Copy BibTeX</button>
  </div>
  <div id="bibtex-box" class="bibtex-box"><div class="bibtex-head"><span>delvadiya2025braintumor</span><button type="button" class="bibtex-copy-btn" data-bibtex-copy="bibtex-code">Copy</button></div><pre id="bibtex-code">{BIB}</pre></div>
</article>'''

LETTER='''<section id="letter"><div class="wrap">
<div class="letter">
  <div class="eyebrow">A letter, of sorts</div>
  <h2>A little about how I see things.</h2>
  <p>I have always believed that if I choose to do something, I owe it my best. I don't like leaving things halfway, especially when I know I could give them a little more thought, a little more time, or a little more care. I may take my time before committing to something, but once I do, I want to see it through and feel that I have done it right. To me, the satisfaction is not only in getting something done. It is in knowing that I gave it my honest effort.</p>
  <p>As an AI engineer with a research background, I am drawn to questions that don't always have immediate answers. I enjoy exploring ideas, understanding why things work the way they do, and looking for possibilities beyond what is already known. I am ambitious, but I also understand that meaningful things rarely happen overnight. They take patience, a willingness to learn, and the discipline to keep going, even when progress feels slow. I try to carry that into my work and, honestly, into the way I live.</p>
  <div class="turn">But there is more to me than the work I do.</div>
  <p>I love the idea of travelling somewhere unfamiliar, especially to places that haven't been written about a hundred times. There is something beautiful about discovering a place without already knowing what to expect from it. I feel much the same way about books. Every now and then, a book lets me step into someone else's world, understand a different way of thinking, or see something familiar from an entirely new perspective. That is one of the nicest things about being curious: there is always more to discover.</p>
  <p>I have never been drawn to consuming more just for the sake of it. I would rather sit through a long conversation that leaves me thinking than spend hours scrolling through things I will forget in a few minutes. I feel similarly about cinema. I have a soft spot for older films, especially those that tell simple stories but leave you with something to think about long after they end. Sometimes the quietest stories have the most to say.</p>
  <p>And then there is visualization, which connects naturally with the way I think about ideas. I find it fascinating how something complicated can become clearer when you find the right way to represent it. Understanding something is only half the journey. Being able to see it, make sense of it, and help someone else understand it matters just as much.</p>
  <p>At the heart of it, I am someone who wants to keep learning, keep exploring, and put genuine care into whatever I choose to do. I want my work to mean something, my experiences to teach me something, and my curiosity to take me places I haven't thought of yet. I don't have everything figured out, and I don't think I need to. There is still so much to learn, so much to experience, and so much room to become better at what I do and who I am.</p>
  <div class="sign">Dev</div>
</div></div></section>'''

PACKER='''<div class="packer" aria-hidden="true"><div class="tokgrid big" data-tokgrid="256"></div><span class="arrow">Token Packer<br>256 → 64</span><div class="tokgrid small" data-tokgrid="64"></div></div>
  <p class="viz-cap">Illustration: 256 visual tokens packed into 64 (75% fewer).</p>'''

def proj_cards(featured=False):
    cards=[
     ('vlm medical','Research project · Oct 2025 — Present','MedOptm: Compact Vision-Language Reasoning for Clinical VQA','A sub-2B parameter vision-language model for medical question answering.',
      'Pairs a CvT-24 encoder with an architectural Token Packer and a 1.7B LLaMA backbone. Built with Prof. Raj Hakani at GTU, reaching a 0.33 METEOR score while staying small enough for clinical hardware.',PACKER,
      ['CvT-24','Token Packer','LLaMA 1.7B','METEOR 0.33'],[('project-medoptm.html','Case study →'),('https://github.com/Devpatel1012/MedOptm','Code ↗')]),
     ('medical','Xu Lab, CMU · Feb 2026 — Present','Brain MRI Surface Registration','Aligning predicted cortical meshes with ground-truth surfaces.',
      'Non-rigid deep learning registration that preserves the geometry of sulcal folds, built on FreeSurfer reconstructions of the IXI benchmark and inspected in Freeview.','',
      ['FreeSurfer','PyTorch3D','IXI dataset'],[('project-brain-mri.html','Case study →'),('https://github.com/Devpatel1012/Brain-MRI-Surface-Registration','Code ↗')]),
     ('medical','GTU · Jun — Aug 2025','BrainScan AI','A web interface for multi-class brain tumor classification.',
      'A deployed CNN with real-time inference behind an interactive interface, built on the two-stage VGG16 training strategy that reached 97.88% accuracy.','',
      ['VGG16','Two-stage training','97.88% accuracy'],[('project-brainscan-ai.html','Case study →'),('https://github.com/Devpatel1012/BrainTumorClassification-','Code ↗')]),
     ('vlm','Build','CvT-24 from First Principles','The Convolutional Vision Transformer, written without wrapper libraries.',
      'A modular PyTorch implementation of CvT-24 with depthwise separable token projections and three hierarchical stages, built to understand the tensor mechanics from the ground up.','',
      ['PyTorch','Depthwise projections','Hierarchical stages'],[('project-cvt24.html','Case study →'),('https://github.com/Devpatel1012/cvt-24','Code ↗')]),
     ('vlm','Build','Fashion Multimodal Semantic Retrieval','Cross-modal search that keeps attributes attached to the right garment.',
      'A residual adapter on a frozen FashionCLIP text encoder, trained with hard negatives so that "blue shirt, black collar" no longer matches "black shirt, blue collar", served through FAISS.','',
      ['FashionCLIP','FAISS','Residual adapter'],[('project-fashion-retrieval.html','Case study →'),('https://github.com/Devpatel1012/Fashion_Retrieval_Model','Code ↗')]),
     ('automation','Build','Automated Article Generation','A workflow that drafts, refines and publishes articles on its own.',
      'Connects Notion, n8n and the Gemini API to generate, refine and publish articles to Dev.to without manual steps.','',
      ['n8n','Notion','Gemini API','Dev.to'],[]),
    ]
    if featured: cards=cards[:3]
    out=[]
    for cat,meta,title,tag,body,viz,chips,links in cards:
        l=''.join(f'<a href="{h}"'+(' target="_blank" rel="noopener"' if h.startswith('http') else '')+f'>{t}</a>' for h,t in links)
        foot=f'<div class="foot">{l}</div>' if l else ''
        ch=''.join(f'<span class="chip">{c}</span>' for c in chips)
        out.append(f'<article class="card project-card" data-category="{cat}"><div class="meta"><span>{meta}</span></div><h3>{title}</h3><p class="tagline">{tag}</p><p>{body}</p>{viz}<div class="chips">{ch}</div>{foot}</article>')
    return '\n'.join(out)

def recog():
    items=[('Top ~2.3%','Selected for Amazon ML Summer School 2026, one of 3,000 chosen from over 130,000 applicants.'),
           ('4,000+','Downloads of a Hugging Face dataset within its first month of release.'),
           ('98.77%','Accuracy across four MRI tumor categories in a first-author paper in Elsevier Procedia Computer Science.'),
           ('Winner','GTU State-Level Hackathon.')]
    return '<div class="cred">'+''.join(f'<div class="card"><div class="big">{b}</div><p>{t}</p></div>' for b,t in items)+'</div>'

# ---------------- index ----------------
now=f'''<div class="now"><span class="dot" aria-hidden="true"></span><span><strong>Right now:</strong> AI Intern at audria.tech (since Sep 2026), Research Intern at Xu Lab, CMU, and reading <em>Dimensionality Reduction in Machine Learning</em>.</span></div>'''
idx=f'''
<div class="wrap hero">
  <div>
    <div class="eyebrow">AI engineer · researcher · Ahmedabad, India</div>
    <h1>Hello, I'm <em>Dev</em>.</h1>
    <p class="lede">I build and study AI systems, mostly in medical imaging, vision-language models and audio. I like hard questions, unfamiliar places and quiet films.</p>
    <div class="btn-row"><a class="btn primary" href="research.html">See my work</a><a class="btn" href="{DRIVE}" target="_blank" rel="noopener">Resume ↗</a><a class="btn" href="{GH}" target="_blank" rel="noopener">GitHub ↗</a></div>
    {now}
  </div>
  <div class="portrait"><span class="tape"></span><div class="photo"><img src="assets/dev-portrait.jpg" alt="Portrait of Dev Delvadiya" width="480" height="480"></div><span class="tag">hi there</span></div>
</div>
{LETTER}
<section id="work"><div class="wrap">
  <div class="sec-head"><div><h2>Where I've been working</h2><div class="squiggle"></div></div><a class="btn sm" href="research.html">Full details →</a></div>
  <div class="timeline">{AUDRIA}{XU}{INFOSYS}</div>
</div></section>
<section id="projects"><div class="wrap">
  <div class="sec-head"><div><h2>Things I've built</h2><div class="squiggle"></div></div><a class="btn sm" href="projects.html">All projects →</a></div>
  <div class="project-list">{proj_cards(True)}</div>
</div></section>
<section id="recognition"><div class="wrap">
  <div class="sec-head"><div><h2>Along the way</h2><div class="squiggle"></div></div></div>
  {recog()}
  <div style="margin-top:20px">{PUB}</div>
</div></section>
{CONTACT}'''
page('index.html','Dev Delvadiya | AI Engineer & Researcher','Dev Delvadiya is an AI engineer with a research background in medical imaging, vision-language models and audio. Based in Ahmedabad, India.','index.html',idx)

# ---------------- work ----------------
work=f'''
<div class="wrap page-hero"><div class="eyebrow">02 · Work</div><h1>Work and research.</h1>
<p class="lede">Industry and research roles, newest first. MedOptm, my compact clinical vision-language model, lives under <a href="projects.html">Projects</a>.</p></div>
<section><div class="wrap"><div class="timeline">{AUDRIA}{XU}{INFOSYS}{GTU}</div></div></section>
<section><div class="wrap"><div class="sec-head"><div><h2>Publication</h2><div class="squiggle"></div></div></div>{PUB}</div></section>
{CONTACT}'''
page('research.html','Work & Research | Dev Delvadiya','Industry and research experience of Dev Delvadiya: audria.tech, Xu Lab at Carnegie Mellon, Infosys Springboard and GTU.','research.html',work)

# ---------------- projects ----------------
proj=f'''
<div class="wrap page-hero"><div class="eyebrow">03 · Projects</div><h1>Things I've built.</h1>
<p class="lede">Research projects and builds, each with the code and the honest limits.</p></div>
<section><div class="wrap">
  <div class="filters" role="group" aria-label="Filter projects"><button class="filter-btn active" data-filter="all" type="button">All</button><button class="filter-btn" data-filter="vlm" type="button">Vision-language</button><button class="filter-btn" data-filter="medical" type="button">Medical</button><button class="filter-btn" data-filter="automation" type="button">Automation</button></div>
  <div class="project-list">{proj_cards()}</div>
</div></section>
{CONTACT}'''
page('projects.html','Projects | Dev Delvadiya','Projects by Dev Delvadiya: MedOptm, brain MRI surface registration, BrainScan AI, CvT-24, fashion retrieval and workflow automation.','projects.html',proj)

# ---------------- reading ----------------
r=open(f'{SRC}/reading.html',encoding='utf-8').read()
rows=r[r.index('<div data-render="reading">'):r.index('</section>',r.index('<div data-render="reading">'))]
rows=rows[:rows.rindex('</div>\n        </div>')] if '</div>\n        </div>' in rows else rows
rows=re.sub(r'<!--.*?-->','',rows)
rows=rows+'</div>'*(rows.count('<div')-rows.count('</div>'))
rd=f'''
<div class="wrap page-hero"><div class="eyebrow">04 · Shelf</div><h1>The shelf.</h1>
<p class="lede">Books that shaped how I think and build, each with a note on how it shows up in my work.</p></div>
<section><div class="wrap">{rows}</div></section>
{CONTACT}'''
# make sure divs are balanced
if rd.count('<div')!=rd.count('</div>'):
    rd=rd.replace('<div data-render="reading">','<div data-render="reading">',1)
page('reading.html','Reading Shelf | Dev Delvadiya','The books behind the work of Dev Delvadiya, from mathematics for machine learning to large language models.','reading.html',rd)

# ---------------- about ----------------
sk=[('Languages and libraries','Python, C, CUDA C++ (basics), PyTorch, Scikit-learn, NumPy, Pandas, OpenCV, Vector databases'),
    ('Technical expertise','Deep learning (CNNs, Transformers), model development and evaluation, ML data pipelines, feature engineering, agentic AI'),
    ('Interests','World models research, medical AI, small vision-language models, LLM reasoning, automation workflows, agent development')]
skh=''.join(f'<div class="skill-group"><h3>{t}</h3><div class="chips">'+''.join(f'<span class="chip{" sage" if i==1 else ""}">{s.strip()}</span>' for s in v.split(', '))+'</div></div>' for i,(t,v) in enumerate(sk))
ab=f'''
<div class="wrap page-hero"><div class="eyebrow">05 · About</div><h1>The details.</h1>
<p class="lede">Education, skills and recognition. For the more personal side, read the <a href="index.html#letter">letter on the home page</a>.</p></div>
<section><div class="wrap">
  <div class="sec-head"><div><h2>Education</h2><div class="squiggle"></div></div></div>
  <div class="card"><div class="meta"><span>Expected June 2027</span><span>Ahmedabad</span></div><h3>Gujarat Technological University</h3><p>Bachelor of Engineering in Computer Science. CGPA 9.35.</p></div>
</div></section>
<section><div class="wrap"><div class="sec-head"><div><h2>Skills and interests</h2><div class="squiggle"></div></div></div>{skh}</div></section>
<section><div class="wrap"><div class="sec-head"><div><h2>Recognition and learning</h2><div class="squiggle"></div></div></div>{recog()}
  <div class="grid-2" style="margin-top:18px"><div class="card"><h3>Introduction to Machine Learning</h3><p>IIT Madras</p></div><div class="card"><h3>Database Management Systems</h3><p>IIT Kharagpur</p></div></div>
</div></section>
{CONTACT}'''
page('about.html','About | Dev Delvadiya','Education, skills and recognition of Dev Delvadiya, an AI engineer and researcher at Gujarat Technological University.','about.html',ab)

# ---------------- case studies ----------------
for fn in ['project-medoptm','project-brain-mri','project-cvt24','project-fashion-retrieval','project-brainscan-ai']:
    t=open(f'{SRC}/{fn}.html',encoding='utf-8').read()
    h=t[:t.index('<link rel="stylesheet" href="style.css">')]
    h=re.sub(r'\n  <!-- Instant Theme Initializer.*?</script>','''
  <script>
    (function () { try { localStorage.removeItem('dev_portfolio_theme'); } catch (e) {} document.documentElement.setAttribute('data-theme', 'bright'); })();
  </script>''',h,flags=re.S) if 'Instant Theme' in h else h
    h+='<link rel="stylesheet" href="style.css">\n</head>\n<body>\n'
    main=t[t.index('<main>')+len('<main>'):t.index('</main>')]
    main=main.replace('assets/cv.pdf',DRIVE).replace('Download CV (PDF) ↗','View Resume ↗')
    main=re.sub(r'\s*<a class="pub-btn" href="assets/delvadiya_icmlde2025.bib" download>\[BibTeX .bib\]</a>','',main)
    if fn=='project-medoptm':
        main=main.replace('Quantitative results are being finalized.','Baseline comparisons are being finalized.')
    open(f'{OUT}/{fn}.html','w',encoding='utf-8').write(h+shell_open('projects.html')+main+FOOT)
print('built')
