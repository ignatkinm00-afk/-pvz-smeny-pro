import os
import shutil

# 1. Создаем все нужные папки автоматически
os.makedirs("www", exist_ok=True)
os.makedirs("assets", exist_ok=True)
os.makedirs(".github/workflows", exist_ok=True)

# 2. Копируем index.html в папку www
if os.path.exists("index.html"):
    shutil.copy("index.html", "www/index.html")
    print("✅ Файл index.html успешно скопирован в папку www/")
else:
    print("⚠️ ВНИМАНИЕ: Файл index.html не найден рядом со скриптом! Не забудь положить его в папку www/")

# 3. Кастомный логотип приложения 1024x1024 (assets/icon.svg)
icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E1B4B"/>
      <stop offset="50%" stop-color="#311042"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <linearGradient id="boxGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#A855F7"/>
      <stop offset="50%" stop-color="#6366F1"/>
      <stop offset="100%" stop-color="#005BFF"/>
    </linearGradient>
    <linearGradient id="badgeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#10B981"/>
      <stop offset="100%" stop-color="#059669"/>
    </linearGradient>
  </defs>
  <rect width="1024" height="1024" rx="220" fill="url(#bg)"/>
  <circle cx="512" cy="480" r="320" fill="url(#boxGrad)" opacity="0.22"/>
  <rect x="212" y="240" width="600" height="560" rx="110" fill="url(#boxGrad)"/>
  <rect x="252" y="370" width="520" height="390" rx="75" fill="#0F172A" opacity="0.92"/>
  <rect x="332" y="180" width="56" height="120" rx="28" fill="#E2E8F0"/>
  <rect x="636" y="180" width="56" height="120" rx="28" fill="#E2E8F0"/>
  <path d="M512 435 L660 510 L512 585 L364 510 Z" fill="#A855F7"/>
  <path d="M364 510 L512 585 L512 710 L364 635 Z" fill="#6366F1"/>
  <path d="M660 510 L512 585 L512 710 L660 635 Z" fill="#3B82F6"/>
  <circle cx="730" cy="710" r="130" fill="#0F172A"/>
  <circle cx="730" cy="710" r="108" fill="url(#badgeGrad)"/>
  <path d="M680 710 L715 745 L785 675" fill="none" stroke="#FFFFFF" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

# 4. Экран загрузки 2732x2732 (assets/splash.svg)
splash_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2732 2732" width="2732" height="2732">
  <rect width="2732" height="2732" fill="#0F172A"/>
  <circle cx="1366" cy="1366" r="550" fill="#6366F1" opacity="0.15"/>
  <g transform="translate(854, 854)">
    <rect x="212" y="240" width="600" height="560" rx="110" fill="#6366F1"/>
    <rect x="252" y="370" width="520" height="390" rx="75" fill="#0F172A"/>
    <path d="M512 435 L660 510 L512 585 L364 510 Z" fill="#A855F7"/>
    <path d="M364 510 L512 585 L512 710 L364 635 Z" fill="#6366F1"/>
    <path d="M660 510 L512 585 L512 710 L660 635 Z" fill="#3B82F6"/>
  </g>
</svg>
"""

# 5. Файл package.json
package_json = """{
  "name": "pvz-shifts-pro",
  "version": "1.0.0",
  "description": "ПВЗ Смены PRO: Календарь смен, биржа подмен и расчет ЗП",
  "main": "www/index.html",
  "scripts": {
    "build": "echo 'Ready'"
  },
  "dependencies": {
    "@capacitor/android": "^6.0.0",
    "@capacitor/cli": "^6.0.0",
    "@capacitor/core": "^6.0.0"
  },
  "devDependencies": {
    "@capacitor/assets": "^3.0.5"
  }
}
"""

# 6. Конфигурация Android-приложения (capacitor.config.json)
capacitor_config = """{
  "appId": "ru.maximeze.pvzshifts",
  "appName": "ПВЗ Смены PRO",
  "webDir": "www",
  "bundledWebRuntime": false
}
"""

# 7. Скрипт авто-сборки APK на GitHub (.github/workflows/build-apk.yml)
github_workflow = """name: Build & Release Android APK

on:
  push:
    branches: [ "main", "master" ]
  workflow_dispatch:

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Скачивание кода репозитория
        uses: actions/checkout@v4

      - name: Установка Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Установка Java 17
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Установка пакетов Capacitor и генератора иконок
        run: npm install

      - name: Создание Android-проекта
        run: |
          if [ ! -d "android" ]; then
            npx cap add android
          fi
          npx cap sync android

      - name: Генерация кастомной иконки и Splash-экрана для Android
        run: |
          npx capacitor-assets generate --android --iconBackgroundColor '#0F172A' --iconBackgroundColorDark '#0F172A' --splashBackgroundColor '#0F172A' --splashBackgroundColorDark '#0F172A'

      - name: Сборка APK файла
        working-directory: ./android
        run: |
          chmod +x gradlew
          ./gradlew assembleDebug
          cp app/build/outputs/apk/debug/app-debug.apk ../PVZ-Smeny-PRO.apk

      - name: Загрузка APK в раздел Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: PVZ-Smeny-PRO-APK
          path: PVZ-Smeny-PRO.apk

      - name: Авто-публикация APK в раздел Releases
        uses: softprops/action-gh-release@v2
        with:
          tag_name: latest
          name: "ПВЗ Смены PRO — Актуальная сборка APK"
          body: "Готовый установочный файл **PVZ-Smeny-PRO.apk** для Android с кастомной иконкой (Управляющий + Оператор ПВЗ)."
          files: PVZ-Smeny-PRO.apk
          prerelease: false
"""

# 8. Описание для главной страницы GitHub (README.md)
readme_md = """<div align="center">
  <img src="assets/icon.svg" width="130" height="130" alt="ПВЗ Смены PRO Logo">
  <h1>📦 ПВЗ Смены PRO: Календарь и Расчет ЗП</h1>
  <p>Мобильное приложение для владельцев, управляющих и операторов пунктов выдачи заказов (<b>Wildberries, Ozon, Яндекс Маркет, Авито</b>)</p>
</div>

---

## 📲 Скачать на Android

Нажмите на ссылку ниже, чтобы скачать готовый установочный файл **`PVZ-Smeny-PRO.apk`**:

👉 **[СКАЧАТЬ APK (Последняя версия)](../../releases/latest/download/PVZ-Smeny-PRO.apk)**

---

## 🔥 Основные возможности
* **Режим Управляющего ПВЗ:** мульти-ПВЗ учет (WB, Ozon, Яндекс), быстрая кисть назначения смен в 1 тап, авто-график 2/2, 3/3, 5/2, учет премий/штрафов, выгрузка в Excel и отправка расчетных листов в мессенджеры.
* **Режим Сотрудника ПВЗ:** личный дашборд заработка, отметка выхода на смену, биржа подмен и мгновенная синхронизация графика по коду.
"""

# 9. Записываем все файлы на диск
with open("assets/icon.svg", "w", encoding="utf-8") as f:
    f.write(icon_svg)

with open("assets/splash.svg", "w", encoding="utf-8") as f:
    f.write(splash_svg)

with open("package.json", "w", encoding="utf-8") as f:
    f.write(package_json)

with open("capacitor.config.json", "w", encoding="utf-8") as f:
    f.write(capacitor_config)

with open(".github/workflows/build-apk.yml", "w", encoding="utf-8") as f:
    f.write(github_workflow)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_md)

print("🚀 УСПЕХ! Все файлы и иконки созданы! Теперь можно загружать их на GitHub.")
input("Нажми Enter, чтобы закрыть окно...")
