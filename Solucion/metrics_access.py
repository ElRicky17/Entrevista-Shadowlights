#!/usr/bin/env python3
import argparse
import duckdb
import json
import datetime

def compute_metrics(con, start, end):
    q = f"""
    SELECT
      SUM(spend) AS spend,
      SUM(conversions) AS conversions,
      SUM(conversions * 100.0) AS revenue
    FROM ads_spend
    WHERE date BETWEEN DATE '{start}' AND DATE '{end}'
    """
    row = con.execute(q).fetchone()
    spend = float(row[0] or 0.0)
    conv = int(row[1] or 0)
    revenue = float(row[2] or 0.0)
    cac = round(spend / conv, 2) if conv else None
    roas = round(revenue / spend, 2) if spend else None
    return {
        "start": start,
        "end": end,
        "spend": round(spend, 2),
        "conversions": conv,
        "revenue": round(revenue, 2),
        "CAC": cac,
        "ROAS": roas
    }

def pct_change(new, old):
    if old is None or old == 0:
        return None
    return round(((new - old) / old) * 100, 2)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dbpath", default="ads_warehouse.duckdb")
    p.add_argument("--start", type=str, help="YYYY-MM-DD")
    p.add_argument("--end", type=str, help="YYYY-MM-DD")
    p.add_argument("--compare-last30", action="store_true", help="Compare last 30 days vs prior 30 days (relative to data max date)")
    p.add_argument("--output", type=str, help="Write JSON output to file")
    args = p.parse_args()

    con = duckdb.connect(args.dbpath)

    if args.compare_last30:
        max_date_row = con.execute("SELECT MAX(date) FROM ads_spend").fetchone()
        max_date = max_date_row[0]
        if isinstance(max_date, str):
            max_date = datetime.date.fromisoformat(max_date)
        last_end = max_date
        last_start = last_end - datetime.timedelta(days=29)
        prior_end = last_start - datetime.timedelta(days=1)
        prior_start = prior_end - datetime.timedelta(days=29)

        last = compute_metrics(con, last_start.isoformat(), last_end.isoformat())
        prior = compute_metrics(con, prior_start.isoformat(), prior_end.isoformat())

        deltas = {
            "spend_delta_pct": pct_change(last["spend"], prior["spend"]),
            "conversions_delta_pct": pct_change(last["conversions"], prior["conversions"]),
            "CAC_delta_pct": pct_change(last["CAC"], prior["CAC"]) if (last["CAC"] is not None and prior["CAC"] is not None) else None,
            "ROAS_delta_pct": pct_change(last["ROAS"], prior["ROAS"]) if (last["ROAS"] is not None and prior["ROAS"] is not None) else None
        }

        out = {"last": last, "prior": prior, "deltas": deltas}

    elif args.start and args.end:
        out = compute_metrics(con, args.start, args.end)
    else:
        p.error("Provide --start and --end OR --compare-last30")

    json_out = json.dumps(out, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(json_out)

    print(json_out)

if __name__ == "__main__":
    main()
