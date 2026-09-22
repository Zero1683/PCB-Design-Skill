"""Run local regression in an explicit workspace; report skips instead of hiding them."""
import argparse,json,os,subprocess,sys,tempfile,time,unittest
from pathlib import Path


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workdir',type=Path,required=True)
    p.add_argument('--allow-skips',action='store_true',help='Diagnostic use only; recorded skips are not release coverage')
    p.add_argument('--python-only',action='store_true')
    a=p.parse_args();work=a.workdir.resolve(strict=True)
    if not work.is_dir():p.error('workdir must exist')
    os.environ['TEMP']=os.environ['TMP']=str(work);tempfile.tempdir=str(work)
    start=time.monotonic();scripts=Path(__file__).resolve().parent
    suite=unittest.defaultTestLoader.discover(str(scripts),pattern='test_*.py')
    for name,module in list(sys.modules.items()):
        if name.startswith('test_') and module is not None:setattr(module,'WORKDIR',str(work))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    node_code=None
    if not a.python_only:
        files=sorted(str(x) for x in scripts.glob('test_*.mjs') if x.name!='test_bridge.mjs')+sorted(str(x) for x in scripts.glob('test_*.cjs'))
        try:
            native_tests=subprocess.run(['node','--test',*files],cwd=scripts.parent,timeout=240,shell=False).returncode
            bridge_test=subprocess.run(['node',str(scripts/'test_bridge.mjs'),'--workdir',str(work)],cwd=scripts.parent,timeout=60,shell=False).returncode
            node_code=int(native_tests!=0 or bridge_test!=0)
        except (OSError,subprocess.TimeoutExpired) as exc:print('Node regression unavailable: '+str(exc));node_code=2
    summary={'python_tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
             'skips':[{'test':str(test),'reason':reason} for test,reason in result.skipped],
             'node_exit':node_code,'seconds':round(time.monotonic()-start,3),
             'scope':'software regression; native EDA and physical acceptance are separate'}
    print(json.dumps(summary,ensure_ascii=False))
    return int(not result.wasSuccessful() or (bool(result.skipped) and not a.allow_skips) or (not a.python_only and node_code!=0))

if __name__=='__main__':raise SystemExit(main())
