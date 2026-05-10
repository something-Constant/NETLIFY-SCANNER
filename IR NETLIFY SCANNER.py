import subprocess
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter
import sys

# --- CONFIGURATION ---
BRAND_NAME = "IR_NETLIFY"
TELEGRAM_CH = "https://t.me/IR_NETLIFY"

domains = [
    "helm.sh", "keda.sh", "rook.io", "istio.io", "cilium.io", "fluxcd.io",
    "harbor.io", "calico.org", "linkerd.io", "openebs.io", "tekton.dev",
    "longhorn.io", "blog.helm.sh", "docs.helm.sh", "crossplane.io",
    "kubernetes.io", "kubebuilder.io", "cert-manager.io", "letsencrypt.org",
    "kind.sigs.k8s.io", "kops.sigs.k8s.io", "krew.sigs.k8s.io",
    "kwok.sigs.k8s.io", "kueue.sigs.k8s.io", "jobset.sigs.k8s.io",
    "kaniko.sigs.k8s.io", "minikube.sigs.k8s.io", "operatorframework.io",
    "container.sigs.k8s.io", "kustomize.sigs.k8s.io", "argo-cd.readthedocs.io",
    "cluster-api.sigs.k8s.io", "descheduler.sigs.k8s.io", "gateway-api.sigs.k8s.io",
    "external-dns.sigs.k8s.io", "service-apis.sigs.k8s.io", "image-builder.sigs.k8s.io",
    "kubectl.docs.kubernetes.io", "metrics-server.sigs.k8s.io",
    "scheduler-plugins.sigs.k8s.io", "controller-runtime.sigs.k8s.io",
    "prometheus-operator.sigs.k8s.io", "node-feature-discovery.sigs.k8s.io",
    "hierarchical-namespaces.sigs.k8s.io", "secrets-store-csi-driver.sigs.k8s.io",
    "security-profiles-operator.sigs.k8s.io", "cluster-proportional-autoscaler.sigs.k8s.io"
]

ips = list(set([
    "50.7.5.83", "50.7.87.2", "50.7.87.3", "50.7.87.4", "50.7.87.5",
    "75.2.60.5", "5.9.210.65", "5.9.248.38", "5.9.248.39", "50.7.85.43",
    "144.76.1.88", "104.21.33.34", "188.114.98.0", "188.114.99.0",
    "3.162.247.34", "3.162.247.38", "3.162.247.45", "3.162.247.77",
    "3.33.186.135", "63.176.8.218", "74.91.29.207", "85.10.207.48",
    "85.10.207.51", "88.99.249.74", "94.130.33.41", "95.216.69.37",
    "104.198.14.52", "104.21.63.202", "148.251.65.39", "15.197.167.90",
    "170.205.28.40", "172.67.150.14", "188.40.147.23", "188.40.181.55",
    "204.12.196.34", "204.12.196.39", "34.194.97.138", "35.157.26.135",
    "40.160.22.170", "52.222.214.38", "52.222.214.99", "54.232.119.62",
    "65.109.34.234", "69.197.138.87", "83.136.211.95", "85.158.145.74",
    "91.99.175.105", "94.130.70.160", "138.201.54.122", "142.54.178.211",
    "142.54.178.215", "142.54.189.111", "172.67.158.128", "178.63.240.111",
    "184.171.110.10", "185.134.23.172", "188.40.254.151", "204.12.192.223",
    "204.12.223.183", "52.222.214.108", "52.222.214.124", "63.141.252.203",
    "63.141.252.207", "69.197.146.178", "69.197.146.183", "136.243.128.223",
    "168.119.202.236", "173.208.128.143", "50.7.5.85", "76.76.21.112",
    "94.130.13.19", "94.130.50.12", "198.252.206.1", "104.18.25.196",
    "149.154.167.99", "178.22.122.101", "204.79.197.220", "216.239.38.120"
]))

MAX_THREADS = 80

# --- UI STYLING ---
if os.name == 'nt': os.system('color')

C_CYAN = "\033[96m"
C_MAGENTA = "\033[95m"
C_YELLOW = "\033[93m"
C_GREEN = "\033[92m"
C_RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

def show_header():
    print(f"\n{BOLD}{C_CYAN}    ▶ {BRAND_NAME} SCANNER v2.0{RESET}")
    print(f"{C_CYAN}    {'-'*30}{RESET}")
    print(f"    {BOLD}{C_YELLOW}Channel:{RESET} {TELEGRAM_CH}\n")

def show_footer():
    print(f"\n{C_CYAN}{'='*60}{RESET}")
    print(f"{BOLD}{C_GREEN}    SCAN FINISHED SUCCESSFULLY!{RESET}")
    print(f"    Follow us: {TELEGRAM_CH}")
    print(f"{C_CYAN}{'='*60}{RESET}")

# --- CORE LOGIC ---
def check_pair(ip, domain):
    cmd = ["curl", "-I", "-s", "--max-time", "3", f"https://{domain}", "--resolve", f"{domain}:443:{ip}"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        output = result.stdout + result.stderr
        if "200 OK" in result.stdout: return ip, domain, "OK"
        if "CRYPT_E_REVOCATION_OFFLINE" in output: return ip, domain, "Revocation"
    except: pass
    return None

def main():
    show_header()
    
    tasks = [(ip, domain) for ip in ips for domain in domains]
    total = len(tasks)
    completed = 0
    found_count = 0
    ip_stats = Counter()

    with open("scan_results.txt", "w") as f:
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            try:
                futures = {executor.submit(check_pair, ip, domain): (ip, domain) for ip, domain in tasks}
                for future in as_completed(futures):
                    res = future.result()
                    completed += 1
                    
                    # Modern Progress Line
                    sys.stdout.write(f"\r{BOLD}{C_MAGENTA}  [PROGRESS]{RESET} {completed}/{total} | {BOLD}{C_GREEN}FOUND: {found_count}{RESET}  ")
                    sys.stdout.flush()

                    if res:
                        ip, dom, status = res
                        found_count += 1
                        ip_stats[ip] += 1
                        sys.stdout.write(f"\r{' ' * 80}\r") # Clear current line
                        status_color = C_GREEN if status == "OK" else C_RED
                        print(f"  {C_GREEN}✔{RESET} {BOLD}{ip:<15}{RESET} → {dom:<25} ({status_color}{status}{RESET})")
                        f.write(f"{ip} {dom} {status}\n")
                        f.flush()
            except KeyboardInterrupt:
                print(f"\n\n{C_RED}[!] Operation cancelled by user.{RESET}")
                executor.shutdown(wait=False)

    if found_count > 0:
        top_ip = ip_stats.most_common(1)[0]
        print(f"\n  {BOLD}{C_YELLOW}STATS:{RESET} Top IP: {C_GREEN}{top_ip[0]}{RESET} ({top_ip[1]} hits)")
    
    show_footer()
    if os.name == 'nt': input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
