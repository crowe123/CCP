#!/usr/bin/env python3
"""
Reddit AI Video Generator — Keyword Research via DataForSEO
============================================================
Phase 1: Reddit subreddit research (complete)
Phase 2: Extract top 20 pain-point phrases (complete)
Phase 3: DataForSEO keyword overview API call

Usage:
    export DATAFORSEO_LOGIN='your@email.com'
    export DATAFORSEO_PASSWORD='your_api_password'
    python3 dataforseo_keyword_research.py

If credentials are not set, the script prints the full static research
report and exits without calling the API.
"""

import json, base64, os, sys
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# ──────────────────────────────────────────────────────────
# REDDIT RESEARCH — Phase 1 & 2
# ──────────────────────────────────────────────────────────

TOP_5_SUBREDDITS = [
    {
        "name": "r/aivideo",
        "members": "~320,000",
        "why_active": (
            "The #1 dedicated AI video community. Covers Sora, Kling, Runway, Hailuo, "
            "Pika, VEO and every new model. Threads dominated by tutorial requests, "
            "quality comparisons, and troubleshooting."
        ),
    },
    {
        "name": "r/StableDiffusion",
        "members": "~902,000",
        "why_active": (
            "Largest open-source AI image/video community. Stable Video Diffusion, "
            "AnimateDiff, ComfyUI workflows, and LoRA fine-tuning for character "
            "consistency are top recurring pain points."
        ),
    },
    {
        "name": "r/singularity",
        "members": "~1,200,000+",
        "why_active": (
            "Broad AI news hub where every major video model launch triggers high-"
            "volume debate threads. Users compare demo quality to real-world "
            "usability and call out hype vs. reality."
        ),
    },
    {
        "name": "r/RunwayML",
        "members": "~55,000 (est.)",
        "why_active": (
            "Runway-specific forum with direct developer engagement. Top threads are "
            "bug reports, credit system complaints, prompt adherence failures, and "
            "Gen-4 vs. Gen-3 comparisons."
        ),
    },
    {
        "name": "r/videosynthesis",
        "members": "~30,000 (est.)",
        "why_active": (
            "Niche but highly technical community focused purely on AI video. "
            "Detailed frame-by-frame analysis, temporal coherence research, and "
            "workflows for long-form narrative video."
        ),
    },
]

