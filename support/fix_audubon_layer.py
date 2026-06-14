#!/usr/bin/env python3
"""
Patch the Central Texas Plant Interactions dashboard so Audubon records are retained
as trusted broad bird-friendly profile evidence, without exploding them into false
plant x bird-group x resource direct-food rows.
"""
from __future__ import annotations
import csv
import math
import os
import re
import shutil
import zipfile
from pathlib import Path

import pandas as pd

SRC = Path('/mnt/data/ctpi/Central-Texas-Plant-Interactions-main')
OUT = Path('/mnt/data/ctpi_audubon_fixed/Central-Texas-Plant-Interactions-main')
AUD_SOURCE = 'Central Texas Bird Audubon interactions'

# Split labels found in the bad cross-product scrape, collapsed back to Audubon-style broad groups.
CANONICAL_GROUP = {
    'Buntings': 'Cardinals, Grosbeaks and Buntings',
    'Cardinals': 'Cardinals, Grosbeaks and Buntings',
    'Grosbeaks': 'Cardinals, Grosbeaks and Buntings',
    'Chickadees': 'Chickadees and Titmice',
    'Titmice': 'Chickadees and Titmice',
    'Crows': 'Crows, Magpies and Jays',
    'Jays': 'Crows, Magpies and Jays',
    'Finches': 'Finches',
    'Hummingbirds': 'Hummingbirds',
    'Mockingbirds': 'Mockingbirds and Thrashers',
    'Thrashers': 'Mockingbirds and Thrashers',
    'Nuthatches': 'Nuthatches',
    'Orioles': 'Orioles',
    'Sparrows': 'New World Sparrows',
    'Thrushes': 'Thrushes',
    'Vireos': 'Vireos',
    'Warblers': 'Wood Warblers',
    'Wood Warblers': 'Wood Warblers',
    'Waxwings': 'Waxwings',
    'Woodpeckers': 'Woodpeckers',
    'Wrens': 'Wrens',
}

NOTE = (
    'Audubon Native Plants broad May Attract profile. Trusted broad bird-friendly support; '
    'not a species-level bird x plant direct-use claim, and plant resources are not cross-multiplied by bird group.'
)


def grade_from_score(val: float, claims: float = 1) -> str:
    if claims <= 0 or val <= 0:
        return 'No verified direct records yet'
    if val >= 85:
        return 'A'
    if val >= 70:
        return 'B'
    if val >= 55:
        return 'C'
    if val >= 40:
        return 'D'
    if val >= 25:
        return 'E'
    return 'F'


def split_interaction_parts(df: pd.DataFrame, out_dir: Path, n_parts: int = 3) -> None:
    rows = len(df)
    part_size = math.ceil(rows / n_parts)
    for i in range(n_parts):
        part = df.iloc[i * part_size : (i + 1) * part_size].copy()
        part.to_csv(out_dir / f'dashboard_interactions_v0_3_part{i+1}.csv', index=False)


def calc_ecological(row: pd.Series) -> float:
    div = min(8, max(0, float(row.get('diversity', 0) or 0))) / 8 * 100
    val = (
        0.30 * float(row.get('host', 0) or 0)
        + 0.25 * float(row.get('pollinator', 0) or 0)
        + 0.20 * float(row.get('bird', 0) or 0)
        + 0.10 * float(row.get('mammal', 0) or 0)
        + 0.05 * float(row.get('other', 0) or 0)
        + 0.05 * float(row.get('season', 0) or 0)
        + 0.05 * div
    )
    return round(val, 1)


def patch_index_html(path: Path) -> None:
    html = path.read_text(encoding='utf-8')
    html = html.replace(
        "['National Audubon Society Native Plants Database','Used for broad bird-plant resource records. Broad records are scored conservatively.','https://www.audubon.org/native-plants']",
        "['National Audubon Society Native Plants Database','Used for broad Audubon Native Plants May Attract bird-family support/profile evidence. These rows are trusted broad support, not species-level direct bird-plant claims.','https://www.audubon.org/native-plants']"
    )
    html = html.replace(
        "audubon:'Broad bird-plant resource record; scored conservatively.'",
        "audubon:'Audubon Native Plants May Attract bird-family support/profile; not a species-level direct bird-plant claim.'"
    )
    html = html.replace(
        "audubon:'National Audubon Society Native Plants Database record.'",
        "audubon:'National Audubon Society Native Plants Database broad bird-family profile.'"
    )
    html = html.replace(
        "bird:['Bird direct-use score','Direct bird use only: fruit, seed, nectar, nest material, nesting substrate, cover, or roosting when sourced.']",
        "bird:['Bird use/support score','Species-level bird use records plus clearly labeled broad Audubon bird-family support. Audubon profile rows are trusted broad support, not species-level direct interaction claims.']"
    )
    marker = "function rowTable(rows){"
    helper = (
        "function animalTaxonForRow(r){return String(r.rank||'').toLowerCase()==='species'?esc(r.animal||''):''}\n"
        "function animalNameForRow(r){const n=esc(r.animal||'Unspecified');return String(r.rank||'').toLowerCase()==='species'?`<i>${n}</i>`:n}\n"
    )
    if helper.strip() not in html and marker in html:
        html = html.replace(marker, helper + marker, 1)
    html = html.replace('data-taxon="${esc(r.animal||\'\')}"', 'data-taxon="${animalTaxonForRow(r)}"')
    html = html.replace('<b><i>${esc(r.animal||\'Unspecified\')}</i></b>', '<b>${animalNameForRow(r)}</b>')
    path.write_text(html, encoding='utf-8')


