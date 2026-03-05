import os
import shutil

# Ana klasörümüz
ana_dizin = os.getcwd()

print("Temizlik robotu calisiyor...\n")

for root, dirs, files in os.walk(ana_dizin):
    # Alt klasörlerdeki gizli .git klasörlerini bul ve acımadan sil (Ana dizindekine dokunma)
    if '.git' in dirs and root != ana_dizin:
        git_yolu = os.path.join(root, '.git')
        print(f"Silindi (Hatalı Gizli Klasör): {git_yolu}")
        shutil.rmtree(git_yolu)

    # Tüm __init__.py dosyalarını bul ve içini bembeyaz bir sayfa yap
    for file in files:
        if file == '__init__.py':
            init_yolu = os.path.join(root, file)
            print(f"İçi temizlendi: {init_yolu}")
            with open(init_yolu, 'w', encoding='utf-8') as f:
                f.write("") # İçini tamamen boşaltır

print("\n🚀 TEMIZLIK KUSURSUZ SEKILDE TAMAMLANDI!")