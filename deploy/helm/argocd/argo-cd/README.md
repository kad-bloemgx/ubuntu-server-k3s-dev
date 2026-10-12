# Argo CD

## Repository-toegang via SSH

Gebruik voor de repository en de Git-bronnen in de ApplicationSet dezelfde SSH-URL:

```text
git@github.com:kad-bloemgx/raspberry_home-assistant.git
```

Voeg de publieke SSH-sleutel in GitHub toe bij **Settings -> Deploy keys** van
deze repository. Read-only toegang is voldoende; laat **Allow write access** uit.

Zet de private SSH-sleutel niet in Git, `values.yaml` of een Helm-template.
Maak vanaf een machine met `kubectl`-toegang en de private sleutel lokaal een
repository-Secret aan in de bestaande `argo-cd`-namespace:

```bash
kubectl -n argo-cd create secret generic raspberry-home-assistant-repo \
  --from-literal=type=git \
  --from-literal=url=git@github.com:kad-bloemgx/raspberry_home-assistant.git \
  --from-file=sshPrivateKey=/pad/naar/de/private-key

kubectl -n argo-cd label secret raspberry-home-assistant-repo \
  argocd.argoproj.io/secret-type=repository
```

Vervang `/pad/naar/de/private-key` door het pad naar de private sleutel, niet
naar het `.pub`-bestand. De twee commando's maken een nieuwe Secret aan en
markeren deze als Argo CD repository-configuratie. Als de repository al is
geregistreerd, werk dan de bestaande repository-Secret bij in plaats van een
duplicaat aan te maken.

Argo CD gebruikt deze Secret voor SSH-authenticatie; een aparte SSH-agent is
niet nodig. Controleer de verbinding via **Settings -> Repositories** in Argo CD.
De Helm-chart mag de repository-URL bevatten, maar niet de private sleutel.
Wil je de Secret via Git beheren, gebruik dan een versleutelde oplossing zoals
SOPS of Sealed Secrets.

## Dubbele repository-registraties voorkomen

De chart registreert de repository niet via `argo-cd.configs.repositories`.
De repository-Secret met de SSH-private key is de enige configuratiebron voor
de verbinding. De SSH-URL's in de ApplicationSet blijven behouden: deze
verwijzen naar de repository, maar maken geen repository-Secret aan.

Controleer voor de eerste synchronisatie dat de handmatige repository-Secret
bestaat en dat de SSH-verbinding werkt. Bij synchronisatie met pruning wordt
de oude, door de chart beheerde repository-Secret verwijderd. Verwijder daarna
eventuele overige ongebruikte entries via **Settings -> Repositories**. Behoud
de entry voor de handmatige Secret met de werkende SSH-private key.