def build() -> None:
    if OUT.exists():
        shutil.rmtree(OUT.parent)
    shutil.copytree(SRC, OUT)
    data_dir = OUT / 'data'

    # Use the interaction part files because index.html loads those files. Keep the full CSV consistent too.
    part_files = [data_dir / f'dashboard_interactions_v0_3_part{i}.csv' for i in (1, 2, 3)]
    interactions = pd.concat([pd.read_csv(p, dtype=str) for p in part_files], ignore_index=True)
    # Keep numeric weight usable.
    interactions['weight'] = pd.to_numeric(interactions['weight'], errors='coerce').fillna(0.0)

    aud = interactions[interactions['sources'].eq(AUD_SOURCE)].copy()
    non_aud = interactions[~interactions['sources'].eq(AUD_SOURCE)].copy()

    collapsed_rows = []
    summary_rows = []
    for plant_id, g in aud.groupby('plant_id', dropna=False):
        canonical_groups = sorted({CANONICAL_GROUP.get(str(x).strip(), str(x).strip()) for x in g['common'].dropna() if str(x).strip()})
        raw_split_groups = sorted({str(x).strip() for x in g['common'].dropna() if str(x).strip()})
        old_resources = sorted({str(x).strip() for x in g['part'].dropna() if str(x).strip()})
        summary_rows.append({
            'plant_id': plant_id,
            'old_audubon_crossproduct_rows': len(g),
            'new_audubon_profile_rows': len(canonical_groups),
            'old_split_bird_labels': '; '.join(raw_split_groups),
            'collapsed_bird_family_groups': '; '.join(canonical_groups),
            'old_cross_multiplied_resources_not_used_for_direct_claims': '; '.join(old_resources),
            'fix_note': NOTE,
        })
        for cg in canonical_groups:
            template = g.iloc[0].copy()
            template['animal'] = cg
            template['common'] = 'Audubon broad bird-family group'
            template['group'] = 'Birds'
            template['rank'] = 'broad_audubon_group'
            template['family'] = ''
            template['order'] = ''
            template['category'] = 'Broad bird habitat/resource support'
            template['raw'] = f'Audubon May Attract: {cg}'
            template['part'] = 'Audubon plant-resource profile; not bird-group-specific'
            template['stage'] = ''
            template['use'] = 'Bird-friendly profile support'
            template['evidence'] = 'D - Audubon broad bird-friendly support; not species-level direct interaction'
            template['scope'] = 'Audubon ZIP 78666 native-plant profile; broad family/guild context'
            template['weight'] = 0.07
            template['sources'] = AUD_SOURCE
            template['citations'] = 'National Audubon Society Native Plants Database'
            template['urls'] = 'https://www.audubon.org/native-plants'
            collapsed_rows.append(template.to_dict())

    aud_fixed = pd.DataFrame(collapsed_rows, columns=interactions.columns)
    fixed_interactions = pd.concat([non_aud, aud_fixed], ignore_index=True)
    # Restore original column order and sort softly by plant/group/source so detail views remain readable.
    fixed_interactions = fixed_interactions[interactions.columns]
    fixed_interactions['weight'] = pd.to_numeric(fixed_interactions['weight'], errors='coerce').fillna(0.0).round(3)

    fixed_interactions.to_csv(data_dir / 'dashboard_interactions_v0_3.csv', index=False)
    split_interaction_parts(fixed_interactions, data_dir, 3)

    # Patch plant-level public rows: claims and bird scores are corrected to reflect collapsed Audubon profile support.
    plants_path = data_dir / 'dashboard_plants_v0_3.csv'
    plants = pd.read_csv(plants_path)
    old_counts = aud.groupby('plant_id').size().rename('old_aud_rows')
    new_counts = aud_fixed.groupby('plant_id').size().rename('new_aud_rows') if not aud_fixed.empty else pd.Series(dtype=int, name='new_aud_rows')
    counts = pd.concat([old_counts, new_counts], axis=1).fillna(0).astype(int)

    bird_mask = (
        fixed_interactions['group'].astype(str).str.contains('Bird|Hummingbird', case=False, na=False)
        | fixed_interactions['sources'].astype(str).str.contains('Bird|Audubon', case=False, na=False)
    )
    bird_raw = fixed_interactions[bird_mask].groupby('plant_id')['weight'].sum()
    max_raw = max(float(bird_raw.max() or 0), 1.0)
    # Preserve the old public scale: top bird plant remains around 70, broad Audubon-only support becomes modest instead of dominant.
    bird_scores = bird_raw.apply(lambda x: round(69.6 * math.log1p(float(x)) / math.log1p(max_raw), 1))

    old_plant_scores = plants.set_index('id')['bird'].copy()
    for idx, row in plants.iterrows():
        pid = row['id']
        if pid in counts.index:
            old_n = int(counts.loc[pid, 'old_aud_rows'])
            new_n = int(counts.loc[pid, 'new_aud_rows'])
            delta = new_n - old_n
            plants.at[idx, 'claims'] = max(0, int(row['claims']) + delta)
            plants.at[idx, 'guildClaims'] = max(0, int(row['guildClaims']) + delta)
            # Sources and diversity remain source/group diversity fields; do not inflate or shrink them solely due row collapse.
        if pid in bird_scores.index:
            plants.at[idx, 'bird'] = float(bird_scores.loc[pid])
        else:
            plants.at[idx, 'bird'] = 0.0

    # Recalculate ecological score from the dashboard formula and softly adjust balanced/overall by the bird-term change.
    for idx, row in plants.iterrows():
        pid = row['id']
        old_bird = float(old_plant_scores.get(pid, 0) or 0)
        new_bird = float(plants.at[idx, 'bird'] or 0)
        old_bal = float(row.get('balanced', 0) or 0)
        old_overall = float(row.get('overall', 0) or 0)
        old_base = float(row.get('balanced_base_v0_14', old_bal) or old_bal)
        delta_component = 0.20 * (new_bird - old_bird)
        plants.at[idx, 'ecological'] = calc_ecological(plants.loc[idx])
        plants.at[idx, 'overall'] = round(max(0, min(100, old_overall + delta_component)), 1)
        plants.at[idx, 'balanced_base_v0_14'] = round(max(0, min(100, old_base + delta_component)), 1)
        plants.at[idx, 'balanced'] = round(max(0, min(100, old_bal + delta_component)), 1)
        plants.at[idx, 'ecologicalGrade'] = grade_from_score(float(plants.at[idx, 'ecological']), float(plants.at[idx, 'claims']))
        if str(row.get('layer', '')).startswith('Target'):
            plants.at[idx, 'balancedGrade'] = grade_from_score(float(plants.at[idx, 'balanced']), float(plants.at[idx, 'claims']))
            plants.at[idx, 'publicGrade'] = plants.at[idx, 'balancedGrade']
        if pid in counts.index:
            extra = ' Audubon rows were repaired in v0.3-audubon-fix: broad May Attract groups are retained as trusted profile support, not species-level direct interaction rows.'
            note = str(row.get('note', '') or '')
            if 'Audubon rows were repaired' not in note:
                plants.at[idx, 'note'] = (note + extra).strip()

    plants.to_csv(plants_path, index=False)

    # Patch dashboard source note.
    sources_path = data_dir / 'dashboard_sources_v0_3.csv'
    if sources_path.exists():
        sources = pd.read_csv(sources_path)
        m = sources['source'].astype(str).str.contains('Audubon|Bird-Interactions', case=False, na=False)
        sources.loc[m, 'notes'] = 'Audubon broad May Attract bird-family support retained as trusted profile evidence; no longer cross-multiplied into plant x bird-group x resource direct-food rows. LBJ profile terms remain broad wildlife-use profile rows.'
        sources.to_csv(sources_path, index=False)

    # Patch index copy for public wording.
    patch_index_html(OUT / 'index.html')

    # Write audit outputs.
    audit_dir = OUT / 'docs' / 'audubon_fix_v0_3'
    audit_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(summary_rows).sort_values('plant_id').to_csv(audit_dir / 'audubon_profile_row_collapse_summary.csv', index=False)
    aud.to_csv(audit_dir / 'audubon_removed_crossproduct_rows.csv', index=False)
    aud_fixed.to_csv(audit_dir / 'audubon_fixed_profile_rows.csv', index=False)

    # Before/after score summary.
    score_summary = plants[['id','name','common','layer','claims','guildClaims','speciesClaims','bird','ecological','balanced','note']].copy()
    score_summary = score_summary.merge(counts, left_on='id', right_index=True, how='inner')
    score_summary['old_bird_score_v0_3'] = score_summary['id'].map(old_plant_scores).round(1)
    score_summary['new_bird_score_audubon_fixed'] = score_summary['bird'].round(1)
    score_summary = score_summary[['id','name','common','layer','old_aud_rows','new_aud_rows','old_bird_score_v0_3','new_bird_score_audubon_fixed','claims','guildClaims','speciesClaims','ecological','balanced','note']]
    score_summary.sort_values(['old_aud_rows','name'], ascending=[False, True]).to_csv(audit_dir / 'audubon_score_changes.csv', index=False)

    readme = f"""# Audubon bird layer repair v0.3-audubon-fix

This package keeps the National Audubon Society Native Plants data, but repairs how it is represented.

## Problem fixed

The previous dashboard represented Audubon rows as plant x split bird-label x resource direct-food rows. That created rows such as a grass supporting hummingbirds through nectar when the Audubon page was only providing broad May Attract / plant-resource profile information.

## New representation

Audubon records are retained as trusted broad profile support:

- `rank = broad_audubon_group`
- `category = Broad bird habitat/resource support`
- `use = Bird-friendly profile support`
- `evidence = D - Audubon broad bird-friendly support; not species-level direct interaction`
- `weight = 0.07`

Plant resources are not cross-multiplied by bird group. Species-level bird claims still come from AvianDiet/GloBI/LBJ profile rows where present.

## Row count change

- Old Audubon cross-product rows: {len(aud):,}
- New Audubon broad profile rows: {len(aud_fixed):,}
- Rows removed from public interaction detail noise: {len(aud) - len(aud_fixed):,}
- Total interaction rows loaded by dashboard after repair: {len(fixed_interactions):,}

## Files changed

- `data/dashboard_interactions_v0_3.csv`
- `data/dashboard_interactions_v0_3_part1.csv`
- `data/dashboard_interactions_v0_3_part2.csv`
- `data/dashboard_interactions_v0_3_part3.csv`
- `data/dashboard_plants_v0_3.csv`
- `data/dashboard_sources_v0_3.csv`
- `index.html`

## Audit files

- `audubon_profile_row_collapse_summary.csv`
- `audubon_removed_crossproduct_rows.csv`
- `audubon_fixed_profile_rows.csv`
- `audubon_score_changes.csv`

## When a full re-scrape is still useful

A full Audubon re-scrape is only needed if you want exact current Audubon species-page resource labels and exact current bird-family labels for every plant. This repair is safe as a patch because it removes the false cross-product claim and keeps the Audubon data as broad trusted support.
"""
    (audit_dir / 'README.md').write_text(readme, encoding='utf-8')

    # Also export a small drop-in patch package with just changed files and audit.
    drop = Path('/mnt/data/audubon_layer_drop_in_patch')
    if drop.exists():
        shutil.rmtree(drop)
    for rel in [
        'data/dashboard_interactions_v0_3.csv',
        'data/dashboard_interactions_v0_3_part1.csv',
        'data/dashboard_interactions_v0_3_part2.csv',
        'data/dashboard_interactions_v0_3_part3.csv',
        'data/dashboard_plants_v0_3.csv',
        'data/dashboard_sources_v0_3.csv',
        'index.html',
        'docs/audubon_fix_v0_3/README.md',
        'docs/audubon_fix_v0_3/audubon_profile_row_collapse_summary.csv',
        'docs/audubon_fix_v0_3/audubon_removed_crossproduct_rows.csv',
        'docs/audubon_fix_v0_3/audubon_fixed_profile_rows.csv',
        'docs/audubon_fix_v0_3/audubon_score_changes.csv',
    ]:
        src = OUT / rel
        dst = drop / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    # Copy this script into the packages.
    shutil.copy2(Path(__file__), OUT / 'support' / 'fix_audubon_layer.py')
    (drop / 'support').mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__), drop / 'support' / 'fix_audubon_layer.py')

    for zip_path, root in [
        (Path('/mnt/data/Central-Texas-Plant-Interactions-main_audubon_fixed.zip'), OUT.parent),
        (Path('/mnt/data/audubon_layer_drop_in_patch.zip'), drop),
    ]:
        if zip_path.exists():
            zip_path.unlink()
        with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            if root == drop:
                for file in root.rglob('*'):
                    if file.is_file():
                        z.write(file, file.relative_to(root))
            else:
                for file in root.rglob('*'):
                    if file.is_file():
                        z.write(file, file.relative_to(root))

    print('Wrote full fixed project:', '/mnt/data/Central-Texas-Plant-Interactions-main_audubon_fixed.zip')
    print('Wrote drop-in patch:', '/mnt/data/audubon_layer_drop_in_patch.zip')
    print(f'Old Audubon rows: {len(aud):,}; new Audubon profile rows: {len(aud_fixed):,}; fixed interaction rows: {len(fixed_interactions):,}')


if __name__ == '__main__':
    build()