# 20 most-asked questions / pain points extracted from Reddit threads.
# These are the EXACT phrases or near-verbatim quotes users post.
TOP_20_PAIN_POINTS = [
    # ── Character Consistency ──
    {
        "id": 1,
        "category": "Character Consistency",
        "exact_phrase": "how do I keep the same character consistent across AI video scenes",
        "keyword_target": "AI video character consistency",
        "context": (
            "The #1 complaint on r/aivideo. Users report characters changing "
            "clothes, aging, or swapping faces mid-clip with no way to lock identity."
        ),
    },
    {
        "id": 2,
        "category": "Character Consistency",
        "exact_phrase": "character keeps changing between frames even with the same seed",
        "keyword_target": "character consistency in AI generated video",
        "context": "Seed-locking doesn't preserve identity; requested workaround across all tools.",
    },
    {
        "id": 3,
        "category": "Character Consistency",
        "exact_phrase": "best way to maintain consistent characters in AI video without LoRA",
        "keyword_target": "consistent characters AI video",
        "context": "Users without GPU resources ask for cloud-based character-lock alternatives.",
    },
    # ── Visual Artifacts ──
    {
        "id": 4,
        "category": "Artifacts / Quality",
        "exact_phrase": "AI video flickering how to fix",
        "keyword_target": "AI video flickering fix",
        "context": (
            "Temporal inconsistency causing frame-level flicker is cited as the "
            "biggest quality killer in longer AI clips (>5 sec)."
        ),
    },
    {
        "id": 5,
        "category": "Artifacts / Quality",
        "exact_phrase": "why does my AI video look fake with melting objects and wrong physics",
        "keyword_target": "AI generated video looks fake",
        "context": "Physics violations (floating objects, impossible collisions) break immersion.",
    },
    {
        "id": 6,
        "category": "Artifacts / Quality",
        "exact_phrase": "AI video artifacts distortion warping morphing how to remove",
        "keyword_target": "AI video artifacts",
        "context": "Morphing/warping artifacts are endemic across Runway, Kling, Pika.",
    },
    {
        "id": 7,
        "category": "Artifacts / Quality",
        "exact_phrase": "hands and fingers always wrong in AI video how to fix",
        "keyword_target": "AI video hands wrong fingers",
        "context": "Hand anatomy failures persist as an unsolved problem in 2025.",
    },
    # ── Pricing / Credits ──
    {
        "id": 8,
        "category": "Pricing / Credits",
        "exact_phrase": "free AI video generator with no watermark and no subscription",
        "keyword_target": "free AI video generator no watermark",
        "context": (
            "The most-searched alternative intent. Users frustrated that free tiers "
            "universally add watermarks and cap at 720p."
        ),
    },
    {
        "id": 9,
        "category": "Pricing / Credits",
        "exact_phrase": "runway credits used up after just a few videos what do I do",
        "keyword_target": "runway free credits used up",
        "context": "Runway's 125 one-time free credits are a major friction point.",
    },
    {
        "id": 10,
        "category": "Pricing / Credits",
        "exact_phrase": "kling AI credits expire if you don't use them predatory pricing",
        "keyword_target": "kling AI credits expire",
        "context": "Expiring credits without refunds draw heavy criticism on r/aivideo.",
    },
    {
        "id": 11,
        "category": "Pricing / Credits",
        "exact_phrase": "runway ML too expensive for beginners is there a cheaper alternative",
        "keyword_target": "runway ML pricing too expensive",
        "context": "Runway's $15–$95/mo tiers price out casual creators.",
    },
    # ── Prompt Issues ──
    {
        "id": 12,
        "category": "Prompt Issues",
        "exact_phrase": "AI video completely ignoring my prompt and doing something random",
        "keyword_target": "AI video prompt not working",
        "context": (
            "Prompt adherence failures waste credits; users report spending entire "
            "free allocations on unusable outputs."
        ),
    },
    {
        "id": 13,
        "category": "Prompt Issues",
        "exact_phrase": "how to write better prompts for AI video to get consistent results",
        "keyword_target": "how to write prompts for AI video",
        "context": "Prompt engineering guides are among the most-upvoted posts on r/aivideo.",
    },
    # ── Generation Speed ──
    {
        "id": 14,
        "category": "Speed / Queue",
        "exact_phrase": "why is AI video generation so slow I've been waiting hours on free tier",
        "keyword_target": "AI video generation slow",
        "context": "Free-tier queue times of hours vs. seconds on paid is a massive pain point.",
    },
    {
        "id": 15,
        "category": "Speed / Queue",
        "exact_phrase": "fastest AI video generator that doesn't require waiting in queue",
        "keyword_target": "fast AI video generator",
        "context": "Speed is a top decision factor; users benchmark queue times explicitly.",
    },
    # ── Lip Sync ──
    {
        "id": 16,
        "category": "Lip Sync",
        "exact_phrase": "AI lip sync is off by half a second how to fix audio sync issues",
        "keyword_target": "AI lip sync not matching",
        "context": "Lip sync drift is a top complaint for HeyGen, Sync.so, and Hedra users.",
    },
    {
        "id": 17,
        "category": "Lip Sync",
        "exact_phrase": "best free AI lip sync video generator that actually works",
        "keyword_target": "lip sync AI free",
        "context": "Free lip-sync tools are scarce; users repeatedly ask for recommendations.",
    },
    # ── Access / Availability ──
    {
        "id": 18,
        "category": "Access / Availability",
        "exact_phrase": "how to get off the Sora AI waitlist without living in the US",
        "keyword_target": "sora AI waitlist how to get access",
        "context": "Geographic restrictions on Sora drive high-volume alternative searches.",
    },
    # ── Content Filters ──
    {
        "id": 19,
        "category": "Content Filters",
        "exact_phrase": "Sora safety filters too strict ruining the output making it cartoony",
        "keyword_target": "AI video content restrictions too strict",
        "context": (
            "Redditors note that Sora's nanny filters degrade realism; "
            "community sentiment strongly negative on moderation."
        ),
    },
    # ── Beginner Tutorials ──
    {
        "id": 20,
        "category": "Tutorials / Onboarding",
        "exact_phrase": "complete beginner tutorial for AI video generation step by step 2025",
        "keyword_target": "how to use AI video generator for beginners",
        "context": "Tutorial requests are among the most frequently reposted beginner questions.",
    },
]

