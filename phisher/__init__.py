from phisher import engine

def run(args):
    phisher_engine = engine.Engine(args.Visits, args.Downloads, args.Blocked)
    if args.parse:
        phisher_engine.parse_results(args.parse)
    if args.show:
        phisher_engine.show_results()
    if args.backup:
        phisher_engine.backup_results(args.backup)
    return
