#!/usr/bin/env python3
"""Simulador exclusivamente local, sem acesso a Kubernetes ou rede."""
import argparse, datetime as dt, json, os, random, re, sys, uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CASES=ROOT/'incident-lab/scenarios'
SESSIONS=ROOT/'.local/incidents'

def read(p): return json.loads(p.read_text())
def write(p,d):
    p.parent.mkdir(parents=True,exist_ok=True,mode=0o700); tmp=p.with_suffix('.tmp'); tmp.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n'); tmp.replace(p)
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def all_cases(): return [read(p) for p in sorted(CASES.glob('INC-*.json'))]
def get_case(i):
    if not re.fullmatch(r'INC-\d{3}',i): raise ValueError('ID inválido')
    return {**read(CASES/(i+'.json')),**read(ROOT/'incident-lab/solutions'/(i+'.json'))}
def session_path(i):
    if not re.fullmatch('[a-f0-9]{32}',i): raise ValueError('Sessão inválida')
    return SESSIONS/(i+'.json')
def get_session(i=None):
    if i is None: i=(SESSIONS/'current').read_text().strip()
    p=session_path(i); return p,read(p)
def start(case):
    id=uuid.uuid4().hex; p=session_path(id)
    d={'session':id,'case':case['id'],'started':now(),'history':[],'revealed':False,'closed':False,'diagnosis':'','mitigation':''}; write(p,d); (SESSIONS/'current').write_text(id); print('Sessão:',id); display(case); return id

def display(c):
    print(f"{c['id']} | {c['level']} | {c['title']}\nAlerta: {c['alert']}\nImpacto simulado: {c['impact']}\nObjetivo: {c['objective']}\nEvidências disponíveis: {len(c['evidence'])}. Use evidence 1, evidence 2...\nRegistre diagnóstico e mitigação antes de verify.")
def evaluate(c,d):
    text=(d['diagnosis']+' '+d['mitigation']).casefold()
    found=[k for k in c['keywords'] if k.casefold() in text]
    return {'matched':len(found),'total':len(c['keywords']),'complete':len(found)==len(c['keywords']),'note':'Avaliação didática por termos, não prova de saúde nem de correção técnica.'}

def main(argv=None):
    os.umask(0o077)
    p=argparse.ArgumentParser(description='Incident Lab: exercícios sintéticos offline, sem mutação da infraestrutura.')
    p.add_argument('--session',help='ID de uma sessão existente (padrão: última)')
    sub=p.add_subparsers(dest='action',required=True)
    for x in ('list','random','hint','solution','verify','report','close','recover','status'): sub.add_parser(x)
    sh=sub.add_parser('show'); sh.add_argument('case')
    e=sub.add_parser('evidence'); e.add_argument('index',type=int)
    d=sub.add_parser('diagnosis'); d.add_argument('text')
    m=sub.add_parser('mitigation'); m.add_argument('text')
    a=p.parse_args(argv)
    if a.action=='list':
        for c in all_cases(): print(c['id'],c['level'],c['title'])
        return 0
    if a.action=='show': start(get_case(a.case)); return 0
    if a.action=='random': start(random.choice(all_cases())); return 0
    path,d=get_session(a.session); c=get_case(d['case']); act=a.action
    if act=='status': display(c); print('Encerrada:',d['closed']); return 0
    if act=='report':
        # Não revela solução automaticamente; guarda somente o que o estudante registrou.
        p=ROOT/'reports/incidents'/('session-'+d['session']+'.json'); write(p,d); print(p); return 0
    if act=='recover':
        # Restaura apenas a sessão sintética por meio de uma nova sessão; preserva histórico.
        start(c); return 0
    if d['closed']: raise ValueError('Sessão encerrada; utilize recover ou selecione novo caso')
    if act=='evidence':
        if not 1<=a.index<=len(c['evidence']): raise ValueError('Índice inválido')
        print(c['evidence'][a.index-1]); d['history'].append({'action':act,'index':a.index,'at':now()})
    elif act=='hint':
        i=min(sum(h['action']=='hint' for h in d['history']),len(c['hints'])-1); print(c['hints'][i]); d['history'].append({'action':act,'at':now()})
    elif act=='solution': print(c['solution']); print('Recuperação esperada (simulada):',c['recovery']); d['revealed']=True
    elif act in ('diagnosis','mitigation'): d[act]=a.text[:4000]; print('Registro salvo.')
    elif act=='verify':
        r=evaluate(c,d); print(r['note']); print(f"Termos esperados identificados: {r['matched']}/{r['total']}. Consulte solução para avaliação qualitativa."); d['evaluation']=r
    elif act=='close': d['closed']=True; d['ended']=now(); print('Sessão encerrada. Exporte com report.')
    write(path,d); return 0

if __name__=='__main__':
    try: sys.exit(main())
    except (ValueError,OSError,KeyError) as e: print('Não foi possível concluir:',type(e).__name__,file=sys.stderr); sys.exit(2)