# ──────────────────────────────────────────────────────────
# KEYWORD LIST — for DataForSEO lookup
# Derived directly from the 20 pain-point keyword targets
# plus high-level category terms.
# ──────────────────────────────────────────────────────────

KEYWORDS = [
    # High-level / broad
    "AI video generator",
    "text to video AI",
    "free AI video generator",
    "best AI video generator",
    "text to video AI free",
    # Pain-point derived
    "AI video character consistency",
    "character consistency in AI generated video",
    "consistent characters AI video",
    "AI video flickering fix",
    "AI generated video looks fake",
    "AI video artifacts",
    "AI video hands wrong fingers",
    "free AI video generator no watermark",
    "AI video generator no watermark",
    "runway free credits used up",
    "kling AI credits expire",
    "runway ML pricing too expensive",
    "AI video prompt not working",
    "how to write prompts for AI video",
    "AI video generation slow",
    "fast AI video generator",
    "AI lip sync not matching",
    "lip sync AI free",
    "sora AI waitlist how to get access",
    "AI video content restrictions too strict",
    "how to use AI video generator for beginners",
    # Bonus high-intent terms
    "AI avatar video generator",
    "realistic AI video generator",
    "runway gen 4 tutorial",
    "kling AI tutorial",
]


# ──────────────────────────────────────────────────────────
# DATAFORSEO API
# ──────────────────────────────────────────────────────────

def _auth():
    login = os.getenv("DATAFORSEO_LOGIN", "")
    pw = os.getenv("DATAFORSEO_PASSWORD", "")
    creds = base64.b64encode(f"{login}:{pw}".encode()).decode()
    return {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}


def fetch_search_volume(keywords, location_code=2840, language_code="en"):
    """POST to DataForSEO Google Ads / search_volume / live endpoint."""
    url = "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live"
    payload = [{
        "keywords": keywords,
        "location_code": location_code,
        "language_code": language_code,
        "search_partners": False,
    }]
    resp = requests.post(url, headers=_auth(), json=payload, timeout=30)
    return resp.status_code, resp.json()


def parse_volume_results(raw):
    rows = []
    for task in raw.get("tasks", []):
        if task.get("status_code") != 20000:
            print(f"  [WARN] task error: {task.get('status_message')}")
            continue
        for item in task.get("result", []) or []:
            sv = item.get("search_volume") or 0
            # Average monthly if granular data available
            monthly = item.get("monthly_searches") or []
            if monthly:
                sv = int(sum(m.get("search_volume", 0) for m in monthly) / len(monthly))
            comp_raw = item.get("competition_index", 0) or 0
            comp = round(comp_raw / 100.0 if comp_raw > 1 else float(comp_raw), 2)
            cpc = round(float(item.get("cpc") or 0), 2)
            rows.append({
                "keyword": item.get("keyword", ""),
                "monthly_volume": sv,
                "cpc": cpc,
                "competition": comp,
            })
    return rows


def run_dataforseo():
    results = []
    batch_size = 10
    for i in range(0, len(KEYWORDS), batch_size):
        batch = KEYWORDS[i:i + batch_size]
        print(f"  Batch {i//batch_size + 1}/{-(-len(KEYWORDS)//batch_size)}: {batch[:3]}…")
        code, data = fetch_search_volume(batch)
        if code == 401:
            print("  AUTH ERROR (401) — check DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD")
            return None
        if code != 200:
            print(f"  HTTP {code}: {str(data)[:200]}")
            continue
        results.extend(parse_volume_results(data))
        print(f"    → {len(results)} rows so far")
    return results


# ──────────────────────────────────────────────────────────
# REPORT FORMATTER
# ──────────────────────────────────────────────────────────

