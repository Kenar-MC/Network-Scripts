import paramiko
import time

# SSH bağlantısı için gerekli bilgiler
host = 'hostip'
port = 22  # SSH portu genellikle 22'dir
username = 'username'
password = 'password'

output_file_path = "ssh_output.txt"  # Çıktı dosyasının yolu

try:
    # SSH istemcisini oluştur
    ssh_client = paramiko.SSHClient()

    # Paramiko'nun host anahtarını otomatik olarak kabul etmesini sağla
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Bağlantıyı gerçekleştir
    ssh_client.connect(hostname=host, port=port, username=username, password=password)

    # SSH oturumu oluştur
    ssh_session = ssh_client.invoke_shell()

    # switch'e giriş yap
    ssh_session.send('enable\n')
    time.sleep(1)  # Bir saniye bekle
    ssh_session.send('enable_password\n')  # enable parolası
    time.sleep(1)  # Bir saniye bekle
    ssh_session.send('show vlan brief\n')
    time.sleep(2)  # Komutun tamamlanması için biraz daha fazla bekleyebiliriz
 
    # Çıktıyı al
    output = ''
    while True:
        output += ssh_session.recv(65535).decode()
        if re.search(r'--More--', output):
            ssh_session.send(' ')
            time.sleep(1)
        else:
            break

    # Çıktıyı dosyaya yaz
    with open(output_file_path, 'w') as f:
        f.write(output)

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