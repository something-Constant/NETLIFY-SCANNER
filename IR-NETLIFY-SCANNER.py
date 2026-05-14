import subprocess
import sys
import os
import time
from collections import Counter
from datetime import datetime
import pathlib
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    TaskProgressColumn,
    MofNCompleteColumn,
    TextColumn,
)
from rich.table import Table
from rich import box
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- CONFIGURATION ---
BRAND_NAME = "IR_NETLIFY"
TELEGRAM_CH = "https://t.me/IR_NETLIFY"

domains = [
    "helm.sh",
    "keda.sh",
    "rook.io",
    "istio.io",
    "cilium.io",
    "fluxcd.io",
    "harbor.io",
    "calico.org",
    "linkerd.io",
    "openebs.io",
    "tekton.dev",
    "longhorn.io",
    "blog.helm.sh",
    "docs.helm.sh",
    "crossplane.io",
    "kubernetes.io",
    "kubebuilder.io",
    "cert-manager.io",
    "letsencrypt.org",
    "kind.sigs.k8s.io",
    "kops.sigs.k8s.io",
    "krew.sigs.k8s.io",
    "kwok.sigs.k8s.io",
    "kueue.sigs.k8s.io",
    "jobset.sigs.k8s.io",
    "kaniko.sigs.k8s.io",
    "minikube.sigs.k8s.io",
    "operatorframework.io",
    "container.sigs.k8s.io",
    "kustomize.sigs.k8s.io",
    "argo-cd.readthedocs.io",
    "cluster-api.sigs.k8s.io",
    "descheduler.sigs.k8s.io",
    "gateway-api.sigs.k8s.io",
    "external-dns.sigs.k8s.io",
    "service-apis.sigs.k8s.io",
    "image-builder.sigs.k8s.io",
    "kubectl.docs.kubernetes.io",
    "metrics-server.sigs.k8s.io",
    "scheduler-plugins.sigs.k8s.io",
    "controller-runtime.sigs.k8s.io",
    "prometheus-operator.sigs.k8s.io",
    "node-feature-discovery.sigs.k8s.io",
    "hierarchical-namespaces.sigs.k8s.io",
    "secrets-store-csi-driver.sigs.k8s.io",
    "security-profiles-operator.sigs.k8s.io",
    "cluster-proportional-autoscaler.sigs.k8s.io",
    "static.cloudflareinsights.com",
    "security.vercel.com",
    "e7.c.lencr.org",
    "e8.c.lencr.org",
    "e9.c.lencr.org",
    "r10.c.lencr.org",
    "r11.c.lencr.org",
    "r13.c.lencr.org",
    "stg-e5.c.lencr.org",
    "stg-e7.c.lencr.org",
    "stg-e8.c.lencr.org",
    "stg-ye1.c.lencr.org",
    "stg-r11.c.lencr.org",
    "stg-ye2.c.lencr.org",
    "stg-yr2.c.lencr.org",
    "yr1.c.lencr.org",
    "ye2.c.lencr.org",
    "sourceforge.net",
    "vercel.com",
    "nextjs.org",
    "pubmed.ncbi.nlm.nih.gov",
    "link.springer.com",
    "www.sciencedirect.com",
    "www.python.org",
    "pypi.org",
    "react.dev",
    "www.certum.eu",
    "ubuntu.com",
    "www.npmjs.com",
    "jquery.com",
    "nodejs.org",
    "eslint.org",
    "jenkins.io",
    "prometheus.io",
    "opentelemetry.io",
    "envoyproxy.io",
    "etcd.io",
    "containerd.io",
    "fluentd.org",
    "keycloak.org",
    "openpolicyagent.org",
    "sigstore.dev",
    "thanos.io",
    "strimzi.io",
    "osquery.io",
    "falco.org",
    "theforeman.org",
    "rubygems.org",
    "cdnjs.com",
    "curl.se",
    "mastodon.social",
    "rust-lang.org",
    "dl.k8s.io",
    "www.nytimes.com",
    "www.ticketmaster.com",
    "vimeo.com",
    "www.airbnb.com",
    "www.pinterest.com",
    "www.buzzfeed.com",
    # Additional CNCF Graduated Projects
    "argo.io",
    "coredns.io",
    "cri-o.io",
    "dragonflydb.io",
    "emissary-ingress.io",
    "grpc.io",
    "in-toto.io",
    "jaegertracing.io",
    "knative.dev",
    "kubeedge.io",
    "kubevirt.io",
    "kyverno.io",
    "notaryproject.dev",
    "oras.land",
    "paralus.io",
    "tuf.community",
    "vitess.io",
    "wasmedge.org",
    # Additional Kubernetes SIGs
    "addon-manager.sigs.k8s.io",
    "apiserver-network-proxy.sigs.k8s.io",
    "boskos.sigs.k8s.io",
    "capabilities.sigs.k8s.io",
    "cli-utils.sigs.k8s.io",
    "cloud-provider-aws.sigs.k8s.io",
    "cloud-provider-azure.sigs.k8s.io",
    "cloud-provider-gcp.sigs.k8s.io",
    "cluster-addons.sigs.k8s.io",
    "e2e-framework.sigs.k8s.io",
    "etcdadm.sigs.k8s.io",
    "instrumentation.sigs.k8s.io",
    "k8s.io",
    "kubespray.io",
    "lwkd.sigs.k8s.io",
    "mcs-api.sigs.k8s.io",
    "multi-tenancy.sigs.k8s.io",
    "node-ipam.sigs.k8s.io",
    "pod-security.sigs.k8s.io",
    "prometheus-adapter.sigs.k8s.io",
    "provider-aws.sigs.k8s.io",
    "sig-docs.sigs.k8s.io",
    "sig-storage.sigs.k8s.io",
    "slack-infra.sigs.k8s.io",
    "structured-logging.sigs.k8s.io",
    "testing.sigs.k8s.io",
    "wg-device-management.sigs.k8s.io",
    "wg-policy.sigs.k8s.io",
    # Additional Fastly-Supported Open Source
    "debian.org",
    "gnome.org",
    "kde.org",
    "freebsd.org",
    "nginx.org",
    "apache.org",
    "mozilla.org",
    "webkit.org",
    "wordpress.org",
    "drupal.org",
    "jquerymobile.com",
    "jqueryui.com",
    "dojotoolkit.org",
    "yui.yahooapis.com",
    "mathjax.org",
    "fontawesome.com",
    "bootstrapcdn.com",
    "stackpath.bootstrapcdn.com",
    "unpkg.com",
    "jsdelivr.net",
    "pycon.org",
    "us.pycon.org",
    "pythonhosted.org",
    "readthedocs.org",
    "packagist.org",
    "getcomposer.org",
    "crates.io",
    "docs.rs",
    "golang.org",
    "go.dev",
    "pkg.go.dev",
    # Let's Encrypt Related
    "acme-v02.api.letsencrypt.org",
    "acme-staging-v02.api.letsencrypt.org",
    "r3.o.lencr.org",
    "r4.o.lencr.org",
    "x1.c.lencr.org",
    "x2.c.lencr.org",
    # Additional Infrastructure
    "www.cloudflare.com",
    "cdn.cloudflare.net",
    "ajax.googleapis.com",
    "fonts.googleapis.com",
    "fonts.gstatic.com",
    "www.gstatic.com",
    "cdn.jsdelivr.net",
    "code.jquery.com",
    "maxcdn.bootstrapcdn.com",
    "netdna.bootstrapcdn.com",
    "oss.maxcdn.com",
    "cdn.rawgit.com",
    "raw.githubusercontent.com",
    "github.io",
    "pages.github.com",
    "gitlab.io",
    "bitbucket.io",
    "netlify.app",
    "netlify.com",
    "herokuapp.com",
    "fly.dev",
    "workers.dev",
    "pages.dev",
    "r2.dev",
]