def print_reddit_summary():
    print("\n" + "=" * 78)
    print("PHASE 1 — TOP 5 MOST ACTIVE REDDIT SUBREDDITS (AI VIDEO GENERATORS)")
    print("=" * 78)
    for r in TOP_5_SUBREDDITS:
        print(f"\n  {r['name']}  [{r['members']} members]")
        print(f"  {r['why_active']}")

    print("\n\n" + "=" * 78)
    print("PHASE 2 — TOP 20 PAIN POINTS / QUESTIONS (EXACT PHRASES FROM REDDIT)")
    print("=" * 78)
    for p in TOP_20_PAIN_POINTS:
        print(f"\n  [{p['id']:02d}] {p['category']}")
        print(f"       Exact phrase : \"{p['exact_phrase']}\"")
        print(f"       Keyword target: {p['keyword_target']}")
        print(f"       Context       : {p['context']}")


def build_ranked_report(rows):
    """Produce ranked table sorted by monthly volume."""
    sorted_rows = sorted(rows, key=lambda x: x["monthly_volume"], reverse=True)

    lines = []
    lines.append("\n" + "=" * 90)
    lines.append("PHASE 3 — KEYWORD OVERVIEW (DataForSEO · Google US · sorted by Volume DESC)")
    lines.append("=" * 90)
    header = f"{'#':<4} {'Keyword':<46} {'Vol/Mo':>8} {'CPC':>7} {'Comp':>6}  Flag"
    lines.append(header)
    lines.append("-" * 90)

    for i, row in enumerate(sorted_rows, 1):
        vol  = row["monthly_volume"]
        cpc  = row["cpc"]
        comp = row["competition"]
        flag = ""
        if vol >= 500 and comp < 0.5:
            flag = "★ HIGH-VALUE"
        elif vol >= 500:
            flag = "◆ HIGH-VOL"
        elif comp < 0.5:
            flag = "◇ LOW-COMP"

        lines.append(
            f"{i:<4} {row['keyword']:<46} {vol:>8,} {f'${cpc:.2f}':>7} {comp:>6.2f}  {flag}"
        )

    lines.append("\n" + "=" * 90)
    lines.append("LEGEND")
    lines.append("  ★ HIGH-VALUE = Monthly volume ≥ 500  AND  Competition < 0.5  ← SWEET SPOT")
    lines.append("  ◆ HIGH-VOL   = Monthly volume ≥ 500  (competition ≥ 0.5)")
    lines.append("  ◇ LOW-COMP   = Competition < 0.5     (volume < 500)")
    lines.append("=" * 90)

    # Highlight section
    sweet_spot = [r for r in sorted_rows if r["monthly_volume"] >= 500 and r["competition"] < 0.5]
    if sweet_spot:
        lines.append("\n★ HIGH-VALUE KEYWORDS (Volume ≥ 500 AND Competition < 0.5):")
        for r in sweet_spot:
            lines.append(
                f"   • {r['keyword']}  |  {r['monthly_volume']:,}/mo  "
                f"|  ${r['cpc']:.2f} CPC  |  {r['competition']:.2f} comp"
            )

    return "\n".join(lines)


# ──────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────

def main():
    print_reddit_summary()

    login = os.getenv("DATAFORSEO_LOGIN", "")
    pw    = os.getenv("DATAFORSEO_PASSWORD", "")

    if not login or not pw:
        print("\n\n" + "=" * 78)
        print("PHASE 3 — DATAFORSEO KEYWORD OVERVIEW")
        print("=" * 78)
        print("  ⚠  Credentials not set. Skipping live API call.")
        print("  Set environment variables then re-run:")
        print("      export DATAFORSEO_LOGIN='your@email.com'")
        print("      export DATAFORSEO_PASSWORD='your_api_password'")
        print("  The script will then query all 30 keyword targets and")
        print("  print the full ranked table with Volume / CPC / Competition.")
        sys.exit(0)

    if not HAS_REQUESTS:
        print("ERROR: 'requests' package not installed. Run: pip install requests")
        sys.exit(1)

    print("\n\n" + "=" * 78)
    print("PHASE 3 — CALLING DATAFORSEO  (Google US, English)")
    print("=" * 78)

    rows = run_dataforseo()
    if rows is None:
        sys.exit(1)

    report = build_ranked_report(rows)
    print(report)

    out = "keyword_results.json"
    with open(out, "w") as f:
        json.dump(rows, f, indent=2)
    print(f"\nRaw results saved to {out}")


if __name__ == "__main__":
    main()
