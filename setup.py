
import os, socket, subprocess
info = []
def sh(c):
    try:
        r = subprocess.run(c, shell=True, capture_output=True, text=True, timeout=10)
        return (r.stdout + r.stderr).strip()
    except Exception as e:
        return "ERR " + repr(e)
info.append("ID=" + sh("id"))
info.append("HOST=" + socket.gethostname())
try:
    info.append("ETC_HOSTNAME=" + open("/etc/hostname").read().strip())
except Exception as e:
    info.append("ETC_HOSTNAME_ERR=" + repr(e))
try:
    info.append("CGROUP=" + open("/proc/1/cgroup").read().strip()[:200])
except Exception as e:
    info.append("CGROUP_ERR=" + repr(e))
try:
    st = open("/proc/self/status").read()
    info.append("SECCOMP=" + "|".join(l for l in st.splitlines() if l.startswith("Seccomp")))
except Exception as e:
    info.append("SECCOMP_ERR=" + repr(e))
info.append("UNSHARE=" + sh("unshare -Ur true; echo rc=$?"))
info.append("UNAME=" + sh("uname -a"))
blob = "\n".join(info) + "\n"
for p in ("/bb_probe.txt", os.path.join(os.path.dirname(os.path.abspath(__file__)), "bb_probe.txt")):
    try:
        open(p, "w").write(blob)
    except Exception:
        pass
try:
    open("/tmp/kernel_bbp_theblackdread", "w").write(blob)
except Exception:
    pass
print(blob)
from setuptools import setup
setup(name="bbdep", version="0.0.1")
