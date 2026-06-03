# Sprawozdanie z Zadania 2 – Automatyzacja budowania obrazów w GitHub Actions
**Autor:** Andrzej Iwanicki  
**Przedmiot:** Technologie Chmurowe  

---

## 1. Architektura potoku CI i konfiguracja etapów

W ramach pliku .github/workflows/ci.yml zaimplementowano następujące, następujące po sobie kroki:
1. **Checkout:** Pobranie kodu źródłowego aplikacji z repozytorium.
2. **QEMU & Buildx:** Instalacja emulatora QEMU w celu natywnego wsparcia kompilacji dla architektury ARM oraz wdrożenie zaawansowanego mechanizmu Docker Buildx opartego na sterowniku docker-container.
3. **Logowanie:** * Do rejestru **GHCR** za pomocą automatycznego tokenu ${{ secrets.GITHUB_TOKEN }}.
   * Do rejestru **DockerHub** za pomocą wcześniej przygotowanych sekretów repozytorium: DOCKERHUB_USERNAME oraz tokenu PAT jako DOCKERHUB_TOKEN.
4. **Przygotowanie Metadanych:** Wykorzystanie akcji docker/metadata-action@v5 do automatycznego wyliczania tagów OCI.
5. **Optymalizacja Cache:** Budowanie wstępne obrazu na platformy linux/amd64 oraz linux/arm64 i wysłanie warstw cache bezpośrednio na konto DockerHub.
6. **Skanowanie bezpieczeństwa (Test CVE):** Zbudowanie lokalnego obrazu dla architektury maszynowej runnera  i wykonanie testu skanerem **Trivy**.
7. **Wypchnięcie gotowego obrazu:** Po zaliczeniu skanowania CVE, Buildx buduje i ostatecznie wysyła wieloplatformowy manifest do ghcr.io.

---

## 2. Przyjęty sposób tagowania obrazów i danych cache

### Tagowanie obrazu aplikacji
Dla obrazu wynikowego w GitHub Container Registry zastosowano reguły automatycznego tagowania na podstawie zdarzeń w Git:
* latest – generowany automatycznie, dla kodu scalanego z główną gałęzią main.
* sha-<hash> – unikalny, krótki identyfikator SHA commitu z Gita.
* semver – reaguje wyłącznie na mechanizm git tags, pozwalając na kontrolowane wydawanie wersji produkcyjnych.

### Tagowanie i dystrybucja danych cache
Dane cache potoku są przesyłane do repozytorium na DockerHub: andrzejiwa/aplikacja-pogodowa-cache z jawnym, stałym tagiem :cache. 

---

## 3. Realizacja i wynik testu CVE

Zatrzymanie potoku w przypadku wykrycia podatności wykonano przy użyciu skanera **Trivy**.
* **Zaimplementowana logika:** W konfiguracji kroku skanującego zadeklarowano parametr exit-code: '1' oraz severity: 'HIGH,CRITICAL. Jeśli skaner wykryje w warstwach obrazu jakiekolwiek zagrożenie sklasyfikowane jako wysokie lub krytyczne, proces natychmiast przerywa działanie całego pipeline'u.

---

## 4. Konfiguracja uprawnień środowiskowych
W konfiguracji repozytorium GitHub ręcznie zmodyfikowano domyślne zachowanie tokenu automatycznego:
* W zakładce Settings -> Actions -> General -> Workflow permissions przyznano uprawnienia "Read and write permissions".