ips = list(
    set(
        [
            "50.7.5.83",
            "50.7.87.2",
            "50.7.87.3",
            "50.7.87.4",
            "50.7.87.5",
            "75.2.60.5",
            "5.9.210.65",
            "5.9.248.38",
            "5.9.248.39",
            "50.7.85.43",
            "144.76.1.88",
            "104.21.33.34",
            "188.114.98.0",
            "188.114.99.0",
            "3.162.247.34",
            "3.162.247.38",
            "3.162.247.45",
            "3.162.247.77",
            "3.33.186.135",
            "63.176.8.218",
            "74.91.29.207",
            "85.10.207.48",
            "85.10.207.51",
            "88.99.249.74",
            "94.130.33.41",
            "95.216.69.37",
            "104.198.14.52",
            "104.21.63.202",
            "148.251.65.39",
            "15.197.167.90",
            "170.205.28.40",
            "172.67.150.14",
            "188.40.147.23",
            "188.40.181.55",
            "204.12.196.34",
            "204.12.196.39",
            "34.194.97.138",
            "35.157.26.135",
            "40.160.22.170",
            "52.222.214.38",
            "52.222.214.99",
            "54.232.119.62",
            "65.109.34.234",
            "69.197.138.87",
            "83.136.211.95",
            "85.158.145.74",
            "91.99.175.105",
            "94.130.70.160",
            "138.201.54.122",
            "142.54.178.211",
            "142.54.178.215",
            "142.54.189.111",
            "172.67.158.128",
            "178.63.240.111",
            "184.171.110.10",
            "185.134.23.172",
            "188.40.254.151",
            "204.12.192.223",
            "204.12.223.183",
            "52.222.214.108",
            "52.222.214.124",
            "63.141.252.203",
            "63.141.252.207",
            "69.197.146.178",
            "69.197.146.183",
            "136.243.128.223",
            "168.119.202.236",
            "173.208.128.143",
            "50.7.5.85",
            "76.76.21.112",
            "94.130.13.19",
            "94.130.50.12",
            "198.252.206.1",
            "104.18.25.196",
            "149.154.167.99",
            "178.22.122.101",
            "204.79.197.220",
            "216.239.38.120",
            # Cloudflare CDN Edge IPs
            "104.16.0.0",
            "104.16.1.0",
            "104.16.2.0",
            "104.16.3.0",
            "104.16.4.0",
            "104.16.5.0",
            "104.16.6.0",
            "104.16.7.0",
            "104.16.8.0",
            "104.16.9.0",
            "104.16.10.0",
            "104.16.11.0",
            "104.16.12.0",
            "104.16.13.0",
            "104.16.14.0",
            "104.16.15.0",
            "104.17.0.0",
            "104.18.0.0",
            "104.18.1.0",
            "104.18.2.0",
            "104.18.32.0",
            "104.19.0.0",
            "104.20.0.0",
            "104.21.0.0",
            "104.22.0.0",
            "104.23.0.0",
            "104.24.0.0",
            "104.25.0.0",
            "104.26.0.0",
            "104.27.0.0",
            "172.64.0.0",
            "172.65.0.0",
            "172.66.0.0",
            "172.67.0.0",
            # Fastly CDN Edge IPs
            "151.101.0.0",
            "151.101.1.0",
            "151.101.2.0",
            "151.101.3.0",
            "151.101.4.0",
            "151.101.5.0",
            "151.101.6.0",
            "151.101.7.0",
            "151.101.8.0",
            "151.101.9.0",
            "151.101.16.0",
            "151.101.32.0",
            "151.101.64.0",
            "151.101.128.0",
            "199.232.0.0",
            "199.232.1.0",
            "199.232.2.0",
            "199.232.3.0",
            "199.232.4.0",
            "199.232.5.0",
            "199.232.6.0",
            "199.232.7.0",
            "199.232.8.0",
            "199.232.9.0",
            "199.232.16.0",
            "199.232.32.0",
            "199.232.64.0",
            "199.232.128.0",
            # Vercel Edge Network IPs
            "76.76.21.0",
            "76.76.21.1",
            "76.76.21.2",
            "76.76.21.3",
            "76.76.21.4",
            "76.76.21.5",
            "76.76.21.6",
            "76.76.21.7",
            "76.76.21.8",
            "76.76.21.9",
            "76.76.21.10",
            "76.76.21.21",
            "76.76.21.22",
            "76.76.21.93",
            "76.76.21.98",
            "76.76.21.123",
            # Netlify CDN IPs
            "3.70.0.0",
            "18.192.0.0",
            "18.193.0.0",
            "18.194.0.0",
            "18.195.0.0",
            "18.196.0.0",
            "18.197.0.0",
            "35.156.0.0",
            "52.58.0.0",
            "54.93.0.0",
            # GitHub Pages / GitHub CDN IPs
            "185.199.108.153",
            "185.199.109.153",
            "185.199.110.153",
            "185.199.111.153",
            "140.82.112.0",
            "140.82.113.0",
            "140.82.114.0",
            "140.82.115.0",
            "140.82.116.0",
            "140.82.117.0",
            "140.82.118.0",
            "140.82.119.0",
            # Google APIs / Fonts / GStatic
            "216.58.192.0",
            "216.58.193.0",
            "216.58.194.0",
            "216.58.195.0",
            "216.58.196.0",
            "216.58.197.0",
            "216.58.198.0",
            "216.58.199.0",
            "216.58.200.0",
            "216.58.201.0",
            "216.58.202.0",
            "216.58.203.0",
            "216.58.204.0",
            "216.58.205.0",
            "216.58.206.0",
            "216.58.207.0",
            "172.217.0.0",
            "142.250.0.0",
            "142.251.0.0",
            "74.125.0.0",
            # jsDelivr CDN
            "104.16.88.20",
            "104.16.89.20",
            "104.16.90.20",
            "104.16.91.20",
            "104.16.92.20",
            "104.16.93.20",
            "104.16.94.20",
            "104.16.95.20",
            "104.17.80.0",
            "104.17.81.0",
            "104.17.82.0",
            # unpkg CDN
            "104.16.121.0",
            "104.16.122.0",
            "104.16.123.0",
            "104.16.124.0",
            "104.16.125.0",
            # Python.org / PyPI (Fastly-backed)
            "146.75.32.0",
            "146.75.33.0",
            "146.75.34.0",
            "146.75.35.0",
            "146.75.36.0",
            "146.75.37.0",
            "146.75.38.0",
            "146.75.39.0",
            # Let's Encrypt OCSP Responders
            "23.32.3.72",
            "23.36.76.232",
            "23.36.77.232",
            "23.57.81.227",
            "23.57.82.227",
            "23.205.175.48",
            "23.205.175.49",
            # Docker Hub / Registry
            "3.216.0.0",
            "3.217.0.0",
            "3.218.0.0",
            "3.219.0.0",
            "34.192.0.0",
            "34.193.0.0",
            "34.194.0.0",
            "34.195.0.0",
            "34.196.0.0",
            "34.197.0.0",
            "34.198.0.0",
            "34.199.0.0",
            "34.200.0.0",
            "34.201.0.0",
            # NPM Registry (Fastly-backed)
            "104.16.0.0",
            "104.16.16.0",
            "104.16.32.0",
            "104.16.48.0",
            "104.16.64.0",
            "104.16.80.0",
            "104.16.96.0",
            # RubyGems (Fastly-backed)
            "151.101.192.0",
            "151.101.193.0",
            "151.101.194.0",
            "151.101.195.0",
            # Rust / crates.io (Fastly-backed)
            "151.101.196.0",
            "151.101.197.0",
            "151.101.198.0",
            "151.101.199.0",
            # Kubernetes / k8s.io
            "34.107.0.0",
            "35.227.0.0",
            "35.241.0.0",
            # Mozilla / Firefox Services (Fastly-backed)
            "13.32.0.0",
            "13.32.1.0",
            "13.32.2.0",
            "13.32.3.0",
            "13.32.4.0",
            "13.32.5.0",
            "13.32.6.0",
            "13.32.7.0",
            # Ubuntu / Canonical
            "91.189.88.0",
            "91.189.89.0",
            "91.189.90.0",
            "91.189.91.0",
            "91.189.92.0",
            "91.189.93.0",
            "91.189.94.0",
            "91.189.95.0",
            "185.125.188.0",
            "185.125.189.0",
            "185.125.190.0",
            # Debian
            "128.31.0.0",
            "130.89.148.0",
            "130.89.149.0",
            "149.20.20.0",
            "149.20.21.0",
            # Apache Foundation
            "40.79.78.0",
            "95.216.0.0",
            "95.216.1.0",
            "140.211.11.0",
            "195.154.0.0",
            # WordPress.org / Drupal.org
            "198.143.164.0",
            "198.143.165.0",
            "198.143.166.0",
            "198.143.167.0",
            # SourceForge
            "204.68.111.0",
            "204.68.112.0",
            # Stack Overflow / Stack Exchange
            "151.101.0.0",
            "151.101.64.0",
            "151.101.128.0",
            "151.101.192.0",
            # ReadTheDocs
            "104.17.32.0",
            "104.17.33.0",
            "104.17.34.0",
            "104.17.35.0",
            # Heroku
            "54.243.0.0",
            "54.243.1.0",
            "50.19.0.0",
            "50.19.1.0",
            "23.21.0.0",
            "23.21.1.0",
            # Fly.io
            "66.241.124.0",
            "66.241.125.0",
            "149.248.192.0",
            "149.248.193.0",
            # Cloudflare Workers / Pages
            "2a06:98c0:3600::0",
            "2a06:98c1:3600::0",
            "2a06:98c1:3601::0",
            "2a06:98c1:3602::0",
        ]
    )
)


