import paramiko
import time
import re
from collections import defaultdict

# SSH bağlantısı için gerekli bilgiler
host = 'ip'
port = 22  # SSH portu genellikle 22'dir
username = 'username'
password = 'password'
enable_password = 'enable_password'
output_file_path = "vlan_mac_counts.txt"  # Çıktı dosyasının yolu

def get_mac_counts_per_vlan(output):
    vlan_mac_counts = defaultdict(int)
    lines = output.splitlines()
    for line in lines:
        match = re.match(r'\s*(\d+)\s+([\da-fA-F\.]+)\s+\w+\s+(\w+)', line)
        if match:
            vlan_id = match.group(1)
            vlan_mac_counts[vlan_id] += 1
    return vlan_mac_counts

try:
    # SSH istemcisini oluştur
    ssh_client = paramiko.SSHClient()

    # Paramiko'nun host anahtarını otomatik olarak kabul etmesini sağla
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Bağlantıyı gerçekleştir
    print("Connecting to the switch...")
    ssh_client.connect(hostname=host, port=port, username=username, password=password)
    print("Connected to the switch.")

    # SSH oturumu oluştur
    ssh_session = ssh_client.invoke_shell()
    print("SSH session created.")

    # switch'e giriş yapmadan önce bekle
    print("Waiting for 5 seconds before entering enable mode...")
    time.sleep(5)
    
    print("Entering enable mode...")
    ssh_session.send('enable\n')
    time.sleep(1)  # Bir saniye bekle
    ssh_session.send(f'{enable_password}\n')  # enable parolası
    time.sleep(1)  # Bir saniye bekle
    ssh_session.send('terminal length 0\n')  # Tam ekran çıktı almak için
    time.sleep(1)
    ssh_session.send('show mac address-table\n')
    time.sleep(5)  # Komutun tamamlanması için yeterli süre ver

    # Çıktıyı al
    print("Receiving output...")
    output = ''
    while True:
        time.sleep(1)
        if ssh_session.recv_ready():
            chunk = ssh_session.recv(65535).decode()
            output += chunk
            # Son alınan çıktı parçasını kontrol et
            if "Total number of mac address" in chunk:
                break
    print("Output received.")

    # Çıktıyı kontrol et
    print(f"Output length: {len(output)} characters")

    # Çıktıyı dosyaya yaz
    with open("raw_output.txt", 'w') as raw_file:
        raw_file.write(output)
    print("Raw output written to 'raw_output.txt'")

    # MAC adresi sayısını VLAN başına hesapla
    vlan_mac_counts = get_mac_counts_per_vlan(output)
    
    # Debug: Print the VLAN MAC counts
    for vlan_id, count in vlan_mac_counts.items():
        print(f'VLAN {vlan_id}: {count} MAC addresses')

    # Sonuçları dosyaya yaz
    with open(output_file_path, 'w') as f:
        for vlan_id, count in vlan_mac_counts.items():
            f.write(f'VLAN {vlan_id}: {count} MAC addresses\n')
    print(f"Çıktı dosyası '{output_file_path}' adıyla kaydedildi.")

except paramiko.AuthenticationException:
    print("Kimlik doğrulama başarısız. Kullanıcı adı veya şifre yanlış.")
except paramiko.SSHException as ssh_err:
    print(f"SSH bağlantı hatası: {ssh_err}")
except Exception as e:
    print(f"Bir hata oluştu: {e}")
finally:
    # Bağlantıyı kapat
    ssh_client.close()
    print("SSH connection closed.")