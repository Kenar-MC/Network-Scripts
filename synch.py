def remove_duplicates(input_file, output_file=None):
    # Dosyayı oku ve her satırı bir listede sakla
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Tekrarlanan satırları bul
    unique_lines = set()
    duplicate_lines = set()
    for line in lines:
        if line in unique_lines:
            duplicate_lines.add(line)
        else:
            unique_lines.add(line)

    # Tekrarlanan satırları kaldırarak yeni bir liste oluştur
    unique_lines = [line for line in lines if line not in duplicate_lines]

    # Sonucu dosyaya yaz veya ekrana yazdır
    if output_file:
        with open(output_file, 'w') as f:
            f.writelines(unique_lines)
    else:
        for line in unique_lines:
            print(line, end='')

# Örnek kullanım
input_file = 'relay_number.txt'
output_file = 'temiz_dosya.txt'
remove_duplicates(input_file, output_file)