MAX_THREADS = 50
DEFAULT_TIMEOUT = 3
timestamp = datetime.now().strftime("%m.%d_%H.%M")
DEFAULT_OUTPUT_DIR = "results_" + timestamp


# --- UI STYLING ---
if os.name == "nt":
    os.system("color")

C_CYAN = "\033[96m"
C_MAGENTA = "\033[95m"
C_YELLOW = "\033[93m"
C_GREEN = "\033[92m"
C_RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def show_header():
    print(f"\n{BOLD}{C_CYAN}    ▶ {BRAND_NAME} SCANNER v2.1.0{RESET}")
    print(f"{C_CYAN}    {'-' * 30}{RESET}")
    print(f"    {BOLD}{C_YELLOW}Channel:{RESET} {TELEGRAM_CH}\n")


def show_footer():
    print(f"\n\n{C_CYAN}{'=' * 60}{RESET}")
    print(f"{BOLD}{C_GREEN}    SCAN FINISHED SUCCESSFULLY!{RESET}")
    print(f"    Follow us: {TELEGRAM_CH}")
    print(f"{C_CYAN}{'=' * 60}{RESET}")


# --- CORE LOGIC ---
def check_pair(ip, domain):
    cmd = [
        "curl",
        "-I",
        "-s",
        "--max-time",
        "3",
        f"https://{domain}",
        "--resolve",
        f"{domain}:443:{ip}",
    ]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        output = result.stdout + result.stderr
        if "200 OK" in result.stdout:
            return ip, domain, "OK"
        if "CRYPT_E_REVOCATION_OFFLINE" in output:
            return ip, domain, "Revocation"
    except:
        pass
    return None


