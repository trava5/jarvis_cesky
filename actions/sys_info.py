"""Systémové informace přes psutil a příkazy Windows/PowerShell."""

import subprocess
import datetime

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


def sys_info(query: str) -> str:
    query = query.lower().strip()
    results = []

    if query in ("battery", "all"):
        results.append(_battery())
    if query in ("cpu", "processor", "all"):
        results.append(_cpu())
    if query in ("ram", "memory", "all"):
        results.append(_ram())
    if query in ("disk", "storage", "all"):
        results.append(_disk())
    if query in ("time", "all"):
        now = datetime.datetime.now()
        results.append(f"Čas: {now.strftime('%H:%M:%S')}")
    if query in ("date", "all"):
        now = datetime.datetime.now()
        results.append(f"Datum: {now.strftime('%d.%m.%Y')}")
    if query in ("network", "wifi", "all"):
        results.append(_network())

    if not results:
        results.append(f"Neznámý dotaz: {query}. Použijte battery/cpu/ram/disk/time/date/network/all.")

    return "\n".join(r for r in results if r)


def _battery() -> str:
    if HAS_PSUTIL:
        bat = psutil.sensors_battery()
        if bat:
            status = "nabíjí se" if bat.power_plugged else "napájení z baterie"
            return f"Baterie: {bat.percent:.0f}% - {status}"
    # Záložní řešení přes PowerShell.
    try:
        out = subprocess.check_output(
            ["powershell", "-Command",
             "Get-WmiObject Win32_Battery | Select-Object EstimatedChargeRemaining,BatteryStatus | ConvertTo-Json"],
            text=True, timeout=8, stderr=subprocess.DEVNULL,
        )
        import json
        data = json.loads(out.strip())
        if isinstance(data, list):
            data = data[0]
        pct = data.get("EstimatedChargeRemaining", "?")
        status_code = data.get("BatteryStatus", 0)
        status = "nabíjí se" if status_code in (2, 6, 7, 8, 9) else "napájení z baterie"
        return f"Baterie: {pct}% - {status}"
    except Exception:
        pass
    return "Informace o baterii se nepodařilo načíst. Zařízení ji nemusí obsahovat nebo chybí psutil."


def _cpu() -> str:
    if HAS_PSUTIL:
        usage = psutil.cpu_percent(interval=0.5)
        count = psutil.cpu_count(logical=True)
        freq = psutil.cpu_freq()
        freq_str = f", {freq.current:.0f} MHz" if freq else ""
        return f"CPU: využití {usage:.1f}% - {count} logických jader{freq_str}"
    return "Informace o CPU se nepodařilo načíst."


def _ram() -> str:
    if HAS_PSUTIL:
        vm = psutil.virtual_memory()
        total = vm.total / (1024 ** 3)
        used = vm.used / (1024 ** 3)
        pct = vm.percent
        return f"RAM: využito {used:.1f} GB z {total:.1f} GB ({pct:.0f}%)"
    return "Informace o RAM se nepodařilo načíst."


def _disk() -> str:
    if HAS_PSUTIL:
        du = psutil.disk_usage("C:\\")
        total = du.total / (1024 ** 3)
        used = du.used / (1024 ** 3)
        free = du.free / (1024 ** 3)
        return f"Disk (C:): využito {used:.1f} GB, volno {free:.1f} GB, celkem {total:.1f} GB"
    try:
        out = subprocess.check_output(["wmic", "logicaldisk", "get", "size,freespace,caption"],
                                      text=True, timeout=5)
        lines = [l for l in out.strip().splitlines() if l.strip() and "Caption" not in l]
        if lines:
            return f"Disk: {lines[0].strip()}"
    except Exception:
        pass
    return "Informace o disku se nepodařilo načíst."


def _network() -> str:
    # SSID Wi-Fi přes netsh.
    try:
        out = subprocess.check_output(
            ["netsh", "wlan", "show", "interfaces"],
            text=True, timeout=5, stderr=subprocess.DEVNULL,
            encoding="utf-8", errors="replace",
        )
        for line in out.splitlines():
            if "SSID" in line and "BSSID" not in line:
                ssid = line.split(":", 1)[-1].strip()
                if ssid:
                    return f"Wi-Fi: připojeno k síti {ssid}"
    except Exception:
        pass
    # Záložní zjištění IP přes ipconfig.
    try:
        out = subprocess.check_output(
            ["ipconfig"],
            text=True, timeout=5,
            encoding="utf-8", errors="replace",
        )
        for line in out.splitlines():
            if "IPv4" in line:
                ip = line.split(":", 1)[-1].strip()
                if ip and not ip.startswith("169."):
                    return f"Síť: IP adresa {ip}"
    except Exception:
        pass
    return "Nebylo nalezeno žádné síťové připojení."
