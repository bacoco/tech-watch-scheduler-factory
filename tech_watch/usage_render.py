"""Readable usage and discovery views; the complete evidence stays in JSON."""
import json


def render_usage(p):
    u, d = p['usage'], p['discovery']
    lines = ['# Usages qui pilotent la veille', '',
             'Le code vérifie la faisabilité ; il ne définit pas seul la pertinence.',
             f"Finalité : {u['watch_purpose']}", f"Valeur : {u['value_delivered']}",
             f"Publics : {', '.join(u['audiences'])}",
             f"Information à livrer : {u['information_output']}"]
    for j in u['journeys']:
        lines += ['', f"## {j['id']} — {j['actor']}", f"But : {j['goal']}",
                  f"Parcours : {j['workflow']}", f"Statut : {j['status']}",
                  'Difficultés : ' + '; '.join(j['pain_points']),
                  'Réussite : ' + '; '.join(j['success_criteria']),
                  'Preuves documentaires : ' + ', '.join(j['evidence_ids']),
                  'Observations directes autorisées : ' + ('; '.join(j['observation_refs']) or 'aucune')]
    lines += ['', '## Limites de connaissance des usages', *u['limits'], '',
              'Un usage documenté ou inféré ne constitue pas une observation terrain.',
              'Une information métier pertinente ne nécessite aucun fichier de code à changer.']
    research = ['# Recherche externe de cadrage', '',
                '**SYNTHÉTIQUE — aucune recherche réelle**' if d['synthetic'] else
                'Déclarations et traces de l’agent ; validation structurelle, pas certification.',
                f"Statut : {d['status']} — {d['started_at']} → {d['finished_at']}",
                d['scope'], 'Ne vaut ni T0 réalisé ni recherche future exécutée.', '',
                '## Recherches réellement consignées (aperçu, 12 maximum)']
    for s in d['searches'][:12]:
        research += [f"- {s['phase']} : {s['query']} — {s['outcome']}",
                     f"  Motif : {s['reason']} ; trace : {s['trace']}"]
    research += ['', '## Sources (aperçu, 12 maximum)']
    for s in d['sources'][:12]:
        research += [f"- {s['id']} / {s['status']} / {s['origin']} : {s['url']}",
                     f"  {s['finding']} Limites : {s['limitations']}"]
    research += ['', '## Conclusions liées aux usages']
    for c in d['conclusions']:
        research += [f"- {c['usage_id']} / {c['decision']} : {c['consequence']}"]
    research += ['', '## Directions découvertes']
    research += [f"- {n['direction']} : {n['why']}" for n in d['new_directions']]
    research += ['', '## Arrêt et limites', d['stop_reason'], *d['blocking_gaps'], '',
                 'Le journal intégral, les sources et leurs relations sont dans `discovery.json`.']
    return {'USAGES.md': '\n'.join(lines) + '\n',
            'RECHERCHE-INITIALE.md': '\n'.join(research) + '\n',
            'discovery.json': json.dumps(d, ensure_ascii=False, sort_keys=True) + '\n'}