def main():
    show_header()

    tasks = [(ip, domain) for ip in ips for domain in domains]
    total = len(tasks)
    completed = 0
    found_count = 0
    ip_stats = Counter()

    console = Console()
    progress = Progress(
        SpinnerColumn(),
        BarColumn(bar_width=50),
        TaskProgressColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        TextColumn("📊 [green]{task.fields[status]}"),
        console=console,
    )

    task1 = progress.add_task("[red]Testing...", total=total, status="Starting...")

    table1 = Table(
        title="[bold]Scan Results",
        box=box.ROUNDED,
        border_style="blue",
        header_style="bold white",
    )

    table1.add_column("IP", style="cyan", width=16, vertical="bottom")
    table1.add_column("Domain", style="bright_blue", width=30, vertical="bottom")

    dir_path = pathlib.Path(__file__).parent / DEFAULT_OUTPUT_DIR

    if not pathlib.Path(dir_path).exists():
        os.mkdir(dir_path)

    f = open(f"{dir_path}/scan_results.txt", "w+")

    f_ip = open(f"{dir_path}/ips.txt", "w+")
    f_sni = open(f"{dir_path}/sni.txt", "w+")

    written_ips = set()
    written_sni = set()

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        try:
            futures = {
                executor.submit(check_pair, ip, domain): (ip, domain)
                for ip, domain in tasks
            }

            progress.start()

            for future in as_completed(futures):
                res = future.result()
                completed += 1

                progress.update(
                    task1, completed=completed, status=f"Found {found_count} domains"
                )

                if res:
                    ip, dom, status = res
                    found_count += 1
                    ip_stats[ip] += 1

                    table1.add_row(
                        f"{ip:<15}",
                        f"{dom:<25}",
                    )

                    if ip not in written_ips:
                        f_ip.write(f"{ip}\n")
                        written_ips.add(ip)

                    if dom not in written_sni:
                        f_sni.write(f"{dom}\n")
                        written_sni.add(dom)

                    f.write(f"{ip}  {dom}\n")
                    f.flush()

                    f_ip.flush()
                    f_sni.flush()

        except KeyboardInterrupt:
            print(f"\n{C_RED}[!] Operation cancelled by user.{RESET}")
            for future in futures:
                future.cancel()

            # Shutdown executor immediately
            executor.shutdown(wait=False, cancel_futures=True)

    f.close()
    f_ip.close()
    f_sni.close()
    progress.stop()

    console.clear()
    console.print(table1)

    if found_count > 0:
        top_ip = ip_stats.most_common(1)[0]
        print()
        print(
            f"\n  {BOLD}{C_YELLOW}STATS:{RESET} Top IP: {C_GREEN}{top_ip[0]}{RESET} ({top_ip[1]} hits)"
        )
        print()

    show_footer()
    if os.name == "nt":
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
